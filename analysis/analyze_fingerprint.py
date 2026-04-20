#!/usr/bin/env python3
"""
Unified browser fingerprint analysis.

For each browser experiment pcap:
1. Extract SYN packet fingerprint (TTL, window, options)
2. Match to DB requests (which have UA string)
3. Infer TCP OS from SYN fingerprint
4. Infer UA OS from User-Agent string
5. Determine mismatch

Output: data/unified/20260331/unified_fingerprint.csv
"""

import csv
import subprocess
import sqlite3
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).parent.parent
DATA_DIR = ROOT / "data"
OUT_CSV = DATA_DIR / "unified" / "20260331" / "unified_fingerprint.csv"

# Browser experiment pcaps → provider groups
BROWSER_PCAPS = [
    {
        "pcap": DATA_DIR / "captures" / "us" / "20260327_browser_full.pcap",
        "providers": ["brightdata", "soax", "direct"],
    },
    {
        "pcap": DATA_DIR / "captures" / "us" / "20260327_iproyal_browser.pcap",
        "providers": ["iproyal"],
    },
    {
        "pcap": DATA_DIR / "captures" / "us" / "20260328_oxylabs_browser.pcap",
        "providers": ["oxylabs", "oxylabs_mobile", "oxylabs_isp"],
    },
    {
        "pcap": DATA_DIR / "captures" / "us" / "20260329_netnut_browser.pcap",
        "providers": ["netnut"],
    },
    {
        "pcap": DATA_DIR / "captures" / "us" / "20260331_bd_mobile_isp_browser.pcap",
        "providers": ["brightdata_mobile", "brightdata_isp"],
    },
]

DB_PATH = DATA_DIR / "db" / "us.db"


def extract_syn_fingerprints(pcap_file):
    """Extract SYN packet fingerprints from pcap."""
    cmd = [
        "tshark", "-r", str(pcap_file), "-T", "fields",
        "-e", "frame.time_epoch",
        "-e", "ip.src", "-e", "ip.dst",
        "-e", "tcp.srcport", "-e", "tcp.dstport",
        "-e", "tcp.flags", "-e", "tcp.len",
        "-e", "ip.ttl", "-e", "tcp.window_size_value",
        "-e", "tcp.options.mss_val",
        "-e", "tcp.option_kind",
        "-e", "tcp.window_size_scalefactor",
        "-Y", "tcp.port == 443",
        "-E", "separator=|",
    ]
    print(f"  tshark on {pcap_file.name}...")
    result = subprocess.run(cmd, capture_output=True, text=True)

    connections = defaultdict(lambda: {
        "syn": None, "syn_ack": None, "ack": None, "first_data": None,
        "syn_ttl": None, "syn_window": None, "syn_mss": None,
        "syn_options": None, "syn_wscale": None, "client_ip": None,
    })

    for line in result.stdout.strip().split("\n"):
        if not line.strip():
            continue
        fields = line.split("|")
        if len(fields) < 12:
            continue

        ts = float(fields[0])
        src_ip, dst_ip = fields[1], fields[2]
        src_port, dst_port = fields[3], fields[4]
        flags = fields[5]
        tcp_len = int(fields[6]) if fields[6] else 0
        ttl = fields[7]
        window = fields[8]
        mss = fields[9]
        options = fields[10]
        wscale = fields[11]

        if dst_port == "443":
            conn_key = f"{src_ip}:{src_port}->{dst_ip}:{dst_port}"
            is_c2s = True
        else:
            conn_key = f"{dst_ip}:{dst_port}->{src_ip}:{src_port}"
            is_c2s = False

        conn = connections[conn_key]
        flags_int = int(flags, 16) if flags.startswith("0x") else int(flags)

        if is_c2s and (flags_int & 0x12) == 0x02:  # SYN
            conn["syn"] = ts
            conn["client_ip"] = src_ip
            conn["syn_ttl"] = int(ttl) if ttl else None
            conn["syn_window"] = int(window) if window else None
            conn["syn_mss"] = mss
            conn["syn_options"] = options
            conn["syn_wscale"] = wscale
        elif not is_c2s and (flags_int & 0x12) == 0x12:  # SYN-ACK
            conn["syn_ack"] = ts
        elif is_c2s and (flags_int & 0x12) == 0x10:  # ACK
            if conn["syn_ack"] and not conn["ack"]:
                conn["ack"] = ts
        if is_c2s and tcp_len > 0 and not conn["first_data"]:
            conn["first_data"] = ts

    return connections


def infer_tcp_os(ttl, window, options):
    """Infer OS from SYN packet fingerprint."""
    if ttl is None:
        return "unknown"
    # Initial TTL inference
    if ttl > 200:
        return "network_equipment"  # TTL 255
    elif ttl > 100:
        return "windows"  # TTL 128
    elif ttl > 32:
        return "linux"  # TTL 64
    else:
        return "unknown"


def infer_ua_os(ua):
    """Infer claimed OS from User-Agent string."""
    if not ua:
        return "unknown"
    ua_lower = ua.lower()
    if "macintosh" in ua_lower or "mac os" in ua_lower:
        return "macos"
    elif "windows" in ua_lower:
        return "windows"
    elif "linux" in ua_lower or "x11" in ua_lower:
        return "linux"
    elif "android" in ua_lower:
        return "linux"
    elif "iphone" in ua_lower or "ipad" in ua_lower:
        return "ios"
    elif "curl" in ua_lower:
        return "curl"
    else:
        return "unknown"


