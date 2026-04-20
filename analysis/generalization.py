#!/usr/bin/env python3
"""
Leave-one-X-out generalization analysis.
Uses existing multiserver_timing.csv (4,479+ connections).
Tests: leave-one-provider, leave-one-server, leave-one-country, threshold stability.
"""

import csv
from collections import defaultdict
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"
ANALYSIS_DIR = DATA_DIR / "analysis"


def load_data():
    """Load multiserver timing data + RIPE Atlas direct baseline."""
    import json

    # Proxy data
    proxy = []
    with open(ANALYSIS_DIR / "multiserver_timing.csv") as f:
        for row in csv.DictReader(f):
            row["gap_ms"] = float(row["gap_ms"])
            row["tcp_rtt_ms"] = float(row["tcp_rtt_ms"])
            proxy.append(row)

    # Direct baseline from main_evaluation
    direct = []
    if (ANALYSIS_DIR / "main_evaluation.csv").exists():
        with open(ANALYSIS_DIR / "main_evaluation.csv") as f:
            for row in csv.DictReader(f):
                if row.get("is_proxied") == "False" and "macos" not in row.get("os", ""):
                    row["gap_ms"] = float(row["gap"])
                    direct.append(row)

    # Fallback: RIPE Atlas from headtohead
    if not direct:
        ripe_dir = DATA_DIR / "ripe_atlas"
        ripe_ips = set()
        for p in ripe_dir.glob("msm_*.json"):
            data = json.loads(p.read_text())
            for d in data:
                if d.get("from"):
                    ripe_ips.add(d["from"])

        with open(ANALYSIS_DIR / "headtohead_clean.csv") as f:
            for row in csv.DictReader(f):
                if row.get("src_type") == "direct":
                    row["gap_ms"] = float(row["our_gap_ms"])
                    direct.append(row)

    return proxy, direct


def compute_metrics(proxy_gaps, direct_gaps, threshold):
    tp = sum(1 for g in proxy_gaps if g > threshold)
    fp = sum(1 for g in direct_gaps if g > threshold)
    fn = len(proxy_gaps) - tp
    tn = len(direct_gaps) - fp
    tpr = tp / len(proxy_gaps) if proxy_gaps else 0
    fpr = fp / len(direct_gaps) if direct_gaps else 0
    prec = tp / (tp + fp) if (tp + fp) else 0
    f1 = 2 * prec * tpr / (prec + tpr) if (prec + tpr) else 0

    # AUC
    roc = []
    for t in [i * 0.5 for i in range(-10, 2001)]:
        tp_t = sum(1 for g in proxy_gaps if g > t)
        fp_t = sum(1 for g in direct_gaps if g > t)
        roc.append((fp_t / len(direct_gaps), tp_t / len(proxy_gaps)))
    roc = sorted(set(roc))
    auc = sum((roc[i][0] - roc[i-1][0]) * (roc[i][1] + roc[i-1][1]) / 2
              for i in range(1, len(roc)))

    return {"tpr": tpr, "fpr": fpr, "prec": prec, "f1": f1, "auc": auc,
            "tp": tp, "fp": fp, "n_proxy": len(proxy_gaps), "n_direct": len(direct_gaps)}


def find_optimal_threshold(proxy_gaps, direct_gaps):
    best_j, best_t = -1, 6
    for t in [i * 0.5 for i in range(0, 100)]:
        tp = sum(1 for g in proxy_gaps if g > t)
        fp = sum(1 for g in direct_gaps if g > t)
        tpr = tp / len(proxy_gaps)
        fpr = fp / len(direct_gaps) if direct_gaps else 0
        j = tpr - fpr
        if j > best_j:
            best_j, best_t = j, t
    return best_t


