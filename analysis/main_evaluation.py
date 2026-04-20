#!/usr/bin/env python3
"""
Main evaluation table: Our Method vs BADPASS on real OS direct baseline.
Combines real direct (Windows/Linux/macOS × 4 servers × TLS 1.2/1.3)
with proxy data (BrightData/SOAX/IPRoyal) for apples-to-apples comparison.
"""

import subprocess
import sqlite3
import csv
import json
from collections import defaultdict
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"
ANALYSIS_DIR = DATA_DIR / "analysis"
FIGURES_DIR = DATA_DIR / "figures"
GNUPLOT_DIR = ANALYSIS_DIR / "gnuplot"
DB_DIR = DATA_DIR / "db"

# Direct baseline pcaps + DBs
DIRECT_CONFIGS = [
    # Virginia server
    {"pcap": DATA_DIR / "captures" / "us" / "20260328_real_direct.pcap",
     "db": DB_DIR / "us.db", "server": "us",
     "filter": "param_src LIKE 'direct_windows%' OR param_src LIKE 'direct_linux%'"},
    {"pcap": DATA_DIR / "captures" / "us" / "20260328_macos_retest.pcap",
     "db": DB_DIR / "us.db", "server": "us",
     "filter": "param_src = 'direct_macos_v2'"},
    # Remote servers
    {"pcap": DATA_DIR / "captures" / "ap" / "20260328_direct_region.pcap",
     "db": DB_DIR / "ap_direct.db", "server": "ap",
     "filter": "param_src LIKE 'direct_%'"},
    {"pcap": DATA_DIR / "captures" / "eu" / "20260328_direct_region.pcap",
     "db": DB_DIR / "eu_direct.db", "server": "eu",
     "filter": "param_src LIKE 'direct_%'"},
    {"pcap": DATA_DIR / "captures" / "sa" / "20260328_direct_region.pcap",
     "db": DB_DIR / "sa_direct.db", "server": "sa",
     "filter": "param_src LIKE 'direct_%'"},
]

# Proxy pcaps + DBs (reuse from multiserver experiment)
PROXY_CONFIGS = [
    {"pcap": DATA_DIR / "captures" / "us" / "20260326_soax_multi.pcap",
     "db": DB_DIR / "us.db", "server": "us", "provider": "soax",
     "filter": "param_src='soax'", "epoch_min": 1774549000},
    {"pcap": DATA_DIR / "captures" / "us" / "20260326_bd_multi.pcap",
     "db": DB_DIR / "us.db", "server": "us", "provider": "brightdata",
     "filter": "param_src='brightdata'", "epoch_min": 1774562000},
    {"pcap": DATA_DIR / "captures" / "us" / "20260327_iproyal_multi.pcap",
     "db": DB_DIR / "us.db", "server": "us", "provider": "iproyal",
     "filter": "param_src='iproyal'", "epoch_min": 1774620000},
]


def extract_connections(pcap_file):
    cmd = ['tshark', '-r', str(pcap_file), '-T', 'fields',
           '-e', 'frame.time_epoch', '-e', 'ip.src', '-e', 'ip.dst',
           '-e', 'tcp.srcport', '-e', 'tcp.dstport',
           '-e', 'tcp.flags', '-e', 'tcp.len', '-e', 'ip.ttl',
           '-e', 'tls.handshake.type', '-e', 'tls.record.content_type',
           '-e', 'frame.number',
           '-Y', 'tcp.port == 443', '-E', 'separator=|', '-E', 'occurrence=a']
    result = subprocess.run(cmd, capture_output=True, text=True)

    conns = defaultdict(lambda: {
        'syn': None, 'syn_ack': None, 'ack': None, 'data': None,
        'ip': None, 'ttl': None, 'syn_frame': None, 'data_frame': None,
        'shd': None, 'cke': None, 'slf': None, 'cccs': None, 'bp_frame': None,
    })

    for line in result.stdout.strip().split('\n'):
        if not line:
            continue
        f = line.split('|')
        if len(f) < 11:
            continue
        ts = float(f[0])
        src, dst, sp, dp = f[1], f[2], f[3], f[4]
        flags = int(f[5], 16) if f[5].startswith('0x') else int(f[5])
        tlen = int(f[6]) if f[6] else 0
        ttl, tls_hs, tls_ct = f[7], f[8], f[9]
        frame = int(f[10]) if f[10] else 0

        if dp == '443':
            key = f'{src}:{sp}'
            c2s = True
        else:
            key = f'{dst}:{dp}'
            c2s = False
        c = conns[key]

        if c2s and (flags & 0x12) == 0x02:
            c['syn'] = ts; c['ip'] = src; c['ttl'] = ttl; c['syn_frame'] = frame
        elif not c2s and (flags & 0x12) == 0x12:
            c['syn_ack'] = ts
        elif c2s and (flags & 0x12) == 0x10 and c['syn_ack'] and not c['ack'] and tlen == 0:
            c['ack'] = ts
        if c2s and tlen > 0 and not c['data']:
            c['data'] = ts; c['data_frame'] = frame

        if tls_hs:
            hs = tls_hs.split(',')
            if '14' in hs and not c2s:
                c['shd'] = ts
            if '16' in hs and c2s:
                c['cke'] = ts; c['bp_frame'] = frame
            if not c2s:
                c['slf'] = ts
        if tls_ct and c2s and '20' in tls_ct.split(',') and not c['cccs']:
            c['cccs'] = ts
            if not c['bp_frame']:
                c['bp_frame'] = frame

    return conns


