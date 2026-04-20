#!/usr/bin/env python3
"""
Disagreement taxonomy: analyze cases where Our Method and BADPASS disagree.
Uses headtohead_clean.csv (5,225 connections).
"""

import csv
from collections import defaultdict, Counter
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"
ANALYSIS_DIR = DATA_DIR / "analysis"


def load_data():
    results = []
    with open(ANALYSIS_DIR / "headtohead_clean.csv") as f:
        for row in csv.DictReader(f):
            row["our_gap_ms"] = float(row["our_gap_ms"])
            row["our_detection"] = row["our_detection"] == "True"
            if row["badpass_delta_ms"] != "":
                row["badpass_delta_ms"] = float(row["badpass_delta_ms"])
                row["badpass_detection"] = row["badpass_detection"] == "True"
                row["has_badpass"] = True
            else:
                row["badpass_delta_ms"] = None
                row["badpass_detection"] = None
                row["has_badpass"] = False
            row["tcp_rtt_ms"] = float(row["tcp_rtt_ms"])
            results.append(row)
    return results


def classify(r):
    """Classify a connection into agreement/disagreement category."""
    if not r["has_badpass"]:
        return "badpass_na"
    if r["our_detection"] and r["badpass_detection"]:
        return "both_detect"
    elif r["our_detection"] and not r["badpass_detection"]:
        return "ours_only"
    elif not r["our_detection"] and r["badpass_detection"]:
        return "badpass_only"
    else:
        return "neither"


def analyze_group(entries, label):
    """Analyze a disagreement group."""
    print(f"\n--- {label} (N={len(entries)}) ---")
    if not entries:
        return

    gaps = [e["our_gap_ms"] for e in entries]
    rtts = [e["tcp_rtt_ms"] for e in entries]
    gaps_s = sorted(gaps)
    rtts_s = sorted(rtts)
    n = len(gaps)

    print(f"  Gap:  mean={sum(gaps)/n:.1f}ms  median={gaps_s[n//2]:.1f}ms  "
          f"min={gaps_s[0]:.1f}  max={gaps_s[-1]:.1f}")
    print(f"  RTT:  mean={sum(rtts)/n:.1f}ms  median={rtts_s[n//2]:.1f}ms")

    if entries[0].get("has_badpass") and entries[0]["badpass_delta_ms"] is not None:
        bps = sorted([e["badpass_delta_ms"] for e in entries if e["badpass_delta_ms"] is not None])
        if bps:
            print(f"  BP δ: mean={sum(bps)/len(bps):.1f}ms  median={bps[len(bps)//2]:.1f}ms")

    # TLS version distribution
    tls_dist = Counter(e.get("tls_version", "?") for e in entries)
    print(f"  TLS:  {dict(tls_dist)}")

    # Provider distribution
    prov_dist = Counter(e.get("provider", e.get("src_type", "?")) for e in entries)
    print(f"  Provider: {dict(prov_dist)}")

    # Country distribution (top 5)
    country_dist = Counter(e.get("country", "?") for e in entries)
    print(f"  Country (top 5): {dict(country_dist.most_common(5))}")

    # TTL distribution
    ttls = Counter(e.get("syn_ttl", "?") for e in entries)
    print(f"  TTL (top 5): {dict(ttls.most_common(5))}")


def deep_analysis_ours_only(entries):
    """Why did our method detect but BADPASS didn't?"""
    print(f"\n{'='*70}")
    print(f"DEEP ANALYSIS: OURS ONLY ({len(entries)} connections)")
    print(f"{'='*70}")
    print("These have gap > 6ms but BADPASS δRTT ≤ 50ms")
    print()

    # Gap vs BADPASS delta
    for e in sorted(entries, key=lambda x: x["our_gap_ms"])[:10]:
        bp = e["badpass_delta_ms"]
        print(f"  gap={e['our_gap_ms']:>8.1f}ms  bp_δ={bp:>8.1f}ms  "
              f"rtt={e['tcp_rtt_ms']:>8.1f}ms  tls={e.get('tls_version','?')}  "
              f"country={e.get('country','?')}")

    # Hypothesis: BADPASS δRTT close to 50ms threshold?
    bp_vals = sorted([e["badpass_delta_ms"] for e in entries if e["badpass_delta_ms"] is not None])
    if bp_vals:
        near_thresh = sum(1 for v in bp_vals if 30 <= v <= 50)
        low = sum(1 for v in bp_vals if v < 30)
        print(f"\n  BADPASS δRTT distribution:")
        print(f"    < 30ms: {low}/{len(bp_vals)} (BADPASS misses these)")
        print(f"    30-50ms: {near_thresh}/{len(bp_vals)} (near threshold)")
        print(f"    > 50ms: {sum(1 for v in bp_vals if v > 50)}/{len(bp_vals)}")