def main():
    proxy, direct = load_data()
    direct_gaps = [r["gap_ms"] for r in direct]

    print(f"Data: {len(proxy)} proxy, {len(direct)} direct")

    # === 1. Leave-one-provider-out ===
    print(f"\n{'='*70}")
    print("LEAVE-ONE-PROVIDER-OUT")
    print(f"{'='*70}")
    print(f"{'Holdout':<12} {'Train thresh':>12} {'Test TPR':>10} {'Test FPR':>10} {'Test AUC':>10} {'Test F1':>8}")
    print("-" * 65)

    providers = sorted(set(r.get("provider", "?") for r in proxy))
    for holdout in providers:
        train = [r["gap_ms"] for r in proxy if r.get("provider") != holdout]
        test = [r["gap_ms"] for r in proxy if r.get("provider") == holdout]
        thresh = find_optimal_threshold(train, direct_gaps)
        m = compute_metrics(test, direct_gaps, thresh)
        print(f"{holdout:<12} {thresh:>12.1f} {m['tpr']:>9.1%} {m['fpr']:>9.1%} {m['auc']:>10.4f} {m['f1']:>8.4f}")

    # === 2. Leave-one-server-out ===
    print(f"\n{'='*70}")
    print("LEAVE-ONE-SERVER-OUT")
    print(f"{'='*70}")
    print(f"{'Holdout':<12} {'Train thresh':>12} {'Test TPR':>10} {'Test FPR':>10} {'Test AUC':>10} {'Test F1':>8}")
    print("-" * 65)

    servers = sorted(set(r.get("server", "?") for r in proxy))
    for holdout in servers:
        train = [r["gap_ms"] for r in proxy if r.get("server") != holdout]
        test = [r["gap_ms"] for r in proxy if r.get("server") == holdout]
        thresh = find_optimal_threshold(train, direct_gaps)
        m = compute_metrics(test, direct_gaps, thresh)
        print(f"{holdout:<12} {thresh:>12.1f} {m['tpr']:>9.1%} {m['fpr']:>9.1%} {m['auc']:>10.4f} {m['f1']:>8.4f}")

    # === 3. Leave-one-country-out (top 5 countries) ===
    print(f"\n{'='*70}")
    print("LEAVE-ONE-COUNTRY-OUT (top countries)")
    print(f"{'='*70}")
    print(f"{'Holdout':<12} {'Train thresh':>12} {'Test TPR':>10} {'Test N':>8} {'Test AUC':>10}")
    print("-" * 55)

    country_counts = defaultdict(int)
    for r in proxy:
        country_counts[r.get("country", "?")] += 1
    top_countries = [c for c, _ in sorted(country_counts.items(), key=lambda x: -x[1])[:10]]

    for holdout in top_countries:
        train = [r["gap_ms"] for r in proxy if r.get("country") != holdout]
        test = [r["gap_ms"] for r in proxy if r.get("country") == holdout]
        thresh = find_optimal_threshold(train, direct_gaps)
        m = compute_metrics(test, direct_gaps, thresh)
        print(f"{holdout:<12} {thresh:>12.1f} {m['tpr']:>9.1%} {len(test):>8} {m['auc']:>10.4f}")

    # === 4. Threshold sweep stability ===
    print(f"\n{'='*70}")
    print("THRESHOLD SWEEP STABILITY")
    print(f"{'='*70}")
    print(f"{'Threshold':>10} {'TPR':>8} {'FPR':>8} {'Precision':>10} {'F1':>8}")
    print("-" * 50)

    all_proxy_gaps = [r["gap_ms"] for r in proxy]
    for t in [2, 4, 5, 6, 7, 8, 10, 12, 15, 20, 30, 50]:
        m = compute_metrics(all_proxy_gaps, direct_gaps, t)
        print(f"{t:>10} {m['tpr']:>7.1%} {m['fpr']:>7.1%} {m['prec']:>9.1%} {m['f1']:>8.4f}")

    # === 5. Cross-day stability ===
    print(f"\n{'='*70}")
    print("CROSS-DAY STABILITY")
    print(f"{'='*70}")

    by_date = defaultdict(list)
    for r in proxy:
        # Extract date from syn_ts if available
        syn = float(r.get("syn_ts", 0)) if r.get("syn_ts") else 0
        if syn > 1774500000:  # valid epoch
            import datetime
            dt = datetime.datetime.fromtimestamp(syn, tz=datetime.timezone.utc)
            day = dt.strftime("%Y-%m-%d")
            by_date[day].append(r["gap_ms"])

    if len(by_date) >= 2:
        days = sorted(by_date.keys())
        print(f"Days found: {days}")
        for i, train_day in enumerate(days):
            for j, test_day in enumerate(days):
                if i == j:
                    continue
                thresh = find_optimal_threshold(by_date[train_day], direct_gaps)
                m = compute_metrics(by_date[test_day], direct_gaps, thresh)
                print(f"  Train={train_day} → Test={test_day}: thresh={thresh:.0f}ms, "
                      f"TPR={m['tpr']:.1%}, AUC={m['auc']:.4f}")
    else:
        print("  Not enough distinct days for cross-day split")


if __name__ == "__main__":
    main()
