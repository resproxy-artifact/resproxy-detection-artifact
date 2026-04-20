#!/usr/bin/env python3
"""
Analyze TCP-to-TLS timing gap from pcap files.

For each TCP connection on port 443:
1. Extract SYN, SYN-ACK, ACK, first data packet timestamps
2. Calculate TCP RTT = ACK.ts - SYN-ACK.ts
3. Calculate Gap = first_data.ts - ACK.ts
4. Calculate Gap Ratio = Gap / TCP RTT
5. Match to experiment metadata via query string in TLS data
"""

import json
import csv
import subprocess
import sys
import re
import sqlite3
from collections import defaultdict
from pathlib import Path
from urllib.parse import parse_qs, urlparse

DATA_DIR = Path(__file__).parent.parent / "data"
ANALYSIS_DIR = DATA_DIR / "analysis"
DB_DIR = DATA_DIR / "db"


def extract_connections_from_pcap(pcap_file):
    """Use tshark to extract TCP connection timing data."""
    # Step 1: Extract all SYN, SYN-ACK, ACK, and data packets
    cmd = [
        "tshark", "-r", str(pcap_file), "-T", "fields",
        "-e", "frame.time_epoch",
        "-e", "ip.src",
        "-e", "ip.dst",
        "-e", "tcp.srcport",
        "-e", "tcp.dstport",
        "-e", "tcp.flags",
        "-e", "tcp.len",
        "-e", "ip.ttl",
        "-e", "tcp.window_size_value",
        "-e", "tcp.options.mss_val",
        "-e", "tcp.option_kind",
        "-e", "tcp.window_size_scalefactor",
        "-Y", "tcp.port == 443",
        "-E", "separator=|",
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"tshark error: {result.stderr}")
        return {}

    connections = defaultdict(lambda: {
        "syn": None, "syn_ack": None, "ack": None, "first_data": None,
        "syn_ttl": None, "syn_window": None, "syn_mss": None,
        "syn_options": None, "syn_wscale": None,
        "client_ip": None, "server_ip": None,
    })

    for line in result.stdout.strip().split("\n"):
        if not line.strip():
            continue
        fields = line.split("|")
        if len(fields) < 12:
            continue

        ts = float(fields[0])
        src_ip = fields[1]
        dst_ip = fields[2]
        src_port = fields[3]
        dst_port = fields[4]
        flags = fields[5]
        tcp_len = int(fields[6]) if fields[6] else 0
        ttl = fields[7]
        window = fields[8]
        mss = fields[9]
        tcp_options = fields[10]
        wscale = fields[11]

        # Determine connection key (always client->server direction for key)
        if dst_port == "443":
            conn_key = f"{src_ip}:{src_port}->{dst_ip}:{dst_port}"
            is_client_to_server = True
        else:
            conn_key = f"{dst_ip}:{dst_port}->{src_ip}:{src_port}"
            is_client_to_server = False

        conn = connections[conn_key]

        flags_int = int(flags, 16) if flags.startswith("0x") else int(flags)

        # SYN (no ACK) from client
        if is_client_to_server and (flags_int & 0x12) == 0x02:
            conn["syn"] = ts
            conn["client_ip"] = src_ip
            conn["server_ip"] = dst_ip
            conn["syn_ttl"] = ttl
            conn["syn_window"] = window
            conn["syn_mss"] = mss
            conn["syn_options"] = tcp_options
            conn["syn_wscale"] = wscale

        # SYN-ACK from server
        elif not is_client_to_server and (flags_int & 0x12) == 0x12:
            conn["syn_ack"] = ts

        # ACK (completing handshake) from client - first ACK after SYN-ACK
        elif is_client_to_server and (flags_int & 0x12) == 0x10:
            if conn["syn_ack"] and not conn["ack"]:
                conn["ack"] = ts

        # First data packet from client (TLS ClientHello)
        if is_client_to_server and tcp_len > 0 and not conn["first_data"]:
            conn["first_data"] = ts

    return connections


def extract_query_strings_from_pcap(pcap_file):
    """Extract HTTP query strings from TLS-decrypted or SNI data."""
    # We'll match connections to requests via the SQLite DB instead
    return {}


def match_connections_to_requests(connections, db_path):
    """Match pcap connections to logged requests via timestamp proximity.

    Since nginx proxies to Flask on localhost, DB src_ip is always 127.0.0.1.
    Instead, we match by timestamp: each pcap connection's first_data timestamp
    should be close to the DB request's epoch (within a few seconds).
    We use a greedy nearest-match approach, consuming each DB row at most once.
    """
    if not Path(db_path).exists():
        print(f"DB not found: {db_path}")
        return connections

    db = sqlite3.connect(str(db_path))
    db.row_factory = sqlite3.Row
    rows = db.execute(
        "SELECT * FROM requests WHERE param_src IS NOT NULL ORDER BY epoch"
    ).fetchall()
    db.close()

    rows = [dict(r) for r in rows]
    used = set()

    # Sort connections by first_data timestamp
    sorted_conns = sorted(
        [(k, v) for k, v in connections.items() if v.get("first_data")],
        key=lambda x: x[1]["first_data"],
    )

    for conn_key, conn in sorted_conns:
        data_ts = conn["first_data"]
        best_match = None
        best_diff = 10.0  # max 10 second window
        best_idx = -1

        for i, row in enumerate(rows):
            if i in used:
                continue
            diff = abs(row["epoch"] - data_ts)
            if diff < best_diff:
                best_diff = diff
                best_match = row
                best_idx = i

        if best_match and best_idx >= 0:
            used.add(best_idx)
            conn["request"] = best_match
        else:
            conn["request"] = None

    matched = sum(1 for k, v in connections.items() if v.get("request"))
    print(f"  Matched {matched}/{len(rows)} requests to pcap connections")
    return connections


