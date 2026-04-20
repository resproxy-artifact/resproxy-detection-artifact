#!/usr/bin/env python3
"""
BADPASS head-to-head comparison with CLEAN baseline.
Uses multi-server pcaps (4,479 proxied) + RIPE Atlas (993 direct probes).
This is the MAIN evaluation table for the paper.
"""

import csv
import json
import subprocess
import sqlite3
from collections import defaultdict
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"
ANALYSIS_DIR = DATA_DIR / "analysis"
GNUPLOT_DIR = ANALYSIS_DIR / "gnuplot"
DB_DIR = DATA_DIR / "db"
RIPE_DIR = DATA_DIR / "ripe_atlas"
FIGURES_DIR = DATA_DIR / "figures"

CF_PREFIXES = (
    "172.70.", "172.71.", "172.69.",
    "141.101.", "162.158.",
    "104.22.", "104.23.", "104.24.", "104.25.", "104.26.", "104.27.",
)

# All multi-server pcap+db pairs
PCAP_CONFIGS = [
    # Original pcap (contains RIPE Atlas 98 probes + initial BrightData)
    {"pcap": DATA_DIR / "captures" / "us" / "20260325_initial.pcap",
     "db": DB_DIR / "us.db", "region": "us", "has_ripe": True},
    # SOAX multi-server
    {"pcap": DATA_DIR / "captures" / "us" / "20260326_soax_multi.pcap",
     "db": DB_DIR / "us.db", "region": "us", "provider_filter": "soax",
     "epoch_min": 1774549000},
    {"pcap": DATA_DIR / "captures" / "ap" / "20260326_soax_multi.pcap",
     "db": DB_DIR / "ap_soax.db", "region": "ap"},
    {"pcap": DATA_DIR / "captures" / "eu" / "20260326_soax_multi.pcap",
     "db": DB_DIR / "eu_soax.db", "region": "eu"},
    {"pcap": DATA_DIR / "captures" / "sa" / "20260326_soax_multi.pcap",
     "db": DB_DIR / "sa_soax.db", "region": "sa"},
    # BrightData multi-server
    {"pcap": DATA_DIR / "captures" / "us" / "20260326_bd_multi.pcap",
     "db": DB_DIR / "us.db", "region": "us", "provider_filter": "brightdata",
     "epoch_min": 1774562000},
    {"pcap": DATA_DIR / "captures" / "ap" / "20260326_bd_multi.pcap",
     "db": DB_DIR / "ap_bd.db", "region": "ap"},
    {"pcap": DATA_DIR / "captures" / "eu" / "20260326_bd_multi.pcap",
     "db": DB_DIR / "eu_bd.db", "region": "eu"},
    {"pcap": DATA_DIR / "captures" / "sa" / "20260326_bd_multi.pcap",
     "db": DB_DIR / "sa_bd.db", "region": "sa"},
]

# RIPE Atlas probe IPs for direct baseline identification
RIPE_MEASUREMENTS = {
    "us": 160278701, "ap": 160278702, "eu": 160278703, "sa": 160278704,
}


def load_ripe_atlas_ips():
    """Load all RIPE Atlas probe public IPs."""
    all_ips = set()
    # 1000-probe measurements
    for region, msm_id in RIPE_MEASUREMENTS.items():
        path = RIPE_DIR / f"msm_{msm_id}_{region}.json"
        if path.exists():
            data = json.loads(path.read_text())
            for d in data:
                if d.get("from"):
                    all_ips.add(d["from"])
    # Original 98-probe measurement
    path = RIPE_DIR / "msm_160223370_98probes.json"
    if path.exists():
        data = json.loads(path.read_text())
        for d in data:
            if d.get("from"):
                all_ips.add(d["from"])
    return all_ips


