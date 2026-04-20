#!/usr/bin/env python3
"""
Lab proxy analysis: causal validation + evasion test.
Extracts timing from pcap, compares normal vs speculative vs direct.
"""

import csv
import json
import subprocess
import shutil
import sqlite3
from collections import defaultdict
from pathlib import Path
import glob

ROOT = Path(__file__).parent.parent
DATA_DIR = ROOT / "data"
ANALYSIS_DIR = DATA_DIR / "analysis"
GNUPLOT_DIR = ANALYSIS_DIR / "gnuplot"
DB_DIR = DATA_DIR / "db"
FIGURES_DIR = DATA_DIR / "figures"

# N=100 data
LABPROXY_N100_DIR = ROOT / "new-data" / "unified" / "labproxy_n100"
LABPROXY_N100_PCAP = LABPROXY_N100_DIR / "pcap_labproxy_n100.pcap"


def extract_connections(pcap_file):
    """Extract TCP timing from pcap. Uses tshark if available, else dpkt."""
    if shutil.which("tshark"):
        return _extract_tshark(pcap_file)
    else:
        return _extract_dpkt(pcap_file)


def _extract_tshark(pcap_file):
    """Extract via tshark."""
    cmd = [
        "tshark", "-r", str(pcap_file), "-T", "fields",
        "-e", "frame.time_epoch",
        "-e", "ip.src", "-e", "ip.dst",
        "-e", "tcp.srcport", "-e", "tcp.dstport",
        "-e", "tcp.flags", "-e", "tcp.len",
        "-Y", "tcp.port == 443",
        "-E", "separator=|",
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)

    connections = defaultdict(lambda: {
        "syn": None, "syn_ack": None, "ack": None, "first_data": None,
        "client_ip": None,
    })

    for line in result.stdout.strip().split("\n"):
        if not line.strip():
            continue
        fields = line.split("|")
        if len(fields) < 7:
            continue

        ts = float(fields[0])
        src_ip, dst_ip = fields[1], fields[2]
        src_port, dst_port = fields[3], fields[4]
        flags_str = fields[5]
        tcp_len = int(fields[6]) if fields[6] else 0

        if dst_port == "443":
            conn_key = f"{src_ip}:{src_port}->{dst_ip}:{dst_port}"
            is_c2s = True
        else:
            conn_key = f"{dst_ip}:{dst_port}->{src_ip}:{src_port}"
            is_c2s = False

        conn = connections[conn_key]
        flags_int = int(flags_str, 16) if flags_str.startswith("0x") else int(flags_str)

        if is_c2s and (flags_int & 0x12) == 0x02:
            conn["syn"] = ts
            conn["client_ip"] = src_ip
        elif not is_c2s and (flags_int & 0x12) == 0x12:
            conn["syn_ack"] = ts
        elif is_c2s and (flags_int & 0x12) == 0x10:
            if conn["syn_ack"] and not conn["ack"]:
                conn["ack"] = ts
        if is_c2s and tcp_len > 0 and not conn["first_data"]:
            conn["first_data"] = ts

    return connections


def _extract_dpkt(pcap_file):
    """Extract via dpkt (fallback when tshark unavailable)."""
    import dpkt
    import socket

    # Convert pcapng to pcap if needed
    pcap_path = str(pcap_file)
    converted = pcap_path + ".converted.pcap"
    with open(pcap_file, "rb") as f:
        magic = f.read(4)
    if magic == b"\x0a\x0d\x0d\x0a":  # pcapng magic
        import os
        if not os.path.exists(converted) or os.path.getmtime(converted) < os.path.getmtime(pcap_path):
            print(f"  Converting pcapng → pcap via tcpdump...")
            subprocess.run(["tcpdump", "-r", pcap_path, "-w", converted, "tcp port 443"],
                           capture_output=True)
        pcap_path = converted

    connections = defaultdict(lambda: {
        "syn": None, "syn_ack": None, "ack": None, "first_data": None,
        "client_ip": None,
    })

    with open(pcap_path, "rb") as f:
        pcap = dpkt.pcap.Reader(f)
        for ts, buf in pcap:
            try:
                eth = dpkt.ethernet.Ethernet(buf)
                if not isinstance(eth.data, dpkt.ip.IP):
                    continue
                ip = eth.data
                if not isinstance(ip.data, dpkt.tcp.TCP):
                    continue
                tcp = ip.data
            except (dpkt.NeedData, dpkt.UnpackError):
                continue

            src_ip = socket.inet_ntoa(ip.src)
            dst_ip = socket.inet_ntoa(ip.dst)
            src_port = tcp.sport
            dst_port = tcp.dport
            flags = tcp.flags
            payload_len = len(tcp.data)

            if src_port != 443 and dst_port != 443:
                continue

            if dst_port == 443:
                conn_key = f"{src_ip}:{src_port}->{dst_ip}:{dst_port}"
                is_c2s = True
            else:
                conn_key = f"{dst_ip}:{dst_port}->{src_ip}:{src_port}"
                is_c2s = False

            conn = connections[conn_key]

            if is_c2s and (flags & 0x12) == 0x02:  # SYN
                conn["syn"] = ts
                conn["client_ip"] = src_ip
            elif not is_c2s and (flags & 0x12) == 0x12:  # SYN-ACK
                conn["syn_ack"] = ts
            elif is_c2s and (flags & 0x12) == 0x10:  # ACK
                if conn["syn_ack"] and not conn["ack"]:
                    conn["ack"] = ts
            if is_c2s and payload_len > 0 and not conn["first_data"]:
                conn["first_data"] = ts

    return connections


