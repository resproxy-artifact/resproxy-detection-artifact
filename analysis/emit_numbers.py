#!/usr/bin/env python3
"""
Emit every number the paper cites as a LaTeX macro, computed from the dataset.

The point is that no figure in the prose is typed by hand: \\OursTPR is defined
here or it does not appear. This is what stops the table and the text drifting
apart, which is a defect reviewers of the previous submission found.

  python3 scripts/emit_numbers.py > out/numbers.tex
  % in the paper preamble:  \\input{numbers}
"""
import json, statistics, sys
from collections import Counter, defaultdict

import numpy as np

DATASET = "out/dataset.jsonl"
T_OURS, T_BADPASS = 10.0, 50.0


def auc(pos, neg):
    if not len(pos) or not len(neg):
        return float("nan")
    y = np.r_[np.ones(len(pos)), np.zeros(len(neg))]
    s = np.r_[np.asarray(pos, float), np.asarray(neg, float)]
    o = np.argsort(-s, kind="mergesort")
    y = y[o]
    return float(np.trapezoid(np.r_[0, np.cumsum(y) / len(pos)],
                              np.r_[0, np.cumsum(1 - y) / len(neg)]))


def tpr_at_fpr(pos, neg, target):
    n = np.sort(np.asarray(neg, float))[::-1]
    k = int(np.floor(target * len(n)))
    thr = n[k] if k < len(n) else -np.inf
    return float(np.mean(np.asarray(pos, float) > thr))


def _roc(pos, neg):
    ps = np.asarray(pos, float); ns = np.asarray(neg, float)
    thr = np.unique(np.concatenate([ps, ns, [-np.inf, np.inf]]))
    pts = sorted({(float(np.mean(ns > t)), float(np.mean(ps > t))) for t in thr})
    return np.asarray(pts)


def pauc(pos, neg, fmax):
    """Normalised partial AUC = mean TPR over FPR in [0, fmax]."""
    pts = _roc(pos, neg)
    g = np.linspace(0, fmax, 5000)
    return float(np.trapezoid(np.interp(g, pts[:, 0], pts[:, 1]), g) / fmax)


def roc_cross_fpr(posA, negA, posB, negB, lo=0.0, hi=0.4):
    """FPR at which ROC_A and ROC_B cross (each ROC on its own negatives)."""
    a = _roc(posA, negA); b = _roc(posB, negB)
    g = np.linspace(lo, hi, 40001)
    d = np.interp(g, a[:, 0], a[:, 1]) - np.interp(g, b[:, 0], b[:, 1])
    fl = np.where(np.diff(np.sign(d)) != 0)[0]
    return float(g[fl[0]] * 100) if len(fl) else float("nan")


