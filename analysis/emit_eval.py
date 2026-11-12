#!/usr/bin/env python3
"""Recompute every §7 evaluation number from the rebuilt dataset.

Companion to emit_numbers.py. This one drives the evaluation-section
reconciliation: detection rates per provider, server-independence,
leave-one-out AUC ranges, threshold sweep, per-OS FPR, scope boundaries,
the SOAX SOCKS5 bypass, protocol invariance, and coverage. Prints a report;
numbers here supersede the earlier figures.

  python3 scripts/emit_eval.py
"""
import json
from collections import defaultdict, Counter
import numpy as np

DATASET = "out/dataset.jsonl"
T = 10.0

COMMERCIAL = ["brightdata", "brightdata_mobile", "brightdata_isp", "soax",
              "oxylabs", "iproyal", "oxylabs_mobile", "oxylabs_isp", "netnut"]
ARCH = {"brightdata": "super", "soax": "super", "oxylabs": "super",
        "iproyal": "p2p", "brightdata_mobile": "mobile", "oxylabs_mobile": "mobile",
        "brightdata_isp": "isp", "oxylabs_isp": "isp", "netnut": "isp"}


def auc(pos, neg):
    pos = np.asarray([x for x in pos if x is not None], float)
    neg = np.asarray([x for x in neg if x is not None], float)
    if not len(pos) or not len(neg):
        return float("nan")
    y = np.r_[np.ones(len(pos)), np.zeros(len(neg))]
    s = np.r_[pos, neg]
    o = np.argsort(-s, kind="mergesort")
    y = y[o]
    return float(np.trapezoid(np.r_[0, np.cumsum(y)/len(pos)],
                              np.r_[0, np.cumsum(1-y)/len(neg)]))


def det(rs):
    g = [r["gap_ms"] for r in rs if r.get("gap_ms") is not None]
    return 100*np.mean(np.asarray(g) > T) if g else float("nan"), len(rs)


def med_gap(rs):
    g = [r["gap_ms"] for r in rs if r.get("gap_ms") is not None]
    return float(np.median(g)) if g else float("nan")