def match_and_analyze(conns, db_path, sql_filter, epoch_min=0):
    db = sqlite3.connect(str(db_path))
    db.row_factory = sqlite3.Row
    where = sql_filter
    if epoch_min:
        where += f" AND epoch > {epoch_min}"
    rows = [dict(r) for r in db.execute(
        f"SELECT * FROM requests WHERE {where} ORDER BY epoch").fetchall()]
    db.close()

    used = set()
    results = []

    for key in sorted(conns.keys(), key=lambda k: conns[k].get('data') or 0):
        c = conns[key]
        if not all([c['syn'], c['syn_ack'], c['ack'], c['data']]):
            continue
        rtt = (c['ack'] - c['syn_ack']) * 1000
        gap = (c['data'] - c['ack']) * 1000
        our_pkts = (c['data_frame'] - c['syn_frame'] + 1) if c['syn_frame'] and c['data_frame'] else 4

        bp = None
        bp_pkts = None
        tls_ver = '?'
        if c['shd'] and c['cke']:
            bp = ((c['cke'] - c['shd']) - (c['ack'] - c['syn_ack'])) * 1000
            tls_ver = '1.2'
        elif c['slf'] and c['cccs']:
            bp = ((c['cccs'] - c['slf']) - (c['ack'] - c['syn_ack'])) * 1000
            tls_ver = '1.3'
        if c['bp_frame'] and c['syn_frame']:
            bp_pkts = c['bp_frame'] - c['syn_frame'] + 1

        best, best_diff, best_idx = None, 10.0, -1
        for i, row in enumerate(rows):
            if i in used:
                continue
            diff = abs(row['epoch'] - c['data'])
            if diff < best_diff:
                best, best_diff, best_idx = row, diff, i
        if best and best_idx >= 0:
            used.add(best_idx)
            qs = best.get('query_string', '')
            params = dict(p.split('=', 1) for p in qs.split('&') if '=' in p)

            try:
                t = int(c['ttl'])
                tcp_os = 'windows' if 100 < t <= 128 else 'linux'
            except:
                tcp_os = 'unknown'

            results.append({
                'gap': round(gap, 3),
                'rtt': round(rtt, 3),
                'bp_delta': round(bp, 3) if bp is not None else None,
                'tls_ver': tls_ver,
                'our_pkts': our_pkts,
                'bp_pkts': bp_pkts,
                'tcp_os': tcp_os,
                'ttl': c['ttl'],
                'os': params.get('src', '?').replace('direct_', '').replace('_v2', '').replace('_v3', ''),
                'tls_forced': params.get('tls', '?'),
                'server': params.get('server', 'us'),
                'provider': params.get('src', 'direct'),
            })

    return results


def compute_roc(positives, negatives, key, max_thresh=1000):
    roc = []
    for thresh in [i * 0.5 for i in range(-20, int(max_thresh * 2) + 1)]:
        tp = sum(1 for r in positives if r[key] is not None and r[key] > thresh)
        fp = sum(1 for r in negatives if r[key] is not None and r[key] > thresh)
        tpr = tp / len(positives) if positives else 0
        fpr = fp / len(negatives) if negatives else 0
        roc.append((fpr, tpr, thresh))
    roc_sorted = sorted(set((fpr, tpr) for fpr, tpr, _ in roc))
    auc = sum(
        (roc_sorted[i][0] - roc_sorted[i - 1][0]) * (roc_sorted[i][1] + roc_sorted[i - 1][1]) / 2
        for i in range(1, len(roc_sorted))
    )
    return roc, auc