def extract_connections(pcap_file):
    """Extract TCP + TLS timing from pcap."""
    cmd = [
        "tshark", "-r", str(pcap_file), "-T", "fields",
        "-e", "frame.time_epoch",
        "-e", "ip.src", "-e", "ip.dst",
        "-e", "tcp.srcport", "-e", "tcp.dstport",
        "-e", "tcp.flags", "-e", "tcp.len",
        "-e", "ip.ttl",
        "-e", "tls.handshake.type",
        "-e", "tls.record.content_type",
        "-e", "frame.number",
        "-Y", "tcp.port == 443",
        "-E", "separator=|", "-E", "occurrence=a",
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)

    connections = defaultdict(lambda: {
        "syn": None, "syn_ack": None, "ack": None, "first_data": None,
        "client_ip": None, "syn_ttl": None,
        "syn_frame": None, "first_data_frame": None,
        "server_hello_done_ts": None, "client_key_exchange_ts": None,
        "server_last_flight_ts": None, "client_ccs_ts": None,
        "badpass_p2_frame": None, "tls_version": None,
    })

    for line in result.stdout.strip().split("\n"):
        if not line.strip():
            continue
        fields = line.split("|")
        if len(fields) < 11:
            continue

        ts = float(fields[0])
        src_ip, dst_ip = fields[1], fields[2]
        src_port, dst_port = fields[3], fields[4]
        flags_str = fields[5]
        tcp_len = int(fields[6]) if fields[6] else 0
        ttl = fields[7]
        tls_hs_type = fields[8]
        tls_ct = fields[9]
        frame_num = int(fields[10]) if fields[10] else 0

        if dst_port == "443":
            conn_key = f"{src_ip}:{src_port}->{dst_ip}:{dst_port}"
            is_c2s = True
        else:
            conn_key = f"{dst_ip}:{dst_port}->{src_ip}:{src_port}"
            is_c2s = False

        conn = connections[conn_key]
        flags_int = int(flags_str, 16) if flags_str.startswith("0x") else int(flags_str)

        # TCP handshake
        if is_c2s and (flags_int & 0x12) == 0x02:
            conn["syn"] = ts
            conn["syn_frame"] = frame_num
            conn["client_ip"] = src_ip
            conn["syn_ttl"] = ttl
        elif not is_c2s and (flags_int & 0x12) == 0x12:
            conn["syn_ack"] = ts
        elif is_c2s and (flags_int & 0x12) == 0x10:
            if conn["syn_ack"] and not conn["ack"]:
                conn["ack"] = ts

        if is_c2s and tcp_len > 0 and not conn["first_data"]:
            conn["first_data"] = ts
            conn["first_data_frame"] = frame_num

        # TLS for BADPASS
        if tls_hs_type:
            hs_types = tls_hs_type.split(",")
            if "14" in hs_types and not is_c2s:
                conn["server_hello_done_ts"] = ts
                conn["tls_version"] = "1.2"
            if "16" in hs_types and is_c2s:
                conn["client_key_exchange_ts"] = ts
                conn["badpass_p2_frame"] = frame_num
            if not is_c2s and tls_hs_type:
                conn["server_last_flight_ts"] = ts

        if tls_ct and is_c2s:
            if "20" in tls_ct.split(",") and not conn["client_ccs_ts"]:
                conn["client_ccs_ts"] = ts
                if not conn["badpass_p2_frame"]:
                    conn["badpass_p2_frame"] = frame_num

    return connections


def match_to_db(connections, db_path, provider_filter=None, epoch_min=0):
    """Match connections to DB requests by timestamp."""
    if not Path(db_path).exists():
        return connections, 0

    db = sqlite3.connect(str(db_path))
    db.row_factory = sqlite3.Row
    conds = ["param_src IS NOT NULL"]
    if provider_filter:
        conds.append(f"param_src='{provider_filter}'")
    if epoch_min:
        conds.append(f"epoch > {epoch_min}")
    rows = [dict(r) for r in db.execute(
        f"SELECT * FROM requests WHERE {' AND '.join(conds)} ORDER BY epoch"
    ).fetchall()]
    db.close()

    used = set()
    for conn_key, conn in sorted(
        ((k, v) for k, v in connections.items() if v.get("first_data")),
        key=lambda x: x[1]["first_data"],
    ):
        best, best_diff, best_idx = None, 10.0, -1
        for i, row in enumerate(rows):
            if i in used:
                continue
            diff = abs(row["epoch"] - conn["first_data"])
            if diff < best_diff:
                best, best_diff, best_idx = row, diff, i
        if best and best_idx >= 0:
            used.add(best_idx)
            conn["request"] = best

    matched = sum(1 for v in connections.values() if v.get("request"))
    return connections, matched