def main():
    rows = [json.loads(l) for l in open(DATASET)]
    byf = defaultdict(list)
    for r in rows:
        byf[r["label_family"]].append(r)
    pos = [r for r in rows if r["label_class"] == "resproxy" and r["label_family"] != "scope_brightdata"]
    neg = [r for r in rows if r["label_class"] == "direct"]
    negg = [r["gap_ms"] for r in neg]

    print("="*66)
    print("PER-PROVIDER DETECTION (9 commercial variants)")
    print(f"{'family':20}{'arch':7}{'n':>7}{'medgap':>8}{'det%':>7}{'AUC':>7}")
    dets = {}
    for f in COMMERCIAL:
        rs = byf[f]
        d, n = det(rs)
        a = auc([r["gap_ms"] for r in rs], negg)
        dets[f] = d
        print(f"{f:20}{ARCH[f]:7}{n:>7}{med_gap(rs):>8.1f}{d:>7.1f}{a:>7.3f}")
    dv = [dets[f] for f in COMMERCIAL]
    print(f"  per-variant det range: {min(dv):.1f}--{max(dv):.1f}%  | median {np.median(dv):.1f}%")

    # server independence (by server_ip, no region labels)
    print("\nSERVER-INDEPENDENCE (per server_ip, core unified.pcap only)")
    core = [r for r in pos if r.get("src_pcap") == "unified.pcap"]
    bysrv = defaultdict(list)
    for r in core:
        bysrv[r["server_ip"]].append(r)
    sdet = {ip: det(rs)[0] for ip, rs in bysrv.items()}
    for ip, d in sdet.items():
        print(f"  {ip:16} n={len(bysrv[ip]):6} det={d:.1f}%")
    print(f"  max inter-server spread: {max(sdet.values())-min(sdet.values()):.1f} pp")

    # arch gap ranges
    print("\nARCH MEDIAN-GAP RANGES")
    byarch = defaultdict(list)
    for f in COMMERCIAL:
        byarch[ARCH[f]].append(med_gap(byf[f]))
    for a, gs in byarch.items():
        print(f"  {a:7}: {min(gs):.0f}--{max(gs):.0f} ms")

    # gap heatmap span (per country-server-family cell, core)
    print("\nGAP/RTT HEATMAP (core unified cells)")
    cell = defaultdict(list)
    for r in core:
        cell[(r["label_family"], r.get("param_country"), r["server_ip"])].append(r)
    cellgap = [med_gap(v) for v in cell.values() if len(v) >= 5]
    cellrtt = [float(np.median([x["tcp_rtt_ms"] for x in v if x.get("tcp_rtt_ms") is not None]))
               for v in cell.values() if len(v) >= 5]
    cellgap = [g for g in cellgap if not np.isnan(g)]
    cellrtt = [g for g in cellrtt if not np.isnan(g)]
    print(f"  cells (n>=5): {len(cellgap)}")
    print(f"  gap span: {min(cellgap):.1f}--{max(cellgap):.1f} ms ({max(cellgap)/min(cellgap):.0f}x); "
          f"min cell = {min(cellgap)/T:.1f}x thr, max = {max(cellgap)/T:.0f}x")
    print(f"  RTT span: {min(cellrtt):.1f}--{max(cellrtt):.1f} ms ({max(cellrtt)/max(min(cellrtt),0.1):.0f}x)")
    above = sum(1 for g in cellgap if g > T)
    print(f"  cells above threshold: {above}/{len(cellgap)}")

    # leave-one-out AUC ranges (vs all 550 direct)
    print("\nLEAVE-ONE-OUT AUC (vs 550 direct)")
    fam_auc = {f: auc([r["gap_ms"] for r in byf[f]], negg) for f in COMMERCIAL}
    fam_det = {f: dets[f] for f in COMMERCIAL}
    print(f"  per-provider AUC: {min(fam_auc.values()):.3f}--{max(fam_auc.values()):.3f} "
          f"(floor {min(fam_auc, key=fam_auc.get)}); det {min(fam_det.values()):.1f}--{max(fam_det.values()):.1f}%")
    srv_auc = {ip: auc([r["gap_ms"] for r in bysrv[ip]], negg) for ip in bysrv}
    srv_det = {ip: det(bysrv[ip])[0] for ip in bysrv}
    print(f"  per-server AUC: {min(srv_auc.values()):.3f}--{max(srv_auc.values()):.3f}; "
          f"det {min(srv_det.values()):.1f}--{max(srv_det.values()):.1f}%")
    cty = defaultdict(list)
    for r in core:
        if r.get("param_country"):
            cty[r["param_country"]].append(r)
    cty_auc = {c: auc([r["gap_ms"] for r in cty[c]], negg) for c in cty}
    cty_det = {c: det(cty[c])[0] for c in cty}
    print(f"  per-country AUC ({len(cty)} cts): {min(cty_auc.values()):.3f}--{max(cty_auc.values()):.3f} "
          f"(floor {min(cty_auc, key=cty_auc.get)}); det {min(cty_det.values()):.1f}--{max(cty_det.values()):.1f}%")

    # threshold sweep
    print("\nTHRESHOLD SWEEP (unscoreable pos = miss)")
    npos = len(pos)
    og = np.asarray([r["gap_ms"] for r in pos if r.get("gap_ms") is not None], float)
    ng = np.asarray([x for x in negg if x is not None], float)
    for t in (6, 8, 10, 12, 15, 20):
        tp = int((og > t).sum()); fp = int((ng > t).sum())
        tpr = tp/npos; fpr = fp/len(ng); prec = tp/(tp+fp) if tp+fp else 0
        f1 = 2*prec*tpr/(prec+tpr) if prec+tpr else 0
        print(f"  t={t:2}  TPR {100*tpr:5.1f}%  FPR {100*fpr:5.2f}%  F1 {f1:.3f}")

    # per-OS FPR
    print("\nPER-OS FPR (direct baseline, N=50 each)")
    for os_ in ("linux", "windows", "macos"):
        rs = [r for r in neg if r["label_family"] == os_]
        d, n = det(rs)
        print(f"  {os_:8} n={n} FPR={d:.1f}% medgap={med_gap(rs):.2f}")

    # scope
    print("\nSCOPE BOUNDARIES")
    for name, sel in (("direct", lambda r: r["label_class"] == "direct"),
                      ("vpn", lambda r: r["label_class"] == "vpn"),
                      ("squid", lambda r: r["label_family"] == "squid"),
                      ("tor", lambda r: r["label_family"] == "tor")):
        rs = [r for r in rows if sel(r)]
        d, n = det(rs)
        print(f"  {name:8} n={n} flag={d:.1f}% medgap={med_gap(rs):.2f}")

    # SOAX bypass
    print("\nSOAX HTTP vs SOCKS5")
    for proto in ("http_connect", "socks5"):
        rs = [r for r in byf["soax"] if r.get("param_proto") == proto]
        d, n = det(rs)
        print(f"  soax {proto:13} n={n} det={d:.1f}%")
    print("  SOAX SOCKS5 per-country (low ones):")
    s5 = [r for r in byf["soax"] if r.get("param_proto") == "socks5"]
    bycty = defaultdict(list)
    for r in s5:
        bycty[r.get("param_country")].append(r)
    for c in sorted(bycty, key=lambda c: det(bycty[c])[0]):
        d, n = det(bycty[c])
        if d < 95:
            print(f"    {c}: {d:.1f}% (n={n})")

    # protocol invariance
    print("\nPROTOCOL INVARIANCE (families with both protocols)")
    for f in COMMERCIAL:
        h = [r for r in byf[f] if r.get("param_proto") == "http_connect"]
        s = [r for r in byf[f] if r.get("param_proto") == "socks5"]
        if h and s:
            print(f"  {f:18} HC {det(h)[0]:.1f}%  S5 {det(s)[0]:.1f}%  d={abs(det(h)[0]-det(s)[0]):.1f}")

    # coverage
    unscor = sum(1 for r in rows if r.get("gap_ms") is None)
    print(f"\nCOVERAGE: unscoreable {unscor}/{len(rows)} = {100*unscor/len(rows):.1f}%")


if __name__ == "__main__":
    main()