def load_logs(log_dir):
    """Load experiment runner logs: timestamp_ms,variant,region,n,status,resp_time"""
    entries = []
    for log_file in sorted(log_dir.glob("*.log")):
        with open(log_file) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split(",")
                if len(parts) < 4:
                    continue
                entries.append({
                    "epoch": float(parts[0]) / 1000.0,  # ms → sec
                    "variant": parts[1],
                    "proxy_region": parts[2],
                })
    entries.sort(key=lambda x: x["epoch"])
    return entries


def match_to_logs(connections, log_entries):
    """Match pcap connections to log entries by timestamp."""
    used = set()
    sorted_conns = sorted(
        [(k, v) for k, v in connections.items() if v.get("first_data")],
        key=lambda x: x[1]["first_data"],
    )

    for conn_key, conn in sorted_conns:
        best_match, best_diff, best_idx = None, 10.0, -1
        for i, entry in enumerate(log_entries):
            if i in used:
                continue
            diff = abs(entry["epoch"] - conn["first_data"])
            if diff < best_diff:
                best_diff, best_match, best_idx = diff, entry, i
        if best_match and best_idx >= 0:
            used.add(best_idx)
            conn["request"] = best_match
        else:
            conn["request"] = None

    matched = sum(1 for _, v in connections.items() if v.get("request"))
    return connections, matched


