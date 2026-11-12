#!/usr/bin/env python3
"""
Does a threshold calibrated on one client population still hold on another?

This is the question an operator actually faces: they must pick a threshold
without having seen their own users' traffic. AUC does not answer it -- AUC is
threshold-free, so a statistic can rank well and still be uncalibratable.

For each method and each pair of direct populations (A, B):
  * choose the threshold on A that yields a target FPR
  * apply that threshold unchanged to B
  * report the FPR actually obtained on B, and the TPR it buys

A signal whose value is bounded by client-stack behaviour should transfer.
A signal that also contains the client's processing of the server flight
should not, because that term varies by population.
"""
import json, sys
from collections import defaultdict

import numpy as np

DATASET = "out/dataset.jsonl"
TARGET_FPR = 0.01

POPS = [
    ("browser/short", lambda r: (r.get("src_pcap") or "").startswith("20260327_browser_full")),
    ("browser/long",  lambda r: r["label_family"] in ("linux", "windows", "macos")),
    ("curl/short",    lambda r: (r.get("src_pcap") or "").startswith("unified")),
    ("curl/scope",    lambda r: (r.get("src_pcap") or "").startswith("20260328_scope")),
    ("curl/vpnrun",   lambda r: (r.get("src_pcap") or "").startswith("20260330_vpn")),
]
METHODS = [("ours", "gap_ms"), ("badpass", "badpass_delta_ms")]


def thr_for_fpr(neg, target):
    """Smallest threshold whose FPR on neg is <= target."""
    n = np.sort(np.asarray(neg, float))[::-1]
    k = int(np.floor(target * len(n)))
    return float(n[k]) if k < len(n) else float("-inf")


def main():
    rows = [json.loads(l) for l in open(DATASET)]
    direct = [r for r in rows if r["label_class"] == "direct"]
    pos = [r for r in rows if r["label_class"] == "resproxy"]

    pops = {}
    for name, f in POPS:
        v = [r for r in direct if f(r)]
        if v:
            pops[name] = v

    for mname, field in METHODS:
        P = [r[field] for r in pos if r.get(field) is not None]
        print(f"\n=== {mname}: threshold calibrated on ROW, applied to COLUMN "
              f"(target FPR {TARGET_FPR:.0%}) ===")
        names = list(pops)
        print(f"{'calibrate on':16}{'thr(ms)':>9}  " +
              "".join(f"{n:>15}" for n in names) + f"{'TPR':>8}")
        for a in names:
            na = [r[field] for r in pops[a] if r.get(field) is not None]
            if not na:
                continue
            t = thr_for_fpr(na, TARGET_FPR)
            cells = []
            for b in names:
                nb = [r[field] for r in pops[b] if r.get(field) is not None]
                fpr = float(np.mean(np.asarray(nb) > t)) if nb else float("nan")
                mark = "*" if a == b else " "
                cells.append(f"{fpr:>14.1%}{mark}")
            tpr = float(np.mean(np.asarray(P) > t))
            print(f"{a:16}{t:>9.2f}  " + "".join(cells) + f"{tpr:>8.1%}")

        # worst-case transfer: the number an operator is exposed to
        worst = 0.0
        for a in names:
            na = [r[field] for r in pops[a] if r.get(field) is not None]
            if not na:
                continue
            t = thr_for_fpr(na, TARGET_FPR)
            for b in names:
                if b == a:
                    continue
                nb = [r[field] for r in pops[b] if r.get(field) is not None]
                if nb:
                    worst = max(worst, float(np.mean(np.asarray(nb) > t)))
        print(f"  worst cross-population FPR: {worst:.1%}"
              f"   ({worst/TARGET_FPR:.0f}x the calibration target)")

    # and the published thresholds, which is what a reader would actually copy
    print("\n=== published thresholds applied to each population ===")
    print(f"{'population':16}{'n':>6}" +
          "".join(f"{m:>18}" for m, _ in METHODS))
    for name in pops:
        v = pops[name]
        cells = []
        for mname, field in METHODS:
            t = 10.0 if mname == "ours" else 50.0
            nb = [r[field] for r in v if r.get(field) is not None]
            cells.append(f"{np.mean(np.asarray(nb) > t):>17.1%}" if nb else f"{'-':>18}")
        print(f"{name:16}{len(v):>6}" + "".join(cells))


if __name__ == "__main__":
    main()
