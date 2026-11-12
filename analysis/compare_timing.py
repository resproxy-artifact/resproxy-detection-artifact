#!/usr/bin/env python3
"""
Head-to-head of the TRAINING-FREE timing detectors (ours vs BADPASS vs the
Casado & Freedman RTT variant) on identical connections.

Training-free is the point: our negative class contains only four distinct
client hosts, so any learned classifier can separate it by memorising those
hosts. Threshold statistics cannot, which makes them the only methods this
dataset can compare honestly.

Reports, for several evaluation slices:
  * threshold-free AUC
  * TPR at MATCHED false-positive rates (the fair operating comparison)
  * TPR/FPR at each method's own published threshold
  * disagreement taxonomy
  * coverage (a method that cannot score a connection is not scored on it)
"""
import json, sys
from collections import defaultdict, Counter

import numpy as np

DATASET = "out/dataset.jsonl"
METHODS = [
    ("ours",    "gap_ms",           10.0),
    ("badpass", "badpass_delta_ms", 50.0),
]


def auc(pos, neg):
    if len(pos) == 0 or len(neg) == 0:
        return float("nan")
    y = np.r_[np.ones(len(pos)), np.zeros(len(neg))]
    s = np.r_[np.asarray(pos, float), np.asarray(neg, float)]
    o = np.argsort(-s, kind="mergesort")
    y = y[o]
    tp = np.cumsum(y) / len(pos)
    fp = np.cumsum(1 - y) / len(neg)
    return float(np.trapezoid(np.r_[0, tp], np.r_[0, fp]))


def tpr_at_fpr(pos, neg, target):
    """Highest TPR achievable while keeping FPR <= target."""
    if len(pos) == 0 or len(neg) == 0:
        return float("nan"), float("nan")
    n = np.sort(np.asarray(neg, float))[::-1]
    k = int(np.floor(target * len(n)))
    thr = n[k] if k < len(n) else -np.inf   # smallest thr with FPR <= target
    return float(np.mean(np.asarray(pos, float) > thr)), float(thr)


def slice_rows(rows, pos_cls="resproxy", neg_sel=None):
    pos = [r for r in rows if r["label_class"] == pos_cls
           and r["label_family"] != "scope_brightdata"]
    neg = [r for r in rows if (neg_sel(r) if neg_sel else
                               r["label_class"] == "direct")]
    return pos, neg


def report(name, pos, neg):
    print(f"\n### {name}: {len(pos)} proxied vs {len(neg)} direct")
    print(f"{'method':10}{'cov+':>7}{'cov-':>7}{'AUC':>8}"
          f"{'TPR@FPR=1%':>12}{'TPR@FPR=0.5%':>14}{'own thr':>10}"
          f"{'TPR':>8}{'FPR':>8}")
    for mname, field, thr in METHODS:
        P = [r[field] for r in pos if r.get(field) is not None]
        N = [r[field] for r in neg if r.get(field) is not None]
        if not P or not N:
            print(f"{mname:10}  (not scoreable on this slice)")
            continue
        a = auc(P, N)
        t1, _ = tpr_at_fpr(P, N, 0.01)
        t5, _ = tpr_at_fpr(P, N, 0.005)
        TPR = float(np.mean(np.asarray(P) > thr))
        FPR = float(np.mean(np.asarray(N) > thr))
        print(f"{mname:10}{len(P)/len(pos):>7.1%}{len(N)/len(neg):>7.1%}"
              f"{a:>8.3f}{t1:>12.1%}{t5:>14.1%}{thr:>9.0f}m{TPR:>8.1%}{FPR:>8.1%}")


def main():
    rows = [json.loads(l) for l in open(DATASET)]

    # 1. everything
    pos, neg = slice_rows(rows)
    report("all proxied vs all direct", pos, neg)

    # 2. the strongest negatives we have: real browsers on real OSes
    real = lambda r: r["label_family"] in ("linux", "windows", "macos")
    report("real-browser directs only", pos, [r for r in rows if real(r)])

    # 3. only connections BOTH methods can score (apples to apples)
    both = lambda r: (r.get("gap_ms") is not None
                      and r.get("badpass_delta_ms") is not None)
    report("both methods scoreable",
           [r for r in pos if both(r)], [r for r in neg if both(r)])

    # 4. per provider
    print("\n### per provider (vs all direct), AUC / TPR at own threshold")
    print(f"{'provider':18}{'n':>7}{'ours AUC':>10}{'bp AUC':>9}"
          f"{'ours TPR':>10}{'bp TPR':>9}")
    fam = defaultdict(list)
    for r in pos:
        fam[r["label_family"]].append(r)
    for f in sorted(fam):
        P = fam[f]
        og = [r["gap_ms"] for r in P if r.get("gap_ms") is not None]
        bg = [r["badpass_delta_ms"] for r in P
              if r.get("badpass_delta_ms") is not None]
        ng = [r["gap_ms"] for r in neg if r.get("gap_ms") is not None]
        nb = [r["badpass_delta_ms"] for r in neg
              if r.get("badpass_delta_ms") is not None]
        print(f"{f:18}{len(P):>7}{auc(og,ng):>10.3f}{auc(bg,nb):>9.3f}"
              f"{np.mean(np.asarray(og)>10):>10.1%}"
              f"{np.mean(np.asarray(bg)>50):>9.1%}")

    # 5. disagreement taxonomy at the two native thresholds
    print("\n### disagreement on proxied connections (own thresholds)")
    both_rows = [r for r in pos if both(r)]
    o = np.asarray([r["gap_ms"] for r in both_rows]) > 10
    b = np.asarray([r["badpass_delta_ms"] for r in both_rows]) > 50
    n = len(both_rows)
    print(f"  both detect  {np.sum(o & b):6d}  {np.mean(o & b):6.1%}")
    print(f"  ours only    {np.sum(o & ~b):6d}  {np.mean(o & ~b):6.1%}")
    print(f"  BADPASS only {np.sum(~o & b):6d}  {np.mean(~o & b):6.1%}")
    print(f"  neither      {np.sum(~o & ~b):6d}  {np.mean(~o & ~b):6.1%}")
    miss = [r for r, ok in zip(both_rows, ~o) if ok]
    print("  families among our misses:",
          dict(Counter(r["label_family"] for r in miss).most_common(8)))

    # 6. coverage: where does each method have no anchor at all?
    print("\n### coverage over ALL labelled connections")
    for mname, field, _ in METHODS:
        miss = [r for r in rows if r.get(field) is None]
        print(f"  {mname:10} unscoreable {len(miss):6d} / {len(rows)} "
              f"({len(miss)/len(rows):.1%})  "
              f"{dict(Counter(r['label_class'] for r in miss).most_common(4))}")


if __name__ == "__main__":
    main()