def compute_mismatch(tcp_os, ua_os):
    """Determine if TCP fingerprint mismatches UA claim."""
    if tcp_os == "unknown" or ua_os == "unknown" or ua_os == "curl":
        return "inconclusive"
    if tcp_os == ua_os:
        return "match"
    # linux TCP + macos UA = mismatch (proxy exit is Linux, client claims macOS)
    # linux TCP + windows UA = mismatch
    # windows TCP + macos UA = mismatch
    # windows TCP + linux UA = mismatch
    return "mismatch"


def match_to_db(connections, providers, epoch_min=0, epoch_max=0):
    """Match connections to DB requests for given providers."""
    db = sqlite3.connect(str(DB_PATH))
    db.row_factory = sqlite3.Row
    placeholders = ",".join(f"'{p}'" for p in providers)
    conditions = [f"param_src IN ({placeholders})"]
    if epoch_min:
        conditions.append(f"epoch > {epoch_min}")
    if epoch_max:
        conditions.append(f"epoch < {epoch_max}")
    conditions.append("(user_agent LIKE '%Chrome%' OR user_agent LIKE '%Firefox%' OR param_src = 'direct')")
    query = f"SELECT * FROM requests WHERE {' AND '.join(conditions)} ORDER BY epoch"
    rows = [dict(r) for r in db.execute(query).fetchall()]
    db.close()

    used = set()
    sorted_conns = sorted(
        [(k, v) for k, v in connections.items() if v.get("first_data")],
        key=lambda x: x[1]["first_data"],
    )
    for conn_key, conn in sorted_conns:
        best, bd, bi = None, 10.0, -1
        for i, row in enumerate(rows):
            if i in used:
                continue
            diff = abs(row["epoch"] - conn["first_data"])
            if diff < bd:
                bd, best, bi = diff, row, i
        if best and bi >= 0:
            used.add(bi)
            conn["request"] = best
        else:
            conn["request"] = None

    matched = sum(1 for _, v in connections.items() if v.get("request"))
    return connections, matched, len(rows)


def main():
    all_results = []

    for entry in BROWSER_PCAPS:
        pcap = entry["pcap"]
        providers = entry["providers"]
        if not pcap.exists():
            print(f"SKIP: {pcap} not found")
            continue

        print(f"\n[{pcap.name}] providers={providers}")
        conns = extract_syn_fingerprints(pcap)
        conns, matched, total = match_to_db(conns, providers)
        print(f"  Matched {matched}/{total} DB requests ({len(conns)} raw flows)")

        for _, conn in conns.items():
            if not all([conn["syn"], conn["syn_ack"], conn["ack"], conn["first_data"]]):
                continue
            if not conn.get("request"):
                continue
            tcp_rtt = conn["ack"] - conn["syn_ack"]
            gap = conn["first_data"] - conn["ack"]
            if tcp_rtt < 0.001:
                continue

            req = conn["request"]
            ttl = conn["syn_ttl"]
            window = conn["syn_window"]
            options = conn["syn_options"]
            ua = req.get("user_agent", "")

            tcp_os = infer_tcp_os(ttl, window, options)
            ua_os = infer_ua_os(ua)
            mismatch = compute_mismatch(tcp_os, ua_os)

            all_results.append({
                "timestamp": req.get("epoch"),
                "provider": req.get("param_src", ""),
                "protocol": req.get("param_proto", ""),
                "country": req.get("param_country", ""),
                "client_ip": conn["client_ip"],
                "user_agent": ua,
                "ua_os": ua_os,
                "syn_ttl": ttl,
                "syn_window": window,
                "syn_mss": conn["syn_mss"],
                "syn_options": conn["syn_options"],
                "syn_wscale": conn["syn_wscale"],
                "tcp_os": tcp_os,
                "gap_ms": round(gap * 1000, 3),
                "tcp_rtt_ms": round(tcp_rtt * 1000, 3),
                "fingerprint_mismatch": mismatch,
            })

    print(f"\n=== Writing {OUT_CSV} ===")
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    if all_results:
        with open(OUT_CSV, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(all_results[0].keys()))
            w.writeheader()
            w.writerows(all_results)
    print(f"Total: {len(all_results)} flows")

    # Summary
    from collections import Counter
    by_prov = defaultdict(lambda: defaultdict(lambda: Counter()))
    for r in all_results:
        by_prov[r["provider"]][r["ua_os"]][r["fingerprint_mismatch"]] += 1

    print(f"\n{'Provider':<20} {'UA_OS':<10} {'N':>5} {'Match':>6} {'Mismatch':>9} {'Rate':>7}")
    print("-" * 60)
    for prov in sorted(by_prov.keys()):
        for ua_os in ["macos", "windows", "linux"]:
            c = by_prov[prov].get(ua_os)
            if not c:
                continue
            n = sum(c.values())
            mm = c.get("mismatch", 0)
            rate = 100 * mm / n if n > 0 else 0
            print(f"{prov:<20} {ua_os:<10} {n:>5} {c.get('match', 0):>6} {mm:>9} {rate:>6.1f}%")


if __name__ == "__main__":
    main()