def match_to_db(connections, db_path):
    db = sqlite3.connect(str(db_path))
    db.row_factory = sqlite3.Row
    rows = [dict(r) for r in db.execute(
        "SELECT * FROM requests WHERE param_src='labproxy' OR param_src='direct_lab' ORDER BY epoch"
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
    return connections, matched


def main():
    # Prefer N=100 pcap + log matching; fall back to old DB matching
    if LABPROXY_N100_PCAP.exists():
        print(f"Using N=100 data: {LABPROXY_N100_PCAP}")
        log_entries = load_logs(LABPROXY_N100_DIR)
        print(f"  Loaded {len(log_entries)} log entries")
        connections = extract_connections(LABPROXY_N100_PCAP)
        connections, matched = match_to_logs(connections, log_entries)
        print(f"  Matched: {matched}/{len(log_entries)}")

        all_results = []
        for conn_key, conn in connections.items():
            if not all([conn["syn"], conn["syn_ack"], conn["ack"], conn["first_data"]]):
                continue
            if not conn.get("request"):
                continue

            tcp_rtt = (conn["ack"] - conn["syn_ack"]) * 1000
            gap = (conn["first_data"] - conn["ack"]) * 1000

            req = conn["request"]
            all_results.append({
                "variant": req["variant"],
                "proxy_region": req["proxy_region"],
                "tcp_rtt_ms": round(tcp_rtt, 3),
                "gap_ms": round(gap, 3),
                "client_ip": conn["client_ip"],
            })
    else:
        print("N=100 pcap not found, falling back to old DB matching")
        pcap_files = sorted(glob.glob(str(DATA_DIR / "captures" / "us" / "*_labproxy.pcap")))
        db_path = DB_DIR / "us.db"

        all_results = []
        for pcap in pcap_files:
            print(f"Processing: {pcap}")
            connections = extract_connections(pcap)
            connections, matched = match_to_db(connections, db_path)
            print(f"  Matched: {matched}")

            for conn_key, conn in connections.items():
                if not all([conn["syn"], conn["syn_ack"], conn["ack"], conn["first_data"]]):
                    continue
                if not conn.get("request"):
                    continue

                tcp_rtt = (conn["ack"] - conn["syn_ack"]) * 1000
                gap = (conn["first_data"] - conn["ack"]) * 1000

                req = conn["request"]
                qs = req.get("query_string", "")
                params = dict(p.split("=", 1) for p in qs.split("&") if "=" in p)

                all_results.append({
                    "variant": params.get("variant", "unknown"),
                    "proxy_region": params.get("proxy_region", "unknown"),
                    "tcp_rtt_ms": round(tcp_rtt, 3),
                    "gap_ms": round(gap, 3),
                    "client_ip": conn["client_ip"],
                })

    if not all_results:
        print("No results!")
        return

    # Write CSV
    out_csv = ANALYSIS_DIR / "labproxy_results.csv"
    with open(out_csv, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(all_results[0].keys()))
        writer.writeheader()
        writer.writerows(all_results)
    print(f"\nResults: {out_csv} ({len(all_results)} connections)")

    # Summary
    print(f"\n{'='*70}")
    print("LAB PROXY RESULTS")
    print(f"{'='*70}")

    print(f"\n{'Variant':<15} {'Region':<10} {'N':>4} {'Mean Gap':>10} {'Med Gap':>10} {'TCP RTT':>10}")
    print("-" * 65)

    by_key = defaultdict(list)
    rtt_by_key = defaultdict(list)
    for r in all_results:
        by_key[(r["variant"], r["proxy_region"])].append(r["gap_ms"])
        rtt_by_key[(r["variant"], r["proxy_region"])].append(r["tcp_rtt_ms"])

    for key in sorted(by_key.keys()):
        gaps = sorted(by_key[key])
        rtts = sorted(rtt_by_key[key])
        n = len(gaps)
        mean = sum(gaps) / n
        median = gaps[n // 2]
        med_rtt = rtts[n // 2]
        print(f"{key[0]:<15} {key[1]:<10} {n:>4} {mean:>10.1f} {median:>10.1f} {med_rtt:>10.1f}")

    # Evasion comparison
    print(f"\n{'='*70}")
    print("EVASION: NORMAL vs SPECULATIVE")
    print(f"{'='*70}")

    print(f"\n{'Region':<10} {'Normal Gap':>12} {'Specul Gap':>12} {'Reduction':>12} {'Direct Gap':>12}")
    print("-" * 60)

    direct_gaps = by_key.get(("direct", "none"), [0])
    direct_med = sorted(direct_gaps)[len(direct_gaps) // 2] if direct_gaps else 0

    for region in ["us", "ap", "eu", "sa"]:
        normal = by_key.get(("normal", region), [])
        specul = by_key.get(("speculative", region), [])
        if normal and specul:
            n_med = sorted(normal)[len(normal) // 2]
            s_med = sorted(specul)[len(specul) // 2]
            reduction = n_med - s_med
            print(f"{region:<10} {n_med:>12.1f} {s_med:>12.1f} {reduction:>12.1f} {direct_med:>12.1f}")

    # Generate figures
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    style = Path(__file__).parent.parent / "style.gnu"

    # Write data for gnuplot
    # 1. Causal: gap vs region (boxplot data)
    for variant in ["direct", "normal", "speculative"]:
        for region in ["none", "us", "ap", "eu", "sa"]:
            gaps = by_key.get((variant, region), [])
            if gaps:
                dat = GNUPLOT_DIR / f"labproxy_{variant}_{region}.dat"
                with open(dat, "w") as f:
                    for g in sorted(gaps):
                        f.write(f"{g}\n")

    # 2. Gap vs RTT scatter (for linear regression)
    # Filter out pcap artifacts (negative RTT from duplicate interface capture)
    GNUPLOT_DIR.mkdir(parents=True, exist_ok=True)
    scatter_dat = GNUPLOT_DIR / "labproxy_gap_vs_rtt.dat"
    with open(scatter_dat, "w") as f:
        f.write("# tcp_rtt_ms gap_ms variant\n")
        for r in all_results:
            if r["variant"] == "normal" and r["tcp_rtt_ms"] >= 0:
                f.write(f"{r['tcp_rtt_ms']} {r['gap_ms']}\n")

    # Linear regression (exclude artifacts)
    normal_data = [(r["tcp_rtt_ms"], r["gap_ms"]) for r in all_results if r["variant"] == "normal" and r["tcp_rtt_ms"] >= 0]
    if normal_data:
        xs = [d[0] for d in normal_data]
        ys = [d[1] for d in normal_data]
        n = len(xs)
        mean_x = sum(xs) / n
        mean_y = sum(ys) / n
        ss_xy = sum((x - mean_x) * (y - mean_y) for x, y in zip(xs, ys))
        ss_xx = sum((x - mean_x) ** 2 for x in xs)
        slope = ss_xy / ss_xx if ss_xx > 0 else 0
        intercept = mean_y - slope * mean_x
        ss_res = sum((y - (slope * x + intercept)) ** 2 for x, y in zip(xs, ys))
        ss_tot = sum((y - mean_y) ** 2 for y in ys)
        r_squared = 1 - ss_res / ss_tot if ss_tot > 0 else 0

        print(f"\nLinear Regression (Normal proxy): gap = {slope:.2f} × RTT + {intercept:.1f}")
        print(f"R² = {r_squared:.4f}")

    # Gap vs RTT figure
    gap_rtt_script = f"""load "{style}"
set terminal postscript eps enhanced color font "Helvetica,16" size 4.5,3.5
set output "{FIGURES_DIR}/labproxy_gap_vs_rtt.eps"

set xlabel "TCP RTT to Proxy (ms)" font "Helvetica,18"
set ylabel "ACK→ClientHello Gap (ms)" font "Helvetica,18"
set key top left font "Helvetica,14"

f(x) = {slope:.4f} * x + {intercept:.4f}

plot "{scatter_dat}" using 1:2 title "Normal proxy" with points pt 7 ps 0.8 lc rgb "#2166ac", \\
     f(x) title sprintf("y = %.2fx + %.1f (R²=%.3f)", {slope:.4f}, {intercept:.4f}, {r_squared:.4f}) \\
        with lines lw 2 lc rgb "#b2182b" dt 2
"""
    script_path = GNUPLOT_DIR / "plot_labproxy_rtt.gnu"
    script_path.write_text(gap_rtt_script)

    # CDF: direct vs normal vs speculative
    cdf_script = f"""load "{style}"
set terminal postscript eps enhanced color font "Helvetica,16" size 4.5,3.0
set output "{FIGURES_DIR}/labproxy_evasion_cdf.eps"

set xlabel "ACK→ClientHello Gap (ms)" font "Helvetica,18"
set ylabel "CDF" font "Helvetica,18"
set key right bottom font "Helvetica,12"
set xrange [0:500]
set yrange [0:1.05]
"""
    # Write CDF data
    for label, variant, region_list in [
        ("direct", "direct", ["none"]),
        ("normal_all", "normal", ["us", "ap", "eu", "sa"]),
        ("speculative_all", "speculative", ["us", "ap", "eu", "sa"]),
    ]:
        gaps = []
        for region in region_list:
            gaps.extend(by_key.get((variant, region), []))
        gaps.sort()
        dat = GNUPLOT_DIR / f"labproxy_cdf_{label}.dat"
        n = len(gaps)
        with open(dat, "w") as f:
            for i, g in enumerate(gaps):
                f.write(f"{g} {(i + 1) / n:.6f}\n")

    cdf_script += f"""
plot "{GNUPLOT_DIR}/labproxy_cdf_direct.dat" using 1:2 \\
        title "Direct (no proxy)" with lines lw 2.5 lc rgb "#2166ac", \\
     "{GNUPLOT_DIR}/labproxy_cdf_normal_all.dat" using 1:2 \\
        title "Normal CONNECT proxy" with lines lw 2.5 lc rgb "#b2182b", \\
     "{GNUPLOT_DIR}/labproxy_cdf_speculative_all.dat" using 1:2 \\
        title "Speculative proxy (evasion)" with lines lw 2.5 lc rgb "#1b7837"
"""
    (GNUPLOT_DIR / "plot_labproxy_cdf.gnu").write_text(cdf_script)

    for name, script in [("Gap-vs-RTT", "plot_labproxy_rtt.gnu"), ("Evasion-CDF", "plot_labproxy_cdf.gnu")]:
        r = subprocess.run(["gnuplot", str(GNUPLOT_DIR / script)], capture_output=True, text=True)
        if r.returncode == 0:
            print(f"{name} figure generated")
            eps_name = script.replace("plot_", "").replace(".gnu", "")
            subprocess.run(["gs", "-dBATCH", "-dNOPAUSE", "-dEPSCrop",
                            "-sDEVICE=png16m", "-r300",
                            f"-sOutputFile={FIGURES_DIR / f'{eps_name}.png'}",
                            str(FIGURES_DIR / f"{eps_name}.eps")],
                           capture_output=True)
        else:
            print(f"{name} error: {r.stderr[:200]}")


if __name__ == "__main__":
    main()