def analyze_connections(connections):
    """Calculate timing metrics for each connection."""
    results = []

    for conn_key, conn in connections.items():
        if not all([conn["syn"], conn["syn_ack"], conn["ack"], conn["first_data"]]):
            continue

        tcp_rtt = conn["ack"] - conn["syn_ack"]
        gap = conn["first_data"] - conn["ack"]
        gap_ratio = gap / tcp_rtt if tcp_rtt > 0 else float("inf")

        req = conn.get("request", {}) or {}

        results.append({
            "conn_key": conn_key,
            "client_ip": conn["client_ip"],
            "syn_ts": conn["syn"],
            "tcp_rtt_ms": round(tcp_rtt * 1000, 3),
            "gap_ms": round(gap * 1000, 3),
            "gap_ratio": round(gap_ratio, 3),
            "syn_ttl": conn["syn_ttl"],
            "syn_window": conn["syn_window"],
            "syn_mss": conn["syn_mss"],
            "syn_options": conn["syn_options"],
            "syn_wscale": conn["syn_wscale"],
            "src": req.get("param_src", "unknown"),
            "proto": req.get("param_proto", "unknown"),
            "country": req.get("param_country", "unknown"),
            "user_agent": req.get("user_agent", ""),
        })

    return results


def classify_timing(gap_ms, gap_ratio, threshold_ms=10.0, threshold_ratio=2.0):
    """Classify connection as proxied based on timing."""
    return gap_ms > threshold_ms and gap_ratio > threshold_ratio


def write_results(results, output_path):
    """Write analysis results to CSV."""
    if not results:
        print("No results to write.")
        return

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = list(results[0].keys()) + ["timing_flag"]
    with open(output_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in results:
            r["timing_flag"] = classify_timing(r["gap_ms"], r["gap_ratio"])
            writer.writerow(r)

    print(f"Results written to {output_path} ({len(results)} connections)")


def print_summary(results):
    """Print summary statistics."""
    if not results:
        print("No results to summarize.")
        return

    print("\n" + "=" * 80)
    print("TIMING GAP ANALYSIS SUMMARY")
    print("=" * 80)

    # Group by source
    by_source = defaultdict(list)
    for r in results:
        key = f"{r['src']}/{r['proto']}"
        by_source[key].append(r)

    print(f"\n{'Source/Proto':<30} {'Count':>6} {'Mean Gap(ms)':>12} {'Med Gap(ms)':>12} "
          f"{'Mean Ratio':>10} {'Detected':>8}")
    print("-" * 80)

    for key in sorted(by_source.keys()):
        entries = by_source[key]
        gaps = [e["gap_ms"] for e in entries]
        ratios = [e["gap_ratio"] for e in entries]
        detected = sum(1 for e in entries if classify_timing(e["gap_ms"], e["gap_ratio"]))

        mean_gap = sum(gaps) / len(gaps)
        sorted_gaps = sorted(gaps)
        median_gap = sorted_gaps[len(sorted_gaps) // 2]
        mean_ratio = sum(ratios) / len(ratios)

        print(f"{key:<30} {len(entries):>6} {mean_gap:>12.3f} {median_gap:>12.3f} "
              f"{mean_ratio:>10.3f} {detected:>5}/{len(entries)}")

    # Group by country
    print(f"\n{'Country':<10} {'Count':>6} {'Mean Gap(ms)':>12} {'Detected':>8}")
    print("-" * 40)
    by_country = defaultdict(list)
    for r in results:
        if r["country"] and r["country"] != "unknown":
            by_country[r["country"]].append(r)

    for country in sorted(by_country.keys(), key=lambda x: x or ""):
        entries = by_country[country]
        gaps = [e["gap_ms"] for e in entries]
        mean_gap = sum(gaps) / len(gaps)
        detected = sum(1 for e in entries if classify_timing(e["gap_ms"], e["gap_ratio"]))
        print(f"{country:<10} {len(entries):>6} {mean_gap:>12.3f} {detected:>5}/{len(entries)}")


if __name__ == "__main__":
    import glob

    capture_dir = DATA_DIR / "captures" / "us"
    db_path = DB_DIR / "us.db"

    pcap_files = sorted(glob.glob(str(capture_dir / "*.pcap")))
    if not pcap_files:
        print("No pcap files found in", capture_dir)
        sys.exit(1)

    all_results = []
    for pcap_file in pcap_files:
        print(f"\nProcessing: {pcap_file}")
        connections = extract_connections_from_pcap(pcap_file)
        connections = match_connections_to_requests(connections, db_path)
        results = analyze_connections(connections)
        all_results.extend(results)

    output_csv = ANALYSIS_DIR / "timing_analysis.csv"
    write_results(all_results, output_csv)
    print_summary(all_results)