def tpr_at_fpr(roc, target):
    best = 0
    for fpr, tpr, _ in roc:
        if fpr <= target:
            best = max(best, tpr)
    return best


def main():
    # Collect direct baseline
    print("=== DIRECT BASELINE ===")
    all_direct = []
    for cfg in DIRECT_CONFIGS:
        if not cfg['pcap'].exists():
            print(f"  SKIP: {cfg['pcap']}")
            continue
        print(f"  Processing: {cfg['pcap'].name} ({cfg['server']})")
        conns = extract_connections(cfg['pcap'])
        results = match_and_analyze(conns, cfg['db'], cfg['filter'])
        for r in results:
            r['is_proxied'] = False
        all_direct.extend(results)
        print(f"    Matched: {len(results)}")

    # Collect proxy data (US server only for fair comparison)
    print("\n=== PROXY DATA ===")
    all_proxy = []
    for cfg in PROXY_CONFIGS:
        if not cfg['pcap'].exists():
            print(f"  SKIP: {cfg['pcap']}")
            continue
        print(f"  Processing: {cfg['pcap'].name} ({cfg['provider']})")
        conns = extract_connections(cfg['pcap'])
        results = match_and_analyze(conns, cfg['db'], cfg['filter'], cfg.get('epoch_min', 0))
        for r in results:
            r['is_proxied'] = True
            r['provider'] = cfg['provider']
        all_proxy.extend(results)
        print(f"    Matched: {len(results)}")

    # Filter: remove RTT < 1ms (local)
    all_direct = [r for r in all_direct if r['rtt'] >= 0.5]

    print(f"\n=== DATASET ===")
    print(f"Direct: {len(all_direct)} (Windows: {sum(1 for r in all_direct if r['tcp_os']=='windows')}, "
          f"Linux: {sum(1 for r in all_direct if r['tcp_os']=='linux')})")
    print(f"Proxy:  {len(all_proxy)}")

    # Filter direct to Windows + Linux only (macOS has bimodal issue)
    direct_clean = [r for r in all_direct if 'macos' not in r['os']]
    direct_all = all_direct

    proxy_bp = [r for r in all_proxy if r['bp_delta'] is not None]
    direct_bp = [r for r in direct_clean if r['bp_delta'] is not None]

    # === MAIN TABLE ===
    print(f"\n{'='*70}")
    print("MAIN EVALUATION TABLE")
    print(f"{'='*70}")

    our_roc, our_auc = compute_roc(all_proxy, direct_clean, 'gap')
    bp_roc, bp_auc = compute_roc(proxy_bp, direct_bp, 'bp_delta')

    our_tpr_001 = tpr_at_fpr(our_roc, 0.01)
    our_tpr_005 = tpr_at_fpr(our_roc, 0.05)
    bp_tpr_001 = tpr_at_fpr(bp_roc, 0.01)
    bp_tpr_005 = tpr_at_fpr(bp_roc, 0.05)

    # At default thresholds
    for thresh_our, thresh_bp in [(6, 50), (10, 50)]:
        our_tp = sum(1 for r in all_proxy if r['gap'] > thresh_our)
        our_fp = sum(1 for r in direct_clean if r['gap'] > thresh_our)
        bp_tp = sum(1 for r in proxy_bp if r['bp_delta'] > thresh_bp)
        bp_fp = sum(1 for r in direct_bp if r['bp_delta'] > thresh_bp)

        our_tpr = our_tp / len(all_proxy)
        our_fpr = our_fp / len(direct_clean)
        our_prec = our_tp / (our_tp + our_fp) if (our_tp + our_fp) else 0
        our_f1 = 2 * our_prec * our_tpr / (our_prec + our_tpr) if (our_prec + our_tpr) else 0

        bp_tpr_v = bp_tp / len(proxy_bp) if proxy_bp else 0
        bp_fpr_v = bp_fp / len(direct_bp) if direct_bp else 0
        bp_prec = bp_tp / (bp_tp + bp_fp) if (bp_tp + bp_fp) else 0
        bp_f1 = 2 * bp_prec * bp_tpr_v / (bp_prec + bp_tpr_v) if (bp_prec + bp_tpr_v) else 0

        our_pkts = sorted([r['our_pkts'] for r in all_proxy if isinstance(r['our_pkts'], int)])
        bp_pkts = sorted([r['bp_pkts'] for r in proxy_bp if r['bp_pkts'] and r['bp_pkts'] > 0])

        print(f"\n--- Threshold: Our={thresh_our}ms, BADPASS=50ms ---")
        print(f"{'Metric':<30} {'Our Method':>15} {'BADPASS':>15}")
        print(f"{'─'*62}")
        print(f"{'N (proxy)':<30} {len(all_proxy):>15} {len(proxy_bp):>15}")
        print(f"{'N (direct, Win+Linux)':<30} {len(direct_clean):>15} {len(direct_bp):>15}")
        print(f"{'AUC':<30} {our_auc:>15.4f} {bp_auc:>15.4f}")
        print(f"{'TPR @ FPR=0.01':<30} {our_tpr_001:>14.1%} {bp_tpr_001:>14.1%}")
        print(f"{'TPR @ FPR=0.05':<30} {our_tpr_005:>14.1%} {bp_tpr_005:>14.1%}")
        print(f"{'TPR (default threshold)':<30} {our_tpr:>14.1%} {bp_tpr_v:>14.1%}")
        print(f"{'FPR (default threshold)':<30} {our_fpr:>14.1%} {bp_fpr_v:>14.1%}")
        print(f"{'Precision':<30} {our_prec:>14.1%} {bp_prec:>14.1%}")
        print(f"{'F1':<30} {our_f1:>15.4f} {bp_f1:>15.4f}")
        med_our = our_pkts[len(our_pkts) // 2] if our_pkts else 'N/A'
        med_bp = bp_pkts[len(bp_pkts) // 2] if bp_pkts else 'N/A'
        print(f"{'Packets (median)':<30} {str(med_our):>15} {str(med_bp):>15}")

    # === TLS VERSION ABLATION ===
    print(f"\n{'='*70}")
    print("TLS VERSION ABLATION (direct = Windows + Linux only)")
    print(f"{'='*70}")

    for tls_ver in ['1.2', '1.3']:
        d = [r for r in direct_clean if r['tls_forced'] == tls_ver]
        p12 = [r for r in all_proxy if r['tls_ver'] == tls_ver]
        if not d or not p12:
            continue
        d_bp = [r for r in d if r['bp_delta'] is not None]
        p_bp = [r for r in p12 if r['bp_delta'] is not None]

        o_roc, o_auc = compute_roc(p12, d, 'gap')
        b_roc, b_auc = compute_roc(p_bp, d_bp, 'bp_delta') if p_bp and d_bp else ([], 0)
        o_tpr = tpr_at_fpr(o_roc, 0.01)
        b_tpr = tpr_at_fpr(b_roc, 0.01) if b_roc else 0

        print(f"\nTLS {tls_ver}: Direct={len(d)}, Proxy={len(p12)}")
        print(f"  Our AUC={o_auc:.4f}  TPR@FPR=0.01={o_tpr:.1%}")
        print(f"  BP  AUC={b_auc:.4f}  TPR@FPR=0.01={b_tpr:.1%}")

    # === PER-OS BREAKDOWN ===
    print(f"\n{'='*70}")
    print("PER-OS FPR (at threshold Our=6ms / Our=10ms / BADPASS=50ms)")
    print(f"{'='*70}")
    print(f"{'OS':<12} {'N':>5} {'Our@6':>8} {'Our@10':>8} {'BP@50':>8}")
    print('-' * 45)
    for os_name in ['windows', 'linux', 'macos']:
        d = [r for r in all_direct if os_name in r['os']]
        if not d:
            continue
        fp6 = sum(1 for r in d if r['gap'] > 6)
        fp10 = sum(1 for r in d if r['gap'] > 10)
        d_bp = [r for r in d if r['bp_delta'] is not None]
        bp50 = sum(1 for r in d_bp if r['bp_delta'] > 50)
        print(f"{os_name:<12} {len(d):>5} {fp6:>5}/{len(d):<2} {fp10:>5}/{len(d):<2} {bp50:>5}/{len(d_bp):<2}")

    # Write CSV
    ANALYSIS_DIR.mkdir(parents=True, exist_ok=True)
    out = ANALYSIS_DIR / "main_evaluation.csv"
    all_data = all_direct + all_proxy
    with open(out, 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(all_data[0].keys()))
        w.writeheader()
        w.writerows(all_data)
    print(f"\nCSV: {out} ({len(all_data)} rows)")

    # Save summary
    summary = {
        "our_auc": round(our_auc, 4),
        "bp_auc": round(bp_auc, 4),
        "n_direct": len(direct_clean),
        "n_proxy": len(all_proxy),
    }
    (ANALYSIS_DIR / "main_evaluation_summary.json").write_text(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
