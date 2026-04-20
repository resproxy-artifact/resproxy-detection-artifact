#!/usr/bin/env python3
"""
Multi-server timing analysis.
Analyzes pcap + DB from 4 server locations to show timing gap
is independent of server location.
"""

import json
import csv
import subprocess
import sqlite3
from collections import defaultdict
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"
ANALYSIS_DIR = DATA_DIR / "analysis"
GNUPLOT_DIR = ANALYSIS_DIR / "gnuplot"
DB_DIR = DATA_DIR / "db"
FIGURES_DIR = DATA_DIR / "figures"

EXPERIMENTS = {
    "soax": {
        "us": {
            "pcap": DATA_DIR / "captures" / "us" / "20260326_soax_multi.pcap",
            "db": DB_DIR / "us.db",
            "label": "US (Virginia)",
            "filter_epoch_min": 1774549000,
            "filter_provider": "soax",
        },
        "ap": {
            "pcap": DATA_DIR / "captures" / "ap" / "20260326_soax_multi.pcap",
            "db": DB_DIR / "ap_soax.db",
            "label": "AP (Tokyo)",
        },
        "eu": {
            "pcap": DATA_DIR / "captures" / "eu" / "20260326_soax_multi.pcap",
            "db": DB_DIR / "eu_soax.db",
            "label": "EU (Paris)",
        },
        "sa": {
            "pcap": DATA_DIR / "captures" / "sa" / "20260326_soax_multi.pcap",
            "db": DB_DIR / "sa_soax.db",
            "label": "SA (São Paulo)",
        },
    },
    "brightdata": {
        "us": {
            "pcap": DATA_DIR / "captures" / "us" / "20260326_bd_multi.pcap",
            "db": DB_DIR / "us.db",
            "label": "US (Virginia)",
            "filter_epoch_min": 1774562000,
            "filter_provider": "brightdata",
        },
        "ap": {
            "pcap": DATA_DIR / "captures" / "ap" / "20260326_bd_multi.pcap",
            "db": DB_DIR / "ap_bd.db",
            "label": "AP (Tokyo)",
        },
        "eu": {
            "pcap": DATA_DIR / "captures" / "eu" / "20260326_bd_multi.pcap",
            "db": DB_DIR / "eu_bd.db",
            "label": "EU (Paris)",
        },
        "sa": {
            "pcap": DATA_DIR / "captures" / "sa" / "20260326_bd_multi.pcap",
            "db": DB_DIR / "sa_bd.db",
            "label": "SA (São Paulo)",
        },
    },
    "iproyal": {
        "us": {
            "pcap": DATA_DIR / "captures" / "us" / "20260327_iproyal_multi.pcap",
            "db": DB_DIR / "us.db",
            "label": "US (Virginia)",
            "filter_provider": "iproyal",
            "filter_epoch_min": 1774620000,
        },
        "ap": {
            "pcap": DATA_DIR / "captures" / "ap" / "20260327_iproyal_multi.pcap",
            "db": DB_DIR / "ap_iproyal.db",
            "label": "AP (Tokyo)",
            "filter_provider": "iproyal",
        },
        "eu": {
            "pcap": DATA_DIR / "captures" / "eu" / "20260327_iproyal_multi.pcap",
            "db": DB_DIR / "eu_iproyal.db",
            "label": "EU (Paris)",
            "filter_provider": "iproyal",
        },
        "sa": {
            "pcap": DATA_DIR / "captures" / "sa" / "20260327_iproyal_multi.pcap",
            "db": DB_DIR / "sa_iproyal.db",
            "label": "SA (São Paulo)",
            "filter_provider": "iproyal",
        },
    },
    "brightdata_mobile": {
        "us": {
            "pcap": DATA_DIR / "captures" / "us" / "20260331_bd_mobile_isp_multi.pcap",
            "db": DB_DIR / "us.db",
            "label": "US (Virginia)",
            "filter_provider": "brightdata_mobile",
            "filter_epoch_min": 1774900000,
        },
        "ap": {
            "pcap": DATA_DIR / "captures" / "ap" / "20260331_bd_mobile_isp.pcap",
            "db": DB_DIR / "ap_bd_mobile_isp.db",
            "label": "AP (Tokyo)",
            "filter_provider": "brightdata_mobile",
        },
        "eu": {
            "pcap": DATA_DIR / "captures" / "eu" / "20260331_bd_mobile_isp.pcap",
            "db": DB_DIR / "eu_bd_mobile_isp.db",
            "label": "EU (Paris)",
            "filter_provider": "brightdata_mobile",
        },
        "sa": {
            "pcap": DATA_DIR / "captures" / "sa" / "20260331_bd_mobile_isp.pcap",
            "db": DB_DIR / "sa_bd_mobile_isp.db",
            "label": "SA (São Paulo)",
            "filter_provider": "brightdata_mobile",
        },
    },
    "brightdata_isp": {
        "us": {
            "pcap": DATA_DIR / "captures" / "us" / "20260331_bd_mobile_isp_multi.pcap",
            "db": DB_DIR / "us.db",
            "label": "US (Virginia)",
            "filter_provider": "brightdata_isp",
            "filter_epoch_min": 1774900000,
        },
        "ap": {
            "pcap": DATA_DIR / "captures" / "ap" / "20260331_bd_mobile_isp.pcap",
            "db": DB_DIR / "ap_bd_mobile_isp.db",
            "label": "AP (Tokyo)",
            "filter_provider": "brightdata_isp",
        },
        "eu": {
            "pcap": DATA_DIR / "captures" / "eu" / "20260331_bd_mobile_isp.pcap",
            "db": DB_DIR / "eu_bd_mobile_isp.db",
            "label": "EU (Paris)",
            "filter_provider": "brightdata_isp",
        },
        "sa": {
            "pcap": DATA_DIR / "captures" / "sa" / "20260331_bd_mobile_isp.pcap",
            "db": DB_DIR / "sa_bd_mobile_isp.db",
            "label": "SA (São Paulo)",
            "filter_provider": "brightdata_isp",
        },
    },
    "netnut": {
        "us": {
            "pcap": DATA_DIR / "captures" / "us" / "20260329_netnut_multi.pcap",
            "db": DB_DIR / "us.db",
            "label": "US (Virginia)",
            "filter_provider": "netnut",
            "filter_epoch_min": 1774790000,
        },
        "ap": {
            "pcap": DATA_DIR / "captures" / "ap" / "20260329_netnut_multi.pcap",
            "db": DB_DIR / "ap_netnut.db",
            "label": "AP (Tokyo)",
            "filter_provider": "netnut",
        },
        "eu": {
            "pcap": DATA_DIR / "captures" / "eu" / "20260329_netnut_multi.pcap",
            "db": DB_DIR / "eu_netnut.db",
            "label": "EU (Paris)",
            "filter_provider": "netnut",
        },
        "sa": {
            "pcap": DATA_DIR / "captures" / "sa" / "20260329_netnut_multi.pcap",
            "db": DB_DIR / "sa_netnut.db",
            "label": "SA (São Paulo)",
            "filter_provider": "netnut",
        },
    },
    "oxylabs": {
        "us": {
            "pcap": DATA_DIR / "captures" / "us" / "20260328_oxylabs_multi.pcap",
            "db": DB_DIR / "us.db",
            "label": "US (Virginia)",
            "filter_provider": "oxylabs",
            "filter_epoch_min": 1774734000,
        },
        "ap": {
            "pcap": DATA_DIR / "captures" / "ap" / "20260328_oxylabs_multi.pcap",
            "db": DB_DIR / "ap_oxylabs.db",
            "label": "AP (Tokyo)",
            "filter_provider": "oxylabs",
        },
        "eu": {
            "pcap": DATA_DIR / "captures" / "eu" / "20260328_oxylabs_multi.pcap",
            "db": DB_DIR / "eu_oxylabs.db",
            "label": "EU (Paris)",
            "filter_provider": "oxylabs",
        },
        "sa": {
            "pcap": DATA_DIR / "captures" / "sa" / "20260328_oxylabs_multi.pcap",
            "db": DB_DIR / "sa_oxylabs.db",
            "label": "SA (São Paulo)",
            "filter_provider": "oxylabs",
        },
    },
    "oxylabs_mobile": {
        "us": {
            "pcap": DATA_DIR / "captures" / "us" / "20260328_oxylabs_multi.pcap",
            "db": DB_DIR / "us.db",
            "label": "US (Virginia)",
            "filter_provider": "oxylabs_mobile",
            "filter_epoch_min": 1774734000,
        },
        "ap": {
            "pcap": DATA_DIR / "captures" / "ap" / "20260328_oxylabs_multi.pcap",
            "db": DB_DIR / "ap_oxylabs.db",
            "label": "AP (Tokyo)",
            "filter_provider": "oxylabs_mobile",
        },
        "eu": {
            "pcap": DATA_DIR / "captures" / "eu" / "20260328_oxylabs_multi.pcap",
            "db": DB_DIR / "eu_oxylabs.db",
            "label": "EU (Paris)",
            "filter_provider": "oxylabs_mobile",
        },
        "sa": {
            "pcap": DATA_DIR / "captures" / "sa" / "20260328_oxylabs_multi.pcap",
            "db": DB_DIR / "sa_oxylabs.db",
            "label": "SA (São Paulo)",
            "filter_provider": "oxylabs_mobile",
        },
    },
    "oxylabs_isp": {
        "us": {
            "pcap": DATA_DIR / "captures" / "us" / "20260328_oxylabs_multi.pcap",
            "db": DB_DIR / "us.db",
            "label": "US (Virginia)",
            "filter_provider": "oxylabs_isp",
            "filter_epoch_min": 1774734000,
        },
        "ap": {
            "pcap": DATA_DIR / "captures" / "ap" / "20260328_oxylabs_multi.pcap",
            "db": DB_DIR / "ap_oxylabs.db",
            "label": "AP (Tokyo)",
            "filter_provider": "oxylabs_isp",
        },
        "eu": {
            "pcap": DATA_DIR / "captures" / "eu" / "20260328_oxylabs_multi.pcap",
            "db": DB_DIR / "eu_oxylabs.db",
            "label": "EU (Paris)",
            "filter_provider": "oxylabs_isp",
        },
        "sa": {
            "pcap": DATA_DIR / "captures" / "sa" / "20260328_oxylabs_multi.pcap",
            "db": DB_DIR / "sa_oxylabs.db",
            "label": "SA (São Paulo)",
            "filter_provider": "oxylabs_isp",
        },
    },
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

        if is_c2s and (flags_int & 0x12) == 0x02:
            conn["syn"] = ts
            conn["client_ip"] = src_ip
            conn["syn_ttl"] = ttl
            conn["syn_window"] = window
        elif not is_c2s and (flags_int & 0x12) == 0x12:
            conn["syn_ack"] = ts
        elif is_c2s and (flags_int & 0x12) == 0x10:
            if conn["syn_ack"] and not conn["ack"]:
                conn["ack"] = ts
        if is_c2s and tcp_len > 0 and not conn["first_data"]:
            conn["first_data"] = ts

    return connections


def match_to_db(connections, db_path, epoch_min=0, provider_filter=None):
    """Match connections to DB requests by timestamp."""
    db = sqlite3.connect(str(db_path))
    db.row_factory = sqlite3.Row
    conditions = ["param_src IS NOT NULL"]
    if provider_filter:
        conditions.append(f"param_src='{provider_filter}'")
    if epoch_min:
        conditions.append(f"epoch > {epoch_min}")
    query = f"SELECT * FROM requests WHERE {' AND '.join(conditions)} ORDER BY epoch"
    rows = [dict(r) for r in db.execute(query).fetchall()]
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
    """Analyze one server's data."""
    pcap = config["pcap"]
    db = config["db"]
    label = config["label"]
    epoch_min = config.get("filter_epoch_min", 0)
    provider_filter = config.get("filter_provider", None)

    if not pcap.exists():
        print(f"  SKIP {region}: pcap not found ({pcap})")
        return []
    if not db.exists():
        print(f"  SKIP {region}: DB not found ({db})")
        return []

    print(f"\nProcessing {label} ({region})...")
    connections = extract_connections(pcap)
    connections, matched, total_db = match_to_db(connections, db, epoch_min, provider_filter)
    print(f"  Matched {matched}/{total_db} requests")

    results = []
    for conn_key, conn in connections.items():
        if not all([conn["syn"], conn["syn_ack"], conn["ack"], conn["first_data"]]):
            continue
        if not conn.get("request"):
            continue

        tcp_rtt = conn["ack"] - conn["syn_ack"]
        gap = conn["first_data"] - conn["ack"]

        if tcp_rtt < 0.001:  # filter local (< 1ms RTT)
            continue

        req = conn["request"]
        results.append({
            "server": region,
            "server_label": label,
            "client_ip": conn["client_ip"],
            "gap_ms": round(gap * 1000, 3),
            "tcp_rtt_ms": round(tcp_rtt * 1000, 3),
            "syn_ttl": conn["syn_ttl"],
            "syn_window": conn["syn_window"],
            "src": req.get("param_src", "unknown"),
            "proto": req.get("param_proto", "unknown"),
            "country": req.get("param_country", "unknown"),
        })

    return results


def main():
    import sys
    # Allow specifying provider(s) via CLI: python3 analyze_multiserver.py [soax|brightdata|all]
    provider_arg = sys.argv[1] if len(sys.argv) > 1 else "all"
    if provider_arg == "all":
        providers_to_run = list(EXPERIMENTS.keys())
    else:
        providers_to_run = [provider_arg]

    all_results = []
    for provider in providers_to_run:
        if provider not in EXPERIMENTS:
            print(f"Unknown provider: {provider}")
            continue
        print(f"\n{'#'*90}")
        print(f"# PROVIDER: {provider.upper()}")
        print(f"{'#'*90}")
        servers = EXPERIMENTS[provider]
        for region, config in servers.items():
            results = analyze_server(region, config)
            # Tag with provider
            for r in results:
                r["provider"] = provider
            all_results.extend(results)
            print(f"  {region}: {len(results)} connections analyzed")

    if not all_results:
        print("No results!")
        return

    # Write CSV
    out_csv = ANALYSIS_DIR / "multiserver_timing.csv"
    with open(out_csv, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(all_results[0].keys()))
        writer.writeheader()
        writer.writerows(all_results)
    print(f"\nResults: {out_csv} ({len(all_results)} connections)")

    # Summary table: server × protocol
    print(f"\n{'='*90}")
    print("MULTI-SERVER TIMING GAP COMPARISON")
    print(f"{'='*90}")

    print(f"\n{'Provider':<12} {'Server':<18} {'Proto':<15} {'N':>5} {'Mean':>8} {'Median':>8} {'P5':>8} {'P95':>8}")
    print("-" * 90)

    by_key = defaultdict(list)
    for r in all_results:
        by_key[(r.get("provider", "?"), r["server_label"], r["proto"])].append(r["gap_ms"])

    for key in sorted(by_key.keys()):
        gaps = sorted(by_key[key])
        n = len(gaps)
        mean = sum(gaps) / n
        median = gaps[n // 2]
        p5 = gaps[int(n * 0.05)]
        p95 = gaps[int(n * 0.95)]
        print(f"{key[0]:<12} {key[1]:<18} {key[2]:<15} {n:>5} {mean:>8.1f} {median:>8.1f} {p5:>8.1f} {p95:>8.1f}")

    # Summary: server × country (for geographic analysis)
    print(f"\n{'='*90}")
    print("GAP BY SERVER × COUNTRY (median, ms)")
    print(f"{'='*90}")

    countries = sorted(set(r["country"] for r in all_results if r["country"] != "unknown"))
    servers = sorted(set(r["server"] for r in all_results))

    # Build matrix
    matrix = defaultdict(lambda: defaultdict(list))
    for r in all_results:
        if r["country"] != "unknown":
            matrix[r["server"]][r["country"]].append(r["gap_ms"])

    header = f"{'Country':<8}" + "".join(f"{s:>12}" for s in servers)
    print(f"\n{header}")
    print("-" * (8 + 12 * len(servers)))

    for country in countries:
        row = f"{country:<8}"
        for server in servers:
            gaps = matrix[server].get(country, [])
            if gaps:
                median = sorted(gaps)[len(gaps) // 2]
                row += f"{median:>12.1f}"
            else:
                row += f"{'—':>12}"
        print(row)

    # Detection performance per server
    print(f"\n{'='*90}")
    print("DETECTION (threshold = 6ms)")
    print(f"{'='*90}")

    print(f"\n{'Provider':<12} {'Server':<20} {'N':>5} {'Gap>6ms':>10} {'Rate':>8}")
    print("-" * 60)

    by_ps = defaultdict(list)
    for r in all_results:
        by_ps[(r.get("provider", "?"), r["server_label"])].append(r["gap_ms"])

    for key in sorted(by_ps.keys()):
        gaps = by_ps[key]
        n = len(gaps)
        detected = sum(1 for g in gaps if g > 6.0)
        print(f"{key[0]:<12} {key[1]:<20} {n:>5} {detected:>5}/{n:<4} {detected/n*100:>6.1f}%")

    # Write CDF data per server
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)

    for server in servers:
        gaps = sorted([r["gap_ms"] for r in all_results if r["server"] == server])
        dat = GNUPLOT_DIR / f"cdf_multiserver_{server}.dat"
        with open(dat, "w") as f:
            for i, g in enumerate(gaps):
                f.write(f"{g} {(i + 1) / len(gaps):.6f}\n")

    # Generate gnuplot figure
    style = Path(__file__).parent.parent / "style.gnu"
    cdf_script = f"""load "{style}"
set terminal postscript eps enhanced color font "Helvetica,16" size 5.0,3.2
set output "{FIGURES_DIR}/timing_cdf_multiserver.eps"

set xlabel "TCP-to-TLS Gap (ms)" font "Helvetica,18"
set ylabel "CDF" font "Helvetica,18"
set key right bottom font "Helvetica,12" spacing 1.2

set xrange [0:500]
set yrange [0:1.05]
set xtics 100
set ytics 0.2

set arrow from 6,0 to 6,1.05 nohead lw 1.5 lc rgb "#888888" dt 2
set label "t = 6 ms" at 12,0.5 font "Helvetica,12" tc rgb "#888888"

plot "{GNUPLOT_DIR}/cdf_multiserver_us.dat" using 1:2 title "US (Virginia)" with lines lw 2.5 lc rgb "#2166ac", \\
     "{GNUPLOT_DIR}/cdf_multiserver_eu.dat" using 1:2 title "EU (Paris)" with lines lw 2.5 lc rgb "#b2182b", \\
     "{GNUPLOT_DIR}/cdf_multiserver_ap.dat" using 1:2 title "AP (Tokyo)" with lines lw 2.5 lc rgb "#1b7837", \\
     "{GNUPLOT_DIR}/cdf_multiserver_sa.dat" using 1:2 title "SA (São Paulo)" with lines lw 2.5 lc rgb "#762a83"
"""
    GNUPLOT_DIR.mkdir(parents=True, exist_ok=True)
    script_path = GNUPLOT_DIR / "plot_cdf_multiserver.gnu"
    script_path.write_text(cdf_script)

    import subprocess as sp
    r = sp.run(["gnuplot", str(script_path)], capture_output=True, text=True)
    if r.returncode == 0:
        print(f"\nCDF figure: {FIGURES_DIR}/timing_cdf_multiserver.eps")
        sp.run(["convert", "-density", "300",
                str(FIGURES_DIR / "timing_cdf_multiserver.eps"),
                str(FIGURES_DIR / "timing_cdf_multiserver.png")],
               capture_output=True)
    else:
        print(f"gnuplot error: {r.stderr[:200]}")


if __name__ == "__main__":
    main()
