#!/usr/bin/env python3
"""
Analyze unified experiment data (data/unified/20260331/).

Extracts TCP-to-TLS timing gap from pcap for all 4 servers,
matches to DB metadata, produces a single CSV covering
7 providers × 15 countries × 4 servers × (HC+SOCKS5 where supported).
"""

import csv
import subprocess
import sqlite3
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).parent.parent
UNIFIED = ROOT / "data" / "unified" / "20260331"
OUT_CSV = UNIFIED / "unified_timing.csv"

# Experiment A start: Apr 3 14:45 UTC = 1775227500
EPOCH_MIN = 1775227500

SERVERS = {
    "us": {"pcap": UNIFIED / "pcap" / "us" / "unified.pcap", "db": UNIFIED / "db_us.db", "label": "US (Virginia)"},
    "ap": {"pcap": UNIFIED / "pcap" / "ap" / "unified.pcap", "db": UNIFIED / "db_ap.db", "label": "AP (Tokyo)"},
    "eu": {"pcap": UNIFIED / "pcap" / "eu" / "unified.pcap", "db": UNIFIED / "db_eu.db", "label": "EU (Paris)"},
    "sa": {"pcap": UNIFIED / "pcap" / "sa" / "unified.pcap", "db": UNIFIED / "db_sa.db", "label": "SA (Sao Paulo)"},
}


def extract_connections(pcap_file):
    """Extract TCP connection timing from pcap using tshark."""
    cmd = [
        "tshark", "-r", str(pcap_file), "-T", "fields",
        "-e", "frame.time_epoch",
        "-e", "ip.src", "-e", "ip.dst",
        "-e", "tcp.srcport", "-e", "tcp.dstport",
        "-e", "tcp.flags", "-e", "tcp.len",
        "-e", "ip.ttl", "-e", "tcp.window_size_value",
        "-Y", "tcp.port == 443",
        "-E", "separator=|",
    ]
    print(f"  Running tshark on {pcap_file.name} ({pcap_file.stat().st_size // (1024*1024)}M)...")
    result = subprocess.run(cmd, capture_output=True, text=True)

    connections = defaultdict(lambda: {
        "syn": None, "syn_ack": None, "ack": None, "first_data": None,
        "syn_ttl": None, "syn_window": None, "client_ip": None,
    })

    for line in result.stdout.strip().split("\n"):
        if not line.strip():
            continue
        fields = line.split("|")
        if len(fields) < 9:
            continue
        ts = float(fields[0])
        src_ip, dst_ip = fields[1], fields[2]
        src_port, dst_port = fields[3], fields[4]
        flags = fields[5]
        tcp_len = int(fields[6]) if fields[6] else 0
        ttl = fields[7]
        window = fields[8]

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
            conn["syn_ttl"] = ttl
            conn["syn_window"] = window
        elif not is_c2s and (flags_int & 0x12) == 0x12:  # SYN-ACK
            conn["syn_ack"] = ts
        elif is_c2s and (flags_int & 0x12) == 0x10:  # pure ACK
            if conn["syn_ack"] and not conn["ack"]:
                conn["ack"] = ts
        if is_c2s and tcp_len > 0 and not conn["first_data"]:
            conn["first_data"] = ts

    return connections


def match_to_db(connections, db_path):
    """Match connections to DB requests by timestamp proximity (<10s)."""
    db = sqlite3.connect(str(db_path))
    db.row_factory = sqlite3.Row
    rows = [dict(r) for r in db.execute(
        "SELECT epoch, param_src, param_proto, param_country, user_agent "
        "FROM requests WHERE param_src IS NOT NULL AND epoch > ? ORDER BY epoch",
        (EPOCH_MIN,)
    ).fetchall()]
    db.close()

    used = set()
    sorted_conns = sorted(
        [(k, v) for k, v in connections.items() if v.get("first_data")],
        key=lambda x: x[1]["first_data"],
    )
    for conn_key, conn in sorted_conns:
        best_match, best_diff, best_idx = None, 10.0, -1
        for i, row in enumerate(rows):
            if i in used:
                continue
            diff = abs(row["epoch"] - conn["first_data"])
            if diff < best_diff:
                best_diff, best_match, best_idx = diff, row, i
        if best_match and best_idx >= 0:
            used.add(best_idx)
            conn["request"] = best_match
        else:
            conn["request"] = None

    matched = sum(1 for _, v in connections.items() if v.get("request"))
    return connections, matched, len(rows)