def compute_badpass(conn):
    """Compute BADPASS δRTT."""
    tcp_rtt = conn["ack"] - conn["syn_ack"] if conn["ack"] and conn["syn_ack"] else None

    if conn["server_hello_done_ts"] and conn["client_key_exchange_ts"]:
        tls_rtt = conn["client_key_exchange_ts"] - conn["server_hello_done_ts"]
        ver = "1.2"
    elif conn["server_last_flight_ts"] and conn["client_ccs_ts"]:
        tls_rtt = conn["client_ccs_ts"] - conn["server_last_flight_ts"]
        ver = "1.3"
    else:
        return None, None, None

    if tcp_rtt and tcp_rtt > 0:
        delta = tls_rtt - tcp_rtt
        return round(tls_rtt * 1000, 3), round(delta * 1000, 3), ver
    return None, None, None


def process_all():
    """Process all pcap files and build unified dataset."""
    ripe_ips = load_ripe_atlas_ips()
    print(f"RIPE Atlas probe IPs: {len(ripe_ips)}")

    all_results = []

    for cfg in PCAP_CONFIGS:
        pcap = cfg["pcap"]
        if not pcap.exists():
            print(f"  SKIP: {pcap}")
            continue

        print(f"\nProcessing: {pcap.name} (region={cfg['region']})")
        connections = extract_connections(pcap)
        connections, matched = match_to_db(
            connections, cfg["db"],
            cfg.get("provider_filter"), cfg.get("epoch_min", 0),
        )
        print(f"  Matched {matched} proxy requests")

        # Count RIPE Atlas direct
        ripe_count = 0

        for conn_key, conn in connections.items():
            if not all([conn["syn"], conn["syn_ack"], conn["ack"], conn["first_data"]]):
                continue

            tcp_rtt_ms = round((conn["ack"] - conn["syn_ack"]) * 1000, 3)
            if tcp_rtt_ms < 1.0:
                continue
            if conn["client_ip"] and conn["client_ip"].startswith(CF_PREFIXES):
                continue

            our_gap_ms = round((conn["first_data"] - conn["ack"]) * 1000, 3)
            our_packets = (conn["first_data_frame"] - conn["syn_frame"] + 1) \
                if conn["syn_frame"] and conn["first_data_frame"] else 4

            tls_rtt_ms, badpass_delta_ms, tls_ver = compute_badpass(conn)
            bp_packets = (conn["badpass_p2_frame"] - conn["syn_frame"] + 1) \
                if conn.get("badpass_p2_frame") and conn["syn_frame"] else None

            req = conn.get("request")

            # Determine src_type
            if req and req.get("param_src") in ("brightdata", "soax"):
                src_type = "proxied"
                provider = req["param_src"]
                proto = req.get("param_proto", "unknown")
                country = req.get("param_country", "unknown")
            elif conn["client_ip"] in ripe_ips:
                src_type = "direct"
                provider = "ripe_atlas"
                proto = "direct_tls"
                country = ""
                ripe_count += 1
            else:
                continue  # unknown — skip

            all_results.append({
                "conn_key": conn_key,
                "client_ip": conn["client_ip"],
                "server_region": cfg["region"],
                "src_type": src_type,
                "provider": provider,
                "protocol": proto,
                "country": country,
                "tcp_rtt_ms": tcp_rtt_ms,
                "syn_ttl": conn["syn_ttl"],
                "our_gap_ms": our_gap_ms,
                "our_detection": our_gap_ms > 6.0,
                "our_packets": our_packets,
                "tls_version": tls_ver or "",
                "tls_rtt_ms": tls_rtt_ms if tls_rtt_ms is not None else "",
                "badpass_delta_ms": badpass_delta_ms if badpass_delta_ms is not None else "",
                "badpass_detection": badpass_delta_ms > 50.0 if badpass_delta_ms is not None else "",
                "badpass_packets": bp_packets or "",
            })

        print(f"  RIPE Atlas direct: {ripe_count}")

    return all_results


