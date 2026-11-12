#!/usr/bin/env python3
"""
Unified per-connection feature extractor for the multi-method comparison.

Reads a pcap (pcapng is converted on the fly via tcpdump) and emits ONE JSON
record per TCP connection to port 443, carrying everything every compared
method needs, so that all methods are evaluated on identical connections:

  identity     conn_key, client_ip, server_ip, ports, first_ts
  ours         t_ack, t_first_client_data  -> gap_ms
  BADPASS      tcp_rtt_ms, tls_rtt_ms (version-specific anchors) -> delta_ms
  Casado'07    syn_ttl, syn_window, syn_mss, syn_wscale, syn_optlayout
  Huang /      per-packet (ts, dir, tcp_payload_len) for the first N packets
  Beyond RTT
  bookkeeping  n_packets, tls_version, anchor availability flags

Deliberately NOT here: labels. Labelling is done by label.py from the
experiment CSV/DB, so extraction stays a pure function of the capture.
"""
import argparse, json, os, subprocess, sys, tempfile
from collections import OrderedDict

import dpkt

MAX_PKTS = 128           # per-packet detail retained per connection
TLS_CT_CCS, TLS_CT_HANDSHAKE, TLS_CT_APPDATA = 20, 22, 23
HS_SERVER_HELLO, HS_SERVER_HELLO_DONE, HS_CLIENT_KEY_EXCHANGE = 2, 14, 16


def to_classic_pcap(path, tmpdir):
    """dpkt cannot read pcapng; tcpdump rewrites it losslessly for our fields."""
    with open(path, "rb") as f:
        magic = f.read(4)
    if magic in (b"\xd4\xc3\xb2\xa1", b"\xa1\xb2\xc3\xd4"):
        return path
    # Cache key must include the full path: several captures share the
    # basename "unified.pcap", and keying on basename alone silently reuses
    # the wrong conversion.
    import hashlib
    h = hashlib.sha1(os.path.abspath(path).encode()).hexdigest()[:12]
    out = os.path.join(tmpdir, f"{os.path.basename(path)}.{h}.classic.pcap")
    if not os.path.exists(out):
        subprocess.run(["tcpdump", "-r", path, "-w", out],
                       check=True, capture_output=True)
    return out


def parse_tcp_options(opts_buf):
    """Return (mss, wscale, layout) where layout is the option-kind sequence."""
    mss = wscale = None
    layout = []
    try:
        for kind, data in dpkt.tcp.parse_opts(opts_buf):
            layout.append(kind)
            if kind == dpkt.tcp.TCP_OPT_MSS and len(data) == 2:
                mss = int.from_bytes(data, "big")
            elif kind == dpkt.tcp.TCP_OPT_WSCALE and len(data) == 1:
                wscale = data[0]
    except Exception:
        pass
    return mss, wscale, "-".join(str(k) for k in layout)


class Conn:
    __slots__ = ("client_ip", "server_ip", "sport", "dport", "t_syn", "t_synack",
                 "t_ack", "t_first_cdata", "syn_ttl", "syn_window", "syn_mss",
                 "syn_wscale", "syn_optlayout", "pkts", "n_packets",
                 "c_buf", "s_buf", "tls_version", "t_shd", "t_cke",
                 "t_server_last_hs", "t_server_at_ccs", "t_client_ccs",
                 "saw_server_hello", "first_cdata_len", "first_cdata_ct",
                 "idx_first_cdata", "idx_bp_anchor", "pkt_i")

    def __init__(self):
        for s in self.__slots__:
            setattr(self, s, None)
        self.pkts = []
        self.n_packets = 0
        self.c_buf = bytearray()
        self.s_buf = bytearray()
        self.saw_server_hello = False


def walk_tls_records(buf, on_record):
    """Walk complete TLS records at the head of buf; drop what we consumed.

    on_record(content_type, body_bytes) is called per complete record.
    Returns the number of bytes consumed.
    """
    off = 0
    n = len(buf)
    while n - off >= 5:
        ct = buf[off]
        ln = int.from_bytes(buf[off + 3:off + 5], "big")
        # Sanity: valid content types and plausible length, else stop (encrypted
        # or non-TLS stream -- we must not desynchronise on garbage).
        if ct not in (20, 21, 22, 23) or ln > 18432:
            break
        if n - off - 5 < ln:
            break
        on_record(ct, bytes(buf[off + 5:off + 5 + ln]))
        off += 5 + ln
    return off