def deep_analysis_badpass_only(entries):
    """Why did BADPASS detect but our method didn't?"""
    print(f"\n{'='*70}")
    print(f"DEEP ANALYSIS: BADPASS ONLY ({len(entries)} connections)")
    print(f"{'='*70}")
    print("These have BADPASS δRTT > 50ms but gap ≤ 6ms")
    print()

    for e in sorted(entries, key=lambda x: x["our_gap_ms"]):
        bp = e["badpass_delta_ms"]
        print(f"  gap={e['our_gap_ms']:>8.1f}ms  bp_δ={bp:>8.1f}ms  "
              f"rtt={e['tcp_rtt_ms']:>8.1f}ms  tls={e.get('tls_version','?')}  "
              f"country={e.get('country','?')}")

    # Hypothesis: ACK and ClientHello arrived simultaneously (TCP coalescing)?
    zero_gap = sum(1 for e in entries if e["our_gap_ms"] < 1)
    print(f"\n  gap < 1ms (likely ACK+ClientHello coalesced): {zero_gap}/{len(entries)}")


def deep_analysis_neither(entries):
    """Why did both methods miss?"""
    print(f"\n{'='*70}")
    print(f"DEEP ANALYSIS: NEITHER ({len(entries)} connections)")
    print(f"{'='*70}")
    print("Both gap ≤ 6ms AND BADPASS δRTT ≤ 50ms, but these are proxied")
    print()

    for e in sorted(entries, key=lambda x: x["our_gap_ms"])[:15]:
        bp = e["badpass_delta_ms"] if e["badpass_delta_ms"] is not None else "N/A"
        bp_str = f"{bp:>8.1f}" if isinstance(bp, float) else f"{bp:>8}"
        print(f"  gap={e['our_gap_ms']:>8.1f}ms  bp_δ={bp_str}ms  "
              f"rtt={e['tcp_rtt_ms']:>8.1f}ms  tls={e.get('tls_version','?')}  "
              f"provider={e.get('provider','?')}  country={e.get('country','?')}")

    # Hypotheses
    zero_gap = sum(1 for e in entries if e["our_gap_ms"] < 1)
    low_rtt = sum(1 for e in entries if e["tcp_rtt_ms"] < 5)
    print(f"\n  gap < 1ms: {zero_gap}/{len(entries)} (ACK+data coalesced)")
    print(f"  RTT < 5ms: {low_rtt}/{len(entries)} (exit node near server)")


def main():
    data = load_data()

    # Separate proxy and direct
    proxy = [r for r in data if r.get("src_type") == "proxied"]
    direct = [r for r in data if r.get("src_type") == "direct"]

    print(f"Total: {len(data)} ({len(proxy)} proxied, {len(direct)} direct)")

    # Classify proxy connections
    categories = defaultdict(list)
    for r in proxy:
        cat = classify(r)
        categories[cat].append(r)

    print(f"\n{'='*70}")
    print("AGREEMENT/DISAGREEMENT SUMMARY (proxy connections)")
    print(f"{'='*70}")
    for cat in ["both_detect", "ours_only", "badpass_only", "neither", "badpass_na"]:
        n = len(categories[cat])
        pct = n / len(proxy) * 100
        print(f"  {cat:<20} {n:>6} ({pct:>5.1f}%)")

    # Group statistics
    for cat in ["both_detect", "ours_only", "badpass_only", "neither"]:
        analyze_group(categories[cat], cat)

    # Deep analysis of disagreements
    deep_analysis_ours_only(categories["ours_only"])
    deep_analysis_badpass_only(categories["badpass_only"])
    deep_analysis_neither(categories["neither"])

    # === Summary table for paper ===
    print(f"\n{'='*70}")
    print("PAPER TABLE: DISAGREEMENT TAXONOMY")
    print(f"{'='*70}")

    ours_only = categories["ours_only"]
    bp_only = categories["badpass_only"]
    neither = categories["neither"]

    print(f"\n{'Category':<20} {'N':>5} {'Primary Cause':<40} {'%':>6}")
    print("-" * 75)

    if ours_only:
        bp_vals = [e["badpass_delta_ms"] for e in ours_only if e["badpass_delta_ms"] is not None]
        low_bp = sum(1 for v in bp_vals if v < 30)
        print(f"{'Ours only':<20} {len(ours_only):>5} "
              f"{'BADPASS δRTT too low for threshold':40} {low_bp/len(ours_only)*100:>5.0f}%")

    if bp_only:
        zero = sum(1 for e in bp_only if e["our_gap_ms"] < 1)
        print(f"{'BADPASS only':<20} {len(bp_only):>5} "
              f"{'ACK+ClientHello coalesced (gap≈0)':40} {zero/len(bp_only)*100:>5.0f}%")

    if neither:
        zero = sum(1 for e in neither if e["our_gap_ms"] < 1)
        low_rtt = sum(1 for e in neither if e["tcp_rtt_ms"] < 5)
        print(f"{'Neither':<20} {len(neither):>5} "
              f"{'ACK+data coalesced or exit near server':40} {(zero+low_rtt)/len(neither)*100:>5.0f}%")


if __name__ == "__main__":
    main()