def compute_roc(positives, negatives, key):
    """Compute ROC points and AUC."""
    roc = []
    for thresh in [i * 0.5 for i in range(-20, 2001)]:
        tp = sum(1 for r in positives if r[key] != "" and float(r[key]) > thresh)
        fp = sum(1 for r in negatives if r[key] != "" and float(r[key]) > thresh)
        tpr = tp / len(positives) if positives else 0
        fpr = fp / len(negatives) if negatives else 0
        roc.append((fpr, tpr, thresh))

    roc_sorted = sorted(set((fpr, tpr) for fpr, tpr, _ in roc))
    auc = sum(
        (roc_sorted[i][0] - roc_sorted[i-1][0]) * (roc_sorted[i][1] + roc_sorted[i-1][1]) / 2
        for i in range(1, len(roc_sorted))
    )
    return roc, auc


def tpr_at_fpr(roc, target_fpr):
    """Find TPR at a specific FPR level."""
    best_tpr = 0
    for fpr, tpr, _ in roc:
        if fpr <= target_fpr:
            best_tpr = max(best_tpr, tpr)
    return best_tpr


def print_and_save(all_results):
    """Print summary and generate figures."""
    proxied = [r for r in all_results if r["src_type"] == "proxied"]
    direct = [r for r in all_results if r["src_type"] == "direct"]
    proxied_bp = [r for r in proxied if r["badpass_delta_ms"] != ""]
    direct_bp = [r for r in direct if r["badpass_delta_ms"] != ""]

    print(f"\n{'='*80}")
    print("HEAD-TO-HEAD: CLEAN BASELINE")
    print(f"{'='*80}")
    print(f"Proxied: {len(proxied)} ({len(proxied_bp)} with BADPASS)")
    print(f"Direct:  {len(direct)} ({len(direct_bp)} with BADPASS)")

    # Write CSV
    out_csv = ANALYSIS_DIR / "headtohead_clean.csv"
    with open(out_csv, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(all_results[0].keys()))
        w.writeheader()
        w.writerows(all_results)
    print(f"CSV: {out_csv}")

    # ROC
    our_roc, our_auc = compute_roc(proxied, direct, "our_gap_ms")
    bp_roc, bp_auc = compute_roc(proxied_bp, direct_bp, "badpass_delta_ms")

    # TPR at specific FPR
    our_tpr_001 = tpr_at_fpr(our_roc, 0.01)
    our_tpr_0001 = tpr_at_fpr(our_roc, 0.001)
    bp_tpr_001 = tpr_at_fpr(bp_roc, 0.01)
    bp_tpr_0001 = tpr_at_fpr(bp_roc, 0.001)

    # Detection at default thresholds
    our_tp = sum(1 for r in proxied if r["our_detection"])
    our_fp = sum(1 for r in direct if r["our_detection"])
    bp_tp = sum(1 for r in proxied_bp if r["badpass_detection"])
    bp_fp = sum(1 for r in direct_bp if r["badpass_detection"])

    our_tpr = our_tp / len(proxied)
    our_fpr = our_fp / len(direct)
    our_prec = our_tp / (our_tp + our_fp) if (our_tp + our_fp) > 0 else 0
    our_f1 = 2 * our_prec * our_tpr / (our_prec + our_tpr) if (our_prec + our_tpr) > 0 else 0

    bp_tpr_v = bp_tp / len(proxied_bp) if proxied_bp else 0
    bp_fpr_v = bp_fp / len(direct_bp) if direct_bp else 0
    bp_prec = bp_tp / (bp_tp + bp_fp) if (bp_tp + bp_fp) > 0 else 0
    bp_f1 = 2 * bp_prec * bp_tpr_v / (bp_prec + bp_tpr_v) if (bp_prec + bp_tpr_v) > 0 else 0

    our_pkts = sorted([r["our_packets"] for r in proxied if isinstance(r["our_packets"], int)])
    bp_pkts = sorted([r["badpass_packets"] for r in proxied_bp if isinstance(r["badpass_packets"], int) and r["badpass_packets"] > 0])

    # MAIN TABLE
    print(f"\n{'─'*70}")
    print(f"{'Metric':<30} {'Our Method':>18} {'BADPASS':>18}")
    print(f"{'─'*70}")
    print(f"{'Threshold':<30} {'6 ms':>18} {'50 ms':>18}")
    print(f"{'N (proxied)':<30} {len(proxied):>18} {len(proxied_bp):>18}")
    print(f"{'N (direct)':<30} {len(direct):>18} {len(direct_bp):>18}")
    print(f"{'AUC':<30} {our_auc:>18.4f} {bp_auc:>18.4f}")
    print(f"{'TPR @ FPR=0.01':<30} {our_tpr_001:>17.1%} {bp_tpr_001:>17.1%}")
    print(f"{'TPR @ FPR=0.001':<30} {our_tpr_0001:>17.1%} {bp_tpr_0001:>17.1%}")
    print(f"{'TPR (default threshold)':<30} {our_tpr:>17.1%} {bp_tpr_v:>17.1%}")
    print(f"{'FPR (default threshold)':<30} {our_fpr:>17.1%} {bp_fpr_v:>17.1%}")
    print(f"{'Precision':<30} {our_prec:>17.1%} {bp_prec:>17.1%}")
    print(f"{'F1 Score':<30} {our_f1:>18.4f} {bp_f1:>18.4f}")
    med_our = our_pkts[len(our_pkts)//2] if our_pkts else "N/A"
    med_bp = bp_pkts[len(bp_pkts)//2] if bp_pkts else "N/A"
    print(f"{'Packets needed (median)':<30} {str(med_our):>18} {str(med_bp):>18}")
    print(f"{'TLS version dependent':<30} {'No':>18} {'Yes':>18}")
    print(f"{'Requires TLS parsing':<30} {'No':>18} {'Yes':>18}")
    print(f"{'─'*70}")

    # Per-server
    print(f"\n--- Per-Server Breakdown ---")
    print(f"{'Server':<10} {'Method':<10} {'N_prox':>8} {'N_dir':>8} {'AUC':>8} {'TPR@.01':>10}")
    print("-" * 60)
    for region in sorted(set(r["server_region"] for r in all_results)):
        r_prox = [r for r in proxied if r["server_region"] == region]
        r_dir = [r for r in direct if r["server_region"] == region]
        if not r_prox or not r_dir:
            continue
        o_roc, o_auc = compute_roc(r_prox, r_dir, "our_gap_ms")
        o_tpr = tpr_at_fpr(o_roc, 0.01)
        r_prox_bp = [r for r in r_prox if r["badpass_delta_ms"] != ""]
        r_dir_bp = [r for r in r_dir if r["badpass_delta_ms"] != ""]
        if r_prox_bp and r_dir_bp:
            b_roc, b_auc = compute_roc(r_prox_bp, r_dir_bp, "badpass_delta_ms")
            b_tpr = tpr_at_fpr(b_roc, 0.01)
        else:
            b_auc, b_tpr = 0, 0
        print(f"{region:<10} {'Ours':<10} {len(r_prox):>8} {len(r_dir):>8} {o_auc:>8.3f} {o_tpr:>9.1%}")
        print(f"{'':<10} {'BADPASS':<10} {len(r_prox_bp):>8} {len(r_dir_bp):>8} {b_auc:>8.3f} {b_tpr:>9.1%}")

    # Per-provider
    print(f"\n--- Per-Provider ---")
    for prov in sorted(set(r["provider"] for r in proxied)):
        p_prox = [r for r in proxied if r["provider"] == prov]
        o_roc, o_auc = compute_roc(p_prox, direct, "our_gap_ms")
        p_bp = [r for r in p_prox if r["badpass_delta_ms"] != ""]
        b_roc, b_auc = compute_roc(p_bp, direct_bp, "badpass_delta_ms") if p_bp and direct_bp else ([], 0)
        print(f"{prov}: Ours AUC={o_auc:.3f}, BADPASS AUC={b_auc:.3f} (N={len(p_prox)})")

    # Agreement
    print(f"\n--- Agreement (N={len(proxied_bp)} proxied with both methods) ---")
    both = sum(1 for r in proxied_bp if r["our_detection"] and r["badpass_detection"])
    ours_only = sum(1 for r in proxied_bp if r["our_detection"] and not r["badpass_detection"])
    bp_only = sum(1 for r in proxied_bp if not r["our_detection"] and r["badpass_detection"])
    neither = sum(1 for r in proxied_bp if not r["our_detection"] and not r["badpass_detection"])
    print(f"Both detect:     {both}")
    print(f"Ours only:       {ours_only}")
    print(f"BADPASS only:    {bp_only}")
    print(f"Neither:         {neither}")

    # TLS version
    tls_versions = defaultdict(int)
    for r in all_results:
        if r["tls_version"]:
            tls_versions[r["tls_version"]] += 1
    print(f"\nTLS versions: {dict(tls_versions)}")

    # Generate figures
    generate_figures(proxied, direct, proxied_bp, direct_bp, our_roc, bp_roc, our_auc, bp_auc)

    # Save summary JSON
    summary = {
        "n_proxied": len(proxied), "n_direct": len(direct),
        "our_auc": round(our_auc, 4), "bp_auc": round(bp_auc, 4),
        "our_tpr": round(our_tpr, 4), "our_fpr": round(our_fpr, 4),
        "bp_tpr": round(bp_tpr_v, 4), "bp_fpr": round(bp_fpr_v, 4),
        "our_f1": round(our_f1, 4), "bp_f1": round(bp_f1, 4),
        "our_tpr_at_001": round(our_tpr_001, 4),
        "bp_tpr_at_001": round(bp_tpr_001, 4),
    }
    (ANALYSIS_DIR / "headtohead_clean_summary.json").write_text(json.dumps(summary, indent=2))


def generate_figures(proxied, direct, proxied_bp, direct_bp, our_roc, bp_roc, our_auc, bp_auc):
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    style = Path(__file__).parent.parent / "style.gnu"

    # Write ROC data
    for name, roc in [("our", our_roc), ("badpass", bp_roc)]:
        dat = GNUPLOT_DIR / f"roc_clean_{name}.dat"
        with open(dat, "w") as f:
            prev = (-1, -1)
            for fpr, tpr, _ in sorted(roc):
                if (fpr, tpr) != prev:
                    f.write(f"{fpr} {tpr}\n")
                    prev = (fpr, tpr)

    # ROC figure
    roc_script = f"""load "{style}"
set terminal postscript eps enhanced color font "Helvetica,16" size 3.5,3.5
set output "{FIGURES_DIR}/headtohead_clean_roc.eps"
set xlabel "False Positive Rate" font "Helvetica,18"
set ylabel "True Positive Rate" font "Helvetica,18"
set key right bottom font "Helvetica,14"
set xrange [0:1]
set yrange [0:1]
set size square
set xtics 0.2
set ytics 0.2
plot x title "" with lines lw 1 lc rgb "#bbbbbb" dt 2, \\
     "{GNUPLOT_DIR}/roc_clean_our.dat" using 1:2 title sprintf("Our Method (AUC=%.3f)", {our_auc}) with lines lw 2.5 lc rgb "#2166ac", \\
     "{GNUPLOT_DIR}/roc_clean_badpass.dat" using 1:2 title sprintf("BADPASS (AUC=%.3f)", {bp_auc}) with lines lw 2.5 lc rgb "#b2182b"
"""

    # Scatter
    GNUPLOT_DIR.mkdir(parents=True, exist_ok=True)
    scatter_dat = GNUPLOT_DIR / "headtohead_clean_scatter.dat"
    with open(scatter_dat, "w") as f:
        for r in proxied_bp + direct_bp:
            if r["badpass_delta_ms"] != "":
                label = 1 if r["src_type"] == "proxied" else 0
                f.write(f"{r['our_gap_ms']} {r['badpass_delta_ms']} {label}\n")

    scatter_script = f"""load "{style}"
set terminal postscript eps enhanced color font "Helvetica,16" size 4.0,4.0
set output "{FIGURES_DIR}/headtohead_clean_scatter.eps"
set xlabel "Our Method: Gap (ms)" font "Helvetica,18"
set ylabel "BADPASS: {{/Symbol d}}RTT (ms)" font "Helvetica,18"
set key top left font "Helvetica,14"
set xrange [-10:500]
set yrange [-50:500]
set arrow from 6,-50 to 6,500 nohead lw 1.5 lc rgb "#2166ac" dt 2
set arrow from -10,50 to 500,50 nohead lw 1.5 lc rgb "#b2182b" dt 2
plot "{scatter_dat}" using ($3==0 ? $1 : 1/0):($3==0 ? $2 : 1/0) title "Direct (RIPE Atlas)" with points pt 1 ps 0.5 lc rgb "#2166ac", \\
     "{scatter_dat}" using ($3==1 ? $1 : 1/0):($3==1 ? $2 : 1/0) title "Proxied" with points pt 2 ps 0.3 lc rgb "#b2182b"
"""

    # Packets CDF
    our_pkts = sorted([r["our_packets"] for r in proxied if isinstance(r["our_packets"], int)])
    bp_pkts = sorted([r["badpass_packets"] for r in proxied_bp if isinstance(r["badpass_packets"], int) and r["badpass_packets"] > 0])
    for name, pkts in [("our", our_pkts), ("badpass", bp_pkts)]:
        dat = GNUPLOT_DIR / f"packets_clean_{name}.dat"
        n = len(pkts)
        with open(dat, "w") as f:
            for i, p in enumerate(pkts):
                f.write(f"{p} {(i+1)/n:.6f}\n")

    pkt_script = f"""load "{style}"
set terminal postscript eps enhanced color font "Helvetica,16" size 4.5,3.0
set output "{FIGURES_DIR}/headtohead_clean_packets.eps"
set xlabel "Packets Observed Before Detection" font "Helvetica,18"
set ylabel "CDF" font "Helvetica,18"
set key right bottom font "Helvetica,14"
set xrange [0:30]
set yrange [0:1.05]
plot "{GNUPLOT_DIR}/packets_clean_our.dat" using 1:2 title "Our Method" with lines lw 2.5 lc rgb "#2166ac", \\
     "{GNUPLOT_DIR}/packets_clean_badpass.dat" using 1:2 title "BADPASS" with lines lw 2.5 lc rgb "#b2182b"
"""

    for name, script in [("ROC", roc_script), ("Scatter", scatter_script), ("Packets", pkt_script)]:
        path = GNUPLOT_DIR / f"plot_clean_{name.lower()}.gnu"
        path.write_text(script)
        r = subprocess.run(["gnuplot", str(path)], capture_output=True, text=True)
        if r.returncode == 0:
            print(f"{name} figure generated")
            eps = f"headtohead_clean_{name.lower()}"
            subprocess.run(["convert", "-density", "300",
                            str(FIGURES_DIR / f"{eps}.eps"),
                            str(FIGURES_DIR / f"{eps}.png")], capture_output=True)
        else:
            print(f"{name} error: {r.stderr[:200]}")


if __name__ == "__main__":
    results = process_all()
    print(f"\nTotal connections: {len(results)}")
    print_and_save(results)