def analyze_server(region, config):
    pcap = config["pcap"]
    db = config["db"]
    if not pcap.exists() or not db.exists():
        print(f"  SKIP {region}: missing pcap or DB")
        return []
    print(f"\n[{config['label']}]")
    conns = extract_connections(pcap)
    conns, matched, total = match_to_db(conns, db)
    print(f"  Matched {matched}/{total} DB requests ({len(conns)} raw flows)")

    results = []
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
        results.append({
            "timestamp": req.get("epoch"),
            "server": region,
            "client_ip": conn["client_ip"],
            "gap_ms": round(gap * 1000, 3),
            "tcp_rtt_ms": round(tcp_rtt * 1000, 3),
            "syn_ttl": conn["syn_ttl"],
            "syn_window": conn["syn_window"],
            "provider": req.get("param_src", ""),
            "protocol": req.get("param_proto", ""),
            "country": req.get("param_country", ""),
            "ua_string": req.get("user_agent", ""),
        })
    print(f"  {len(results)} complete flows")
    return results


def match_sticky_to_db(connections, db_path):
    """Match A2 sticky/rotating connections to DB requests by timestamp."""
    from urllib.parse import parse_qs
    db = sqlite3.connect(str(db_path))
    db.row_factory = sqlite3.Row
    rows = [dict(r) for r in db.execute(
        "SELECT epoch, query_string, user_agent "
        "FROM requests WHERE query_string LIKE '%session=%' ORDER BY epoch"
    ).fetchall()]
    db.close()

    # Parse query strings to extract provider/session
    for row in rows:
        qs = parse_qs(row.get("query_string", ""))
        row["provider"] = qs.get("provider", [""])[0]
        row["session_mode"] = qs.get("session", [""])[0]

    used = set()
    sorted_conns = sorted(
        [(k, v) for k, v in connections.items() if v.get("first_data")],
        key=lambda x: x[1]["first_data"],
    )
    for conn_key, conn in sorted_conns:
        best_match, best_diff, best_idx = None, 10.0, -1
        for i, row in enumerate(rows):
            if i in used:
                continue
            diff = abs(row["epoch"] - conn["first_data"])
            if diff < best_diff:
                best_diff, best_match, best_idx = diff, row, i
        if best_match and best_idx >= 0:
            used.add(best_idx)
            conn["request"] = best_match
        else:
            conn["request"] = None

    matched = sum(1 for _, v in connections.items() if v.get("request"))
    return connections, matched, len(rows)


def analyze_sticky():
    """Analyze A2 sticky/rotating from US server pcap + DB."""
    pcap = SERVERS["us"]["pcap"]
    db = SERVERS["us"]["db"]
    if not pcap.exists() or not db.exists():
        print("SKIP sticky: missing US pcap or DB")
        return []
    print("\n[A2: Sticky/Rotating — US server]")
    conns = extract_connections(pcap)
    conns, matched, total = match_sticky_to_db(conns, db)
    print(f"  Matched {matched}/{total} sticky requests")

    results = []
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
        results.append({
            "timestamp": req.get("epoch"),
            "server": "us",
            "client_ip": conn["client_ip"],
            "gap_ms": round(gap * 1000, 3),
            "tcp_rtt_ms": round(tcp_rtt * 1000, 3),
            "syn_ttl": conn["syn_ttl"],
            "syn_window": conn["syn_window"],
            "provider": req.get("provider", ""),
            "protocol": "http_connect",
            "country": "us",
            "session_mode": req.get("session_mode", ""),
            "ua_string": req.get("user_agent", ""),
        })
    print(f"  {len(results)} complete sticky flows")
    return results


STICKY_CSV = UNIFIED / "unified_sticky.csv"


def main():
    import sys
    mode = sys.argv[1] if len(sys.argv) > 1 else "all"

    all_results = []
    sticky_results = []

    if mode in ("all", "proxied"):
        for region, config in SERVERS.items():
            all_results.extend(analyze_server(region, config))
        print(f"\n=== Writing {OUT_CSV} ===")
        OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
        if all_results:
            with open(OUT_CSV, "w", newline="") as f:
                w = csv.DictWriter(f, fieldnames=list(all_results[0].keys()))
                w.writeheader()
                w.writerows(all_results)
        print(f"Proxied total: {len(all_results)} flows")

    if mode in ("all", "sticky"):
        sticky_results = analyze_sticky()
        print(f"\n=== Writing {STICKY_CSV} ===")
        if sticky_results:
            with open(STICKY_CSV, "w", newline="") as f:
                w = csv.DictWriter(f, fieldnames=list(sticky_results[0].keys()))
                w.writeheader()
                w.writerows(sticky_results)
        print(f"Sticky total: {len(sticky_results)} flows")


if __name__ == "__main__":
    main()
