#!/usr/bin/env python3
"""
Regression check: does the rebuilt dataset still reproduce the published
findings? Run after every pipeline change. Prints PASS/FAIL per expectation
with the observed value, so a silent extraction bug cannot slip through.

Expectations are the paper's own reported figures, with tolerances wide enough
to absorb the labelling differences between this pipeline and the original.
"""
import json, statistics, sys
from collections import defaultdict

DATASET = "out/dataset.jsonl"
T = 10.0   # our operating threshold, ms

# (description, family or class, metric, low, high)
EXPECT = [
    ("direct Linux FPR@10ms == 0%",        "fam:linux",    "det", 0.0, 0.02),
    ("direct Windows FPR@10ms == 0%",      "fam:windows",  "det", 0.0, 0.02),
    ("direct macOS FPR@10ms <= 4%",        "fam:macos",    "det", 0.0, 0.04),
    ("VPN FPR <= 2%",                      "cls:vpn",      "det", 0.0, 0.02),
    ("Squid (fwd proxy) FPR <= 5%",        "fam:squid",    "det", 0.0, 0.05),
    ("Tor detection >= 95%",               "fam:tor",      "det", 0.95, 1.0),
    ("resproxy detection 95-99.9%",        "cls:resproxy", "det", 0.95, 0.999),
    ("direct gap median < 5 ms",           "cls:direct",   "med", 0.0, 5.0),
    ("resproxy gap median > 100 ms",       "cls:resproxy", "med", 100.0, 1e9),
    ("BADPASS delta: direct median < 20ms", "cls:direct",  "bpmed", -5.0, 20.0),
    ("BADPASS delta: <2% negative (direct)", "cls:direct", "bpneg", 0.0, 0.02),
]


def main():
    rows = [json.loads(l) for l in open(DATASET)]
    byf, byc = defaultdict(list), defaultdict(list)
    for r in rows:
        byf[r["label_family"]].append(r)
        byc[r["label_class"]].append(r)

    def sel(spec):
        kind, key = spec.split(":", 1)
        return (byf if kind == "fam" else byc).get(key, [])

    ok = True
    for desc, spec, metric, lo, hi in EXPECT:
        rs = sel(spec)
        if not rs:
            print(f"  SKIP  {desc}  (no rows for {spec})")
            continue
        if metric == "det":
            g = [r["gap_ms"] for r in rs if r["gap_ms"] is not None]
            val = sum(1 for x in g if x > T) / len(g) if g else float("nan")
            shown = f"{val:.3%}"
        elif metric == "med":
            g = [r["gap_ms"] for r in rs if r["gap_ms"] is not None]
            val = statistics.median(g) if g else float("nan")
            shown = f"{val:.2f} ms"
        elif metric == "bpmed":
            d = [r["badpass_delta_ms"] for r in rs
                 if r["badpass_delta_ms"] is not None]
            val = statistics.median(d) if d else float("nan")
            shown = f"{val:.2f} ms"
        elif metric == "bpneg":
            d = [r["badpass_delta_ms"] for r in rs
                 if r["badpass_delta_ms"] is not None]
            val = sum(1 for x in d if x < 0) / len(d) if d else float("nan")
            shown = f"{val:.2%}"
        good = (val == val) and lo <= val <= hi
        ok &= good
        print(f"  {'PASS' if good else 'FAIL'}  {desc:38} = {shown:>12}"
              f"   (n={len(rs)})")

    print("\nSANITY:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