def main():
    rows = [json.loads(l) for l in open(DATASET)]
    out = []
    def m(name, val, fmt="{}"):
        out.append(f"\\newcommand{{\\{name}}}{{{fmt.format(val)}}}")

    byc = defaultdict(list)
    byf = defaultdict(list)
    for r in rows:
        byc[r["label_class"]].append(r)
        byf[r["label_family"]].append(r)

    pos = [r for r in byc["resproxy"] if r["label_family"] != "scope_brightdata"]
    neg = byc["direct"]
    m("NumConnections", f"{len(rows):,}".replace(",", "{,}"))
    m("NumProxied", f"{len(pos):,}".replace(",", "{,}"))
    m("NumDirect", len(neg))
    m("NumVPN", len(byc["vpn"]))
    m("NumBenignTunnel", len(byc["benign_tunnel"]))
    m("NumExitIPs", f"{len({r['client_ip'] for r in pos}):,}".replace(",", "{,}"))
    m("NumDirectHosts", len({r["client_ip"] for r in neg}))
    m("NumProviders", len({r["label_family"] for r in pos}))

    def gaps(rs):
        return [r["gap_ms"] for r in rs if r.get("gap_ms") is not None]
    def bps(rs):
        return [r["badpass_delta_ms"] for r in rs
                if r.get("badpass_delta_ms") is not None]

    og, ng = gaps(pos), gaps(neg)
    bg, nb = bps(pos), bps(neg)

    m("OursTPR", 100 * np.mean(np.asarray(og) > T_OURS), "{:.1f}")
    m("OursFPR", 100 * np.mean(np.asarray(ng) > T_OURS), "{:.1f}")
    m("OursAUC", auc(og, ng), "{:.3f}")
    m("BpTPR", 100 * np.mean(np.asarray(bg) > T_BADPASS), "{:.1f}")
    m("BpFPR", 100 * np.mean(np.asarray(nb) > T_BADPASS), "{:.1f}")
    m("BpAUC", auc(bg, nb), "{:.3f}")
    m("OursTPRatOne", 100 * tpr_at_fpr(og, ng, 0.01), "{:.1f}")
    m("BpTPRatOne", 100 * tpr_at_fpr(bg, nb, 0.01), "{:.1f}")

    # real-browser negatives only
    realneg = [r for r in rows if r["label_family"] in ("linux", "windows", "macos")]
    m("NumRealBrowserDirect", len(realneg))
    m("OursAUCreal", auc(og, gaps(realneg)), "{:.3f}")
    m("BpAUCreal", auc(bg, bps(realneg)), "{:.3f}")
    m("OursFPRreal", 100 * np.mean(np.asarray(gaps(realneg)) > T_OURS), "{:.1f}")

    # class-level behaviour
    for cls, nm in (("vpn", "VPN"), ("benign_tunnel", "BenignTunnel")):
        g = gaps(byc[cls])
        m(f"Det{nm}", 100 * np.mean(np.asarray(g) > T_OURS), "{:.1f}")
    for fam, nm in (("tor", "Tor"), ("squid", "Squid")):
        g = gaps(byf[fam])
        if g:
            m(f"Det{nm}", 100 * np.mean(np.asarray(g) > T_OURS), "{:.1f}")
            m(f"Num{nm}", len(g))

    # decision depth
    depth = []
    for r in pos:
        for i, (ts, d, l) in enumerate(r.get("pkts", []), 1):
            if d == 1 and l > 0:
                depth.append(i)
                break
    if depth:
        m("OursPktsMedian", int(np.median(depth)))
        m("OursPktsMean", float(np.mean(depth)), "{:.1f}")
    bpd = [r["idx_bp_anchor"] for r in pos if r.get("idx_bp_anchor")]
    if bpd:
        m("BpPktsMedian", int(np.median(bpd)))
        m("BpPktsMean", float(np.mean(bpd)), "{:.1f}")

    # coverage
    for nm, field in (("Ours", "gap_ms"), ("Bp", "badpass_delta_ms")):
        miss = sum(1 for r in rows if r.get(field) is None)
        m(f"{nm}Unscoreable", 100 * miss / len(rows), "{:.1f}")

    # disagreement
    both = [r for r in pos
            if r.get("gap_ms") is not None and r.get("badpass_delta_ms") is not None]
    o = np.asarray([r["gap_ms"] for r in both]) > T_OURS
    b = np.asarray([r["badpass_delta_ms"] for r in both]) > T_BADPASS
    m("DisagreeBoth", 100 * np.mean(o & b), "{:.1f}")
    m("DisagreeOurs", 100 * np.mean(o & ~b), "{:.1f}")
    m("DisagreeBp", 100 * np.mean(~o & b), "{:.1f}")
    m("DisagreeNeither", 100 * np.mean(~o & ~b), "{:.1f}")

    # PPV at base rates
    tpr = np.mean(np.asarray(og) > T_OURS)
    fpr = np.mean(np.asarray(ng) > T_OURS)
    for p, nm in ((0.8, "Eighty"), (0.1, "Ten"), (0.01, "One"), (0.005, "Half")):
        v = tpr * p / (tpr * p + fpr * (1 - p))
        m(f"PPVat{nm}", 100 * v, "{:.1f}")

    # ---- bytes-to-verdict (cumulative payload up to each method's anchor) ----
    def bytes_to(r, idx, server_only=False):
        pk = r.get("pkts")
        if not pk or not idx:
            return None
        sub = pk[:idx]
        return sum(p[2] for p in sub if (not server_only or p[1] == 0))
    ob = [bytes_to(r, r.get("idx_first_cdata")) for r in rows]
    bb = [bytes_to(r, r.get("idx_bp_anchor")) for r in rows]
    bbs = [bytes_to(r, r.get("idx_bp_anchor"), server_only=True) for r in rows]
    ob = [x for x in ob if x is not None]
    bb = [x for x in bb if x is not None]
    bbs = [x for x in bbs if x is not None]
    m("OursBytes", int(np.median(ob)))
    m("BpBytes", f"{int(np.median(bb)):,}".replace(",", "{,}"))
    m("BpServerBytes", f"{int(np.median(bbs)):,}".replace(",", "{,}"))

    # ---- threshold-free ranking with unscoreable positives charged as misses ----
    def auc_miss(field, thr_neg_field):
        # positives: score = signal, or -inf if unscoreable (never ranked above a negative)
        ps = [r.get(field) if r.get(field) is not None else -1e18 for r in pos]
        ns = [r.get(thr_neg_field) for r in neg if r.get(thr_neg_field) is not None]
        return auc(ps, ns)
    # unconditional operating-point TPR: unscoreable positives charged as misses
    m("OursTPRuncond", 100 * np.mean([(r.get("gap_ms") or 0) > T_OURS for r in pos]), "{:.1f}")
    m("BpTPRuncond", 100 * np.mean([(r.get("badpass_delta_ms") or 0) > T_BADPASS for r in pos]), "{:.1f}")
    m("OursAUCmiss", auc_miss("gap_ms", "gap_ms"), "{:.3f}")
    m("BpAUCmiss", auc_miss("badpass_delta_ms", "badpass_delta_ms"), "{:.3f}")

    # partial AUC over the operationally relevant low-FPR region, and the FPR
    # at which the two ROC curves cross (badpass's full-AUC lead lives above it)
    m("OursPaucOne", pauc(og, ng, 0.01), "{:.3f}")
    m("BpPaucOne", pauc(bg, nb, 0.01), "{:.3f}")
    m("RocCrossFpr", roc_cross_fpr(og, ng, bg, nb), "{:.1f}")

    # ---- fusion OR(gap>10 OR badpass>150), unscoreable arm = not flagged ----
    T_BP_FUSE = 150.0
    def fired(r):
        g = r.get("gap_ms"); b = r.get("badpass_delta_ms")
        return (g is not None and g > T_OURS) or (b is not None and b > T_BP_FUSE)
    def ours_fired_miss(r):
        g = r.get("gap_ms"); return g is not None and g > T_OURS
    fus_tpr = 100 * np.mean([fired(r) for r in pos])
    fus_fpr = 100 * np.mean([fired(r) for r in neg])
    ours_tpr_miss = 100 * np.mean([ours_fired_miss(r) for r in pos])
    m("FusionTPR", fus_tpr, "{:.1f}")
    m("FusionFPR", fus_fpr, "{:.2f}")
    m("FusionGain", fus_tpr - ours_tpr_miss, "{:.2f}")

    # ---- speculative-buffering evasion (seeded full-deployment simulation) ----
    # Replace every proxied gap with a draw from the benign (direct) gap
    # distribution; BADPASS's response-side interval is unchanged. 20 seeds.
    ng_arr = np.asarray(ng, float)
    ours_ev, fus_ev = [], []
    for seed in range(20):
        rng = np.random.default_rng(seed)
        gsim = rng.choice(ng_arr, size=len(pos), replace=True)
        ours_ev.append(np.mean(gsim > T_OURS))
        bfired = np.asarray([(r.get("badpass_delta_ms") or 0) > T_BP_FUSE for r in pos])
        fus_ev.append(np.mean((gsim > T_OURS) | bfired))
    m("OursTPREvaded", 100 * float(np.mean(ours_ev)), "{:.1f}")
    m("FusionTPREvaded", 100 * float(np.mean(fus_ev)), "{:.1f}")
    # controlled lab A/B: flag rate on the speculatively-buffered ("late") blocks
    lab = [r for r in rows if r.get("param_src") == "labproxy"]
    from collections import defaultdict as _dd
    byrelay = _dd(list)
    for r in lab:
        byrelay[r["client_ip"]].append(r)
    late_ours, late_bp = [], []
    for ip, v in byrelay.items():
        v = sorted(v, key=lambda r: r.get("first_ts") or 0)
        h = len(v) // 2
        early, late = v[:h], v[h:]
        # only relays with a detectable early (eager-connect) block, i.e. a real
        # relay RTT there is something to evade; excludes co-located relays.
        early_det = np.mean([(r.get("gap_ms") or 0) > T_OURS for r in early]) if early else 0
        if len(v) >= 100 and early_det >= 0.9:
            late_ours += [(r.get("gap_ms") or 0) > T_OURS for r in late]
            late_bp   += [(r.get("badpass_delta_ms") or 0) > T_BADPASS for r in late]
    if late_ours:
        m("OursEvadedLab", 100 * float(np.mean(late_ours)), "{:.0f}")
        m("BpEvadedLab", 100 * float(np.mean(late_bp)), "{:.0f}")

    print("% Generated by revision/analysis/scripts/emit_numbers.py -- do not edit.")
    print("\n".join(sorted(out)))


if __name__ == "__main__":
    main()