def extract(pcap_path, tmpdir, server_port=443):
    path = to_classic_pcap(pcap_path, tmpdir)
    conns = OrderedDict()
    live = {}   # base 4-tuple -> current instance number

    with open(path, "rb") as fh:
        reader = dpkt.pcap.Reader(fh)
        linktype = reader.datalink()
        for ts, buf in reader:
            try:
                if linktype == dpkt.pcap.DLT_EN10MB:
                    eth = dpkt.ethernet.Ethernet(buf)
                    ip = eth.data
                elif linktype == dpkt.pcap.DLT_LINUX_SLL:
                    ip = dpkt.sll.SLL(buf).data
                else:
                    ip = dpkt.ethernet.Ethernet(buf).data
            except Exception:
                continue
            if not isinstance(ip, dpkt.ip.IP):
                continue
            tcp = ip.data
            if not isinstance(tcp, dpkt.tcp.TCP):
                continue

            if tcp.dport == server_port:
                c2s = True
                cip, sip = ip.src, ip.dst
                sport, dport = tcp.sport, tcp.dport
            elif tcp.sport == server_port:
                c2s = False
                cip, sip = ip.dst, ip.src
                sport, dport = tcp.dport, tcp.sport
            else:
                continue

            import socket
            base = (f"{socket.inet_ntoa(cip)}:{sport}->"
                    f"{socket.inet_ntoa(sip)}:{dport}")
            syn = bool(tcp.flags & dpkt.tcp.TH_SYN)
            ack = bool(tcp.flags & dpkt.tcp.TH_ACK)
            plen = len(tcp.data)

            # Ephemeral ports are reused within a long capture. A fresh
            # client SYN on a key that already carries a handshake starts a
            # NEW connection instance; without this, two connections merge
            # and their timestamps produce nonsense (negative TLS RTTs).
            inst = live.get(base, 0)
            if syn and not ack and inst and conns[(base, inst)].t_syn is not None:
                inst += 1
                live[base] = inst
            elif base not in live:
                inst = live[base] = 1

            key = (base, inst)
            c = conns.get(key)
            if c is None:
                c = conns[key] = Conn()
                c.client_ip = socket.inet_ntoa(cip)
                c.server_ip = socket.inet_ntoa(sip)
                c.sport, c.dport = sport, dport

            c.n_packets += 1
            c.pkt_i = (c.pkt_i or 0) + 1
            if len(c.pkts) < MAX_PKTS:
                c.pkts.append((round(ts, 9), 1 if c2s else 0, plen))

            # --- TCP handshake anchors -------------------------------------
            if c2s and syn and not ack:
                if c.t_syn is None:
                    c.t_syn = ts
                    c.syn_ttl = ip.ttl
                    c.syn_window = tcp.win
                    (c.syn_mss, c.syn_wscale,
                     c.syn_optlayout) = parse_tcp_options(tcp.opts)
            elif (not c2s) and syn and ack:
                if c.t_synack is None:
                    c.t_synack = ts
            elif c2s and ack and plen == 0 and c.t_synack is not None \
                    and c.t_ack is None:
                c.t_ack = ts

            # --- first client data (our signal) ----------------------------
            if c2s and plen > 0 and c.t_first_cdata is None:
                c.t_first_cdata = ts
                c.idx_first_cdata = c.pkt_i
                c.first_cdata_len = plen
                c.first_cdata_ct = tcp.data[0] if plen else None

            # --- TLS record tracking (BADPASS anchors) ---------------------
            if plen:
                if c2s:
                    c.c_buf += tcp.data
                    def on_c(ct, body, _c=c, _ts=ts):
                        # TLS 1.3 middlebox-compatibility mode lets a client send
                        # a dummy ChangeCipherSpec straight after its ClientHello,
                        # i.e. BEFORE the server flight. Browsers do; curl does
                        # not. BADPASS's anchor is the client's response to the
                        # server flight, so only a CCS after ServerHello counts.
                        if (ct == TLS_CT_CCS and _c.t_client_ccs is None
                                and _c.saw_server_hello):
                            _c.t_client_ccs = _ts
                            _c.idx_bp_anchor = _c.pkt_i
                            # BADPASS's TLS 1.3 anchor is the server's last
                            # record BEFORE this point, not the last record of
                            # the whole connection.
                            _c.t_server_at_ccs = _c.t_server_last_hs
                        elif ct == TLS_CT_HANDSHAKE and body:
                            if body[0] == HS_CLIENT_KEY_EXCHANGE and _c.t_cke is None:
                                _c.t_cke = _ts
                                _c.idx_bp_anchor = _c.pkt_i
                    del c.c_buf[:walk_tls_records(c.c_buf, on_c)]
                else:
                    c.s_buf += tcp.data
                    def on_s(ct, body, _c=c, _ts=ts):
                        if ct == TLS_CT_HANDSHAKE and body:
                            ht = body[0]
                            if ht == HS_SERVER_HELLO:
                                _c.saw_server_hello = True
                                # TLS 1.2 negotiated version lives in the body;
                                # 1.3 advertises 1.2 here and uses an extension,
                                # so treat "handshake stays cleartext" as 1.2.
                                _c.tls_version = "1.2"
                            if ht == HS_SERVER_HELLO_DONE:
                                _c.t_shd = _ts
                        if _c.saw_server_hello:
                            _c.t_server_last_hs = _ts
                    del c.s_buf[:walk_tls_records(c.s_buf, on_s)]

    out = []
    for (base, inst), c in conns.items():
        if c.t_syn is None and c.t_first_cdata is None:
            continue
        key = base if inst == 1 else f"{base}#{inst}"
        gap = tcp_rtt = tls_rtt = None
        if c.t_ack is not None and c.t_first_cdata is not None:
            gap = (c.t_first_cdata - c.t_ack) * 1000.0
        if c.t_synack is not None and c.t_ack is not None:
            tcp_rtt = (c.t_ack - c.t_synack) * 1000.0
        # BADPASS TLS_RTT: 1.2 -> ServerHelloDone->ClientKeyExchange
        #                  1.3 -> last server handshake record -> client CCS
        ver = None
        if c.t_shd is not None and c.t_cke is not None:
            tls_rtt = (c.t_cke - c.t_shd) * 1000.0
            ver = "1.2"
        elif c.t_server_at_ccs is not None and c.t_client_ccs is not None:
            tls_rtt = (c.t_client_ccs - c.t_server_at_ccs) * 1000.0
            ver = "1.3"
        out.append({
            "conn_key": key,
            "client_ip": c.client_ip, "server_ip": c.server_ip,
            "sport": c.sport, "dport": c.dport,
            "first_ts": c.t_syn if c.t_syn is not None else c.t_first_cdata,
            "gap_ms": None if gap is None else round(gap, 4),
            "tcp_rtt_ms": None if tcp_rtt is None else round(tcp_rtt, 4),
            "tls_rtt_ms": None if tls_rtt is None else round(tls_rtt, 4),
            "badpass_delta_ms": (None if (tls_rtt is None or tcp_rtt is None)
                                 else round(tls_rtt - tcp_rtt, 4)),
            "tls_version": ver,
            "syn_ttl": c.syn_ttl, "syn_window": c.syn_window,
            "syn_mss": c.syn_mss, "syn_wscale": c.syn_wscale,
            "syn_optlayout": c.syn_optlayout,
            "first_cdata_len": c.first_cdata_len,
            "first_cdata_ct": c.first_cdata_ct,
            "n_packets": c.n_packets,
            "idx_first_cdata": c.idx_first_cdata,
            "idx_bp_anchor": c.idx_bp_anchor,
            "pkts": c.pkts,
        })
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pcaps", nargs="+")
    ap.add_argument("-o", "--out", required=True, help="output .jsonl")
    ap.add_argument("--tag", default=None, help="source tag stored per record")
    ap.add_argument("--tmpdir", default=None)
    a = ap.parse_args()

    tmpdir = a.tmpdir or tempfile.mkdtemp(prefix="pcapconv-")
    os.makedirs(tmpdir, exist_ok=True)
    n = 0
    with open(a.out, "w") as w:
        for p in a.pcaps:
            recs = extract(p, tmpdir)
            for r in recs:
                r["src_pcap"] = os.path.basename(p)
                if a.tag:
                    r["tag"] = a.tag
                w.write(json.dumps(r) + "\n")
                n += 1
            print(f"  {os.path.basename(p)}: {len(recs)} connections",
                  file=sys.stderr)
    print(f"wrote {n} connections -> {a.out}", file=sys.stderr)


if __name__ == "__main__":
    main()
