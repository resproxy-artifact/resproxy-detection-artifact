#!/usr/bin/env python3
"""
method_beyondrtt_ta.py -- LIGHTWEIGHT tier of

  Ali, Yoosuf, Rabhi, Al-Sabah, Yun,
  "Beyond RTT: An Adversarially Robust Two-Tiered Approach for Residential
   Proxy Detection", NDSS 2026.

WHAT THIS IMPLEMENTS
--------------------
Their *lightweight* tier: a tree-ensemble classifier (they use gradient
boosting / random forest) over the FIRST 20 PACKETS of a flow, built from

  (a) connection-level statistics
        - inter-connection gaps (spacing of successive connections from the
          same client IP)
        - cross-layer RTT (TCP-handshake RTT vs. TLS-layer RTT, i.e. the
          BADPASS-style delta)
        - mean / median / mode of sent volume and of received volume
        - whole-connection duration
  (b) k-fingerprinting-style traffic-analysis features (Hayes & Danezis,
      USENIX Sec 2016), i.e. per-direction packet counts, size statistics,
      burst structure, packet ordering, and timing statistics.

This is the tier that is deployable at a CONTENT PROVIDER, which is their RQ3
setting and the only setting our vantage point supports.

WHAT THIS DELIBERATELY DOES *NOT* IMPLEMENT
-------------------------------------------
Their strongest tier (Corr / CorrTransform) correlates the relayed flow
against the proxy peer's OWN concurrent background traffic.  That requires an
ISP-side vantage that observes BOTH legs of the relay (client->exit and
exit->server).  We observe only the exit->server leg at the destination
server, so the other leg does not exist in our captures at all.  It is
STRUCTURALLY UNAVAILABLE here and is not approximated, faked, or substituted.

FEATURES WE DELIBERATELY EXCLUDE (and why)
------------------------------------------
  * gap_ms  -- this is the detection signal proposed by the paper this
    baseline is being compared against.  Feeding it to the baseline would
    make the comparison meaningless.  It is NOT in the Beyond RTT feature
    list either.  (Caveat, stated in the report: generic k-FP inter-packet
    timing statistics computed over the first 20 packets can partially
    capture the same underlying quantity.  We keep those, because they ARE
    part of the source method; that can only help this baseline.)
  * syn_ttl / syn_window / syn_mss / syn_wscale / syn_optlayout -- passive OS
    fingerprinting (p0f-style), not part of the Beyond RTT lightweight
    traffic-analysis feature set.
  * user_agent, dport, server_ip, tag, param_* -- application/experiment
    metadata, not traffic-analysis features.  (In our data every flow is
    curl-or-Chrome over TCP/443, so these carry capture-campaign identity,
    not method signal.)

DATA LIMITATIONS FORCED ON US (all reported, none silently patched)
-------------------------------------------------------------------
  1. WINDOW.  Almost none of our negative flows are 20 packets long (see the
     printed summary).  We therefore treat "first 20 packets" as an UPPER
     truncation bound: a flow of n < 20 packets contributes all n packets.
     `pkts_used` in the output records exactly how many packets each score
     was computed from, so a consumer can re-filter to the strict >=20
     subset.  The strict >=20 subset is reported separately and is shown to
     be non-evaluable for this task (see summary).
  2. k-FP CONSTANTS.  k-FP was defined over full Tor traces (thousands of
     packets): first/last 30 packets, concentration in chunks of 20, burst
     length thresholds of >5/10/15/20.  Inside a 20-packet window those are
     degenerate, so we rescale them to first/last 10, chunks of 5, and burst
     thresholds >2/3/5.  This is a forced adaptation, not the original
     constants.
  3. WHOLE-CONNECTION DURATION.  Our per-flow packet list is capped at 128
     packets by the extractor, so for the (few) flows longer than that the
     duration is the duration of the first 128 packets.  Flagged by a
     feature `conn_pkts_truncated`.
  4. MISSING VALUES are left as NaN and handled natively by the tree
     ensembles.  Nothing is imputed.

LEAKAGE CONTROL
---------------
Grouped cross-validation by client_ip (exit nodes recur).  We use
StratifiedGroupKFold as the primary splitter -- it enforces the same
"no client_ip in both train and test" constraint as GroupKFold, but also
keeps at least some negatives in every fold, which plain GroupKFold does not
guarantee here because the negative class comes from only a handful of IPs.
Plain GroupKFold is also run and reported for transparency.
Only out-of-fold scores are ever reported.  Class imbalance is handled with
balanced class weights.

Usage:
  python3 scripts/method_beyondrtt_ta.py                       # paper-faithful
  python3 scripts/method_beyondrtt_ta.py --features flowonly \
      --out out/scores_beyondrtt_ta_flowonly.jsonl             # ablation
"""

import argparse
import json
import math
import os
import sys
from collections import Counter, defaultdict

import numpy as np
from sklearn.ensemble import HistGradientBoostingClassifier, RandomForestClassifier
from sklearn.metrics import roc_auc_score, average_precision_score, roc_curve
from sklearn.model_selection import GroupKFold, StratifiedGroupKFold

POS_CLASS = "resproxy"
NEG_CLASS = "direct"

# ---------------------------------------------------------------------------
# feature helpers
# ---------------------------------------------------------------------------


def _stats(v, prefix, out):
    """mean/std/max/min/median over a list; NaN when undefined."""
    if len(v) == 0:
        for s in ("mean", "std", "max", "min", "med", "sum"):
            out[f"{prefix}_{s}"] = np.nan
        return
    a = np.asarray(v, dtype=float)
    out[f"{prefix}_mean"] = float(a.mean())
    out[f"{prefix}_std"] = float(a.std()) if a.size > 1 else np.nan
    out[f"{prefix}_max"] = float(a.max())
    out[f"{prefix}_min"] = float(a.min())
    out[f"{prefix}_med"] = float(np.median(a))
    out[f"{prefix}_sum"] = float(a.sum())


def _mode(v):
    """Mode of a list; ties broken by smallest value for determinism.

    'mode of sent / received volume' is an explicit Beyond RTT
    connection-level statistic.
    """
    if not v:
        return np.nan
    c = Counter(v)
    best = max(c.values())
    return float(min(k for k, n in c.items() if n == best))


def flow_features(rec, window):
    """k-FP-style + connection-level features over the first `window` packets."""
    f = {}
    pkts = rec["pkts"][:window]
    n = len(pkts)

    ts = np.asarray([p[0] for p in pkts], dtype=float)
    dr = np.asarray([p[1] for p in pkts], dtype=int)      # 1 = client->server
    ln = np.asarray([p[2] for p in pkts], dtype=int)      # tcp payload length

    out_mask = dr == 1
    in_mask = dr == 0
    n_out, n_in = int(out_mask.sum()), int(in_mask.sum())

    # --- k-FP 1-8: per-direction packet counts and fractions ---------------
    f["n_pkts_window"] = float(n)
    f["n_out"] = float(n_out)
    f["n_in"] = float(n_in)
    f["frac_out"] = n_out / n if n else np.nan
    f["frac_in"] = n_in / n if n else np.nan
    f["ratio_out_in"] = n_out / n_in if n_in else np.nan

    # --- k-FP 9-18: first/last k packets per direction ---------------------
    # k-FP uses 30; a 20-packet window forces k=10 (DEVIATION, documented).
    k = 10
    f["out_first10"] = float((dr[:k] == 1).sum())
    f["in_first10"] = float((dr[:k] == 0).sum())
    f["out_last10"] = float((dr[-k:] == 1).sum())
    f["in_last10"] = float((dr[-k:] == 0).sum())

    # --- size statistics per direction (Beyond RTT: mean/median/mode of
    #     sent and received volume; k-FP: size stats) ---------------------
    lo, li = ln[out_mask].tolist(), ln[in_mask].tolist()
    _stats(lo, "sz_out", f)
    _stats(li, "sz_in", f)
    _stats(ln.tolist(), "sz_all", f)
    f["sz_out_mode"] = _mode(lo)
    f["sz_in_mode"] = _mode(li)
    tot = float(ln.sum())
    f["bytes_total"] = tot
    f["bytes_ratio_out"] = float(ln[out_mask].sum()) / tot if tot else np.nan

    # pure-ACK structure (a size statistic; zero-payload packets)
    f["n_ack_out"] = float(((ln == 0) & out_mask).sum())
    f["n_ack_in"] = float(((ln == 0) & in_mask).sum())
    f["frac_ack"] = float((ln == 0).sum()) / n if n else np.nan

    # --- k-FP 19-30: concentration of outgoing packets ---------------------
    # k-FP chunks of 20 over a full trace; a 20-packet window forces chunks
    # of 5 (DEVIATION, documented).
    chunk = 5
    conc = [int((dr[i:i + chunk] == 1).sum()) for i in range(0, n, chunk)]
    _stats(conc, "conc", f)

    # --- bursts (Wang et al., used by k-FP): maximal runs of outgoing pkts --
    bursts, cur = [], 0
    for d in dr:
        if d == 1:
            cur += 1
        elif cur:
            bursts.append(cur)
            cur = 0
    if cur:
        bursts.append(cur)
    f["n_bursts"] = float(len(bursts))
    f["burst_max"] = float(max(bursts)) if bursts else np.nan
    f["burst_mean"] = float(np.mean(bursts)) if bursts else np.nan
    f["burst_std"] = float(np.std(bursts)) if len(bursts) > 1 else np.nan
    # k-FP thresholds >5/10/15/20 are all-zero in a 20-packet window;
    # rescaled to >2/3/5 (DEVIATION, documented).
    for t in (2, 3, 5):
        f[f"n_bursts_gt{t}"] = float(sum(1 for b in bursts if b > t))

    # --- k-FP packet ordering: positions of outgoing packets ---------------
    pos = np.nonzero(out_mask)[0].astype(float)
    f["ord_out_mean"] = float(pos.mean()) if pos.size else np.nan
    f["ord_out_std"] = float(pos.std()) if pos.size > 1 else np.nan
    posi = np.nonzero(in_mask)[0].astype(float)
    f["ord_in_mean"] = float(posi.mean()) if posi.size else np.nan
    f["ord_in_std"] = float(posi.std()) if posi.size > 1 else np.nan

    # --- k-FP timing: inter-packet times, overall and per direction --------
    rel = ts - ts[0]
    f["window_duration_s"] = float(rel[-1])
    ipt = np.diff(rel)
    if ipt.size:
        f["ipt_mean"] = float(ipt.mean())
        f["ipt_std"] = float(ipt.std()) if ipt.size > 1 else np.nan
        f["ipt_max"] = float(ipt.max())
        f["ipt_q25"] = float(np.percentile(ipt, 25))
        f["ipt_q50"] = float(np.percentile(ipt, 50))
        f["ipt_q75"] = float(np.percentile(ipt, 75))
    else:
        for s in ("mean", "std", "max", "q25", "q50", "q75"):
            f[f"ipt_{s}"] = np.nan
    for name, m in (("out", out_mask), ("in", in_mask)):
        d = np.diff(rel[m])
        f[f"ipt_{name}_mean"] = float(d.mean()) if d.size else np.nan
        f[f"ipt_{name}_std"] = float(d.std()) if d.size > 1 else np.nan
        f[f"ipt_{name}_max"] = float(d.max()) if d.size else np.nan

    # --- k-FP transmission-time percentiles --------------------------------
    for p in (25, 50, 75, 100):
        f[f"txtime_p{p}"] = float(np.percentile(rel, p))

    # --- Beyond RTT connection-level: whole-connection duration ------------
    # NOTE: rec["pkts"] is capped at 128 packets by the extractor, so for
    # longer flows this is the duration of the first 128 packets.
    allts = [p[0] for p in rec["pkts"]]
    f["conn_duration_s"] = float(allts[-1] - allts[0])
    f["conn_n_packets"] = float(rec["n_packets"])
    f["conn_pkts_truncated"] = 1.0 if len(rec["pkts"]) >= 128 else 0.0

    # --- Beyond RTT connection-level: cross-layer RTT ----------------------
    # tcp_rtt_ms  : server SYN-ACK -> client ACK
    # tls_rtt_ms  : TLS-layer RTT anchor
    # badpass_delta_ms : tls_rtt_ms - tcp_rtt_ms  (the cross-layer delta)
    for key in ("tcp_rtt_ms", "tls_rtt_ms", "badpass_delta_ms"):
        v = rec.get(key)
        f[key] = float(v) if v is not None else np.nan

    return f


def interconn_features(records):
    """Causal inter-connection-gap statistics, per client_ip.

    Beyond RTT lists 'inter-connection gaps' as a connection-level statistic.
    At a content provider these are computed over the connections that IP has
    already made.  We compute them CAUSALLY (only connections with an earlier
    first_ts from the same client_ip contribute) so no future information
    leaks backwards.
    """
    order = sorted(range(len(records)), key=lambda i: records[i]["first_ts"] or 0.0)
    hist = defaultdict(list)          # client_ip -> [timestamps]
    gaps = defaultdict(list)          # client_ip -> [inter-connection gaps]
    feats = [None] * len(records)
    for i in order:
        r = records[i]
        ip = r["client_ip"]
        t = r["first_ts"] or 0.0
        h, g = hist[ip], gaps[ip]
        f = {}
        f["ic_n_prior"] = float(len(h))
        f["ic_prev_gap_s"] = float(t - h[-1]) if h else np.nan
        f["ic_mean_gap_s"] = float(np.mean(g)) if g else np.nan
        f["ic_med_gap_s"] = float(np.median(g)) if g else np.nan
        f["ic_std_gap_s"] = float(np.std(g)) if len(g) > 1 else np.nan
        f["ic_min_gap_s"] = float(np.min(g)) if g else np.nan
        for w in (60.0, 600.0):
            f[f"ic_n_prior_{int(w)}s"] = float(sum(1 for x in h if t - x <= w))
        f["ic_age_s"] = float(t - h[0]) if h else np.nan
        feats[i] = f
        if h:
            g.append(t - h[-1])
        h.append(t)
    return feats


# ---------------------------------------------------------------------------
# evaluation helpers
# ---------------------------------------------------------------------------


def make_model(kind, seed):
    if kind == "hgb":
        # gradient boosting, native NaN handling, balanced class weights
        return HistGradientBoostingClassifier(
            max_iter=300, learning_rate=0.1, max_leaf_nodes=31,
            class_weight="balanced", random_state=seed)
    return RandomForestClassifier(
        n_estimators=400, min_samples_leaf=2, n_jobs=-1,
        class_weight="balanced_subsample", random_state=seed)


def negbal_splits(y, groups, n_splits, rng):
    """Group split that puts at least one NEGATIVE group in every fold.

    Plain GroupKFold / StratifiedGroupKFold are unusable here: the negative
    class comes from only a handful of client_ip groups, so most splits leave
    entire folds with zero negatives, which makes the per-fold AUC undefined
    and the pooled out-of-fold AUC an artefact of which fold happened to get
    the negatives.  This splitter assigns the negative groups round-robin
    across folds first, then the positive groups, so
      * no client_ip is ever in both train and test (same guarantee as
        GroupKFold), and
      * every fold contains real negatives.
    """
    neg_g = list(dict.fromkeys(groups[y == 0].tolist()))
    pos_g = [x for x in dict.fromkeys(groups[y == 1].tolist())
             if x not in set(neg_g)]
    rng.shuffle(neg_g)
    rng.shuffle(pos_g)
    assign = {}
    for i, gname in enumerate(neg_g):
        assign[gname] = i % n_splits
    for i, gname in enumerate(pos_g):
        assign[gname] = i % n_splits
    fold_of = np.asarray([assign[x] for x in groups])
    return [(np.nonzero(fold_of != k)[0], np.nonzero(fold_of == k)[0])
            for k in range(n_splits)]


def oof_scores(X, y, groups, kind, splits, seed):
    """Out-of-fold probabilities + per-fold AUC + fold models."""
    oof = np.full(len(y), np.nan)
    fold_auc, models, fold_of = [], [], np.full(len(y), -1)
    for k, (tr, te) in enumerate(splits):
        m = make_model(kind, seed)
        m.fit(X[tr], y[tr])
        p = m.predict_proba(X[te])[:, 1]
        oof[te] = p
        fold_of[te] = k
        models.append((m, set(np.unique(groups[tr]))))
        if len(np.unique(y[te])) == 2:
            fold_auc.append((k, len(te), int((y[te] == 0).sum()),
                             roc_auc_score(y[te], p)))
        else:
            fold_auc.append((k, len(te), int((y[te] == 0).sum()), float("nan")))
    return oof, fold_auc, models, fold_of


def tpr_at_fpr(y, s, target):
    fpr, tpr, thr = roc_curve(y, s)
    idx = np.searchsorted(fpr, target, side="right") - 1
    idx = max(idx, 0)
    return float(tpr[idx]), float(fpr[idx]), float(thr[idx])


# ---------------------------------------------------------------------------


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default="out/dataset.jsonl")
    ap.add_argument("--out", default="out/scores_beyondrtt_ta.jsonl")
    ap.add_argument("--window", type=int, default=20,
                    help="Beyond RTT lightweight tier: first 20 packets")
    ap.add_argument("--min-pkts", type=int, default=8,
                    help="minimum packets for the feature vector to be "
                         "defined (3-way handshake + a handshake exchange in "
                         "both directions)")
    ap.add_argument("--features",
                    choices=["full", "flowonly", "nortt", "taonly"],
                    default="full",
                    help="full     = paper-faithful (all lightweight-tier "
                         "features); "
                         "flowonly = drop inter-connection statistics; "
                         "nortt    = drop cross-layer RTT features; "
                         "taonly   = drop both, i.e. pure k-FP "
                         "traffic-analysis features only")
    ap.add_argument("--model", choices=["hgb", "rf"], default="hgb")
    ap.add_argument("--splits", type=int, default=4)
    ap.add_argument("--repeats", type=int, default=5,
                    help="repeats of the grouped CV with different group->fold "
                         "assignments; the spread across repeats is the "
                         "honest uncertainty given so few negative groups")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--diagnose", action="store_true",
                    help="print per-feature univariate AUC and value ranges, "
                         "to expose features that separate the classes for "
                         "reasons of capture design rather than proxying")
    a = ap.parse_args()

    recs = [json.loads(l) for l in open(a.data)]
    print(f"loaded {len(recs)} connections from {a.data}")

    # ---- packet-budget reality check (reported, never patched) -----------
    reach20 = Counter()
    tot_cls = Counter()
    for r in recs:
        tot_cls[r["label_class"]] += 1
        if r["n_packets"] >= a.window:
            reach20[r["label_class"]] += 1
    print(f"\n-- packet budget: flows reaching the {a.window}-packet window --")
    for c in ("resproxy", "direct", "benign_tunnel", "vpn"):
        n, m = tot_cls[c], reach20[c]
        print(f"   {c:14s} {m:6d} / {n:6d}  ({100*m/n:5.1f}%)")
    print(f"   {'ALL':14s} {sum(reach20.values()):6d} / {len(recs):6d}  "
          f"({100*sum(reach20.values())/len(recs):5.1f}%)")

    # ---- features --------------------------------------------------------
    RTT_FEATS = {"tcp_rtt_ms", "tls_rtt_ms", "badpass_delta_ms"}
    drop_ic = a.features in ("flowonly", "taonly")
    drop_rtt = a.features in ("nortt", "taonly")

    ic = interconn_features(recs)
    rows, names = [], None
    for r, icf in zip(recs, ic):
        f = flow_features(r, a.window)
        if not drop_ic:
            f.update(icf)
        if drop_rtt:
            for k in RTT_FEATS:
                f.pop(k, None)
        if names is None:
            names = sorted(f)
        rows.append([f[k] for k in names])
    X_all = np.asarray(rows, dtype=float)
    print(f"\nfeature vector: {len(names)} features  (mode={a.features})")

    applicable = np.asarray([r["n_packets"] >= a.min_pkts for r in recs])
    pkts_used = np.asarray([min(len(r["pkts"]), a.window) for r in recs])
    cls = np.asarray([r["label_class"] for r in recs])
    groups_all = np.asarray([r["client_ip"] for r in recs])

    n_inap = int((~applicable).sum())
    print(f"inapplicable (n_packets < {a.min_pkts}): {n_inap} "
          f"({dict(Counter(cls[~applicable]))})")

    # ---- binary evaluation set ------------------------------------------
    sel = applicable & np.isin(cls, [POS_CLASS, NEG_CLASS])
    idx = np.nonzero(sel)[0]
    X, g = X_all[idx], groups_all[idx]
    y = (cls[idx] == POS_CLASS).astype(int)
    print(f"\nevaluation set: {len(idx)} flows "
          f"({int(y.sum())} {POS_CLASS} / {int((y==0).sum())} {NEG_CLASS}), "
          f"{len(set(g))} client_ip groups "
          f"({len(set(g[y==0]))} negative-class groups)")

    # ---- optional: univariate separability diagnostic --------------------
    if a.diagnose:
        print("\n-- univariate AUC of each feature (resproxy vs direct) --")
        print("   a feature at AUC ~1.00 single-handedly separates the two "
              "classes; check whether that is plausible proxy behaviour or "
              "an artefact of how the two captures were generated")
        rows_d = []
        for j, nm in enumerate(names):
            col = X[:, j]
            ok = ~np.isnan(col)
            if ok.sum() < 10 or len(np.unique(y[ok])) < 2:
                continue
            u = roc_auc_score(y[ok], col[ok])
            u = max(u, 1.0 - u)                      # direction-agnostic
            p = col[ok & (y == 1)]
            q = col[ok & (y == 0)]
            rows_d.append((u, nm, np.median(p), np.median(q),
                           float(ok.mean())))
        rows_d.sort(reverse=True)
        print(f"   {'feature':24s} {'|AUC|':>6s} {'med(resproxy)':>14s} "
              f"{'med(direct)':>13s} {'coverage':>9s}")
        for u, nm, mp, mq, cov in rows_d[:20]:
            print(f"   {nm:24s} {u:6.4f} {mp:14.4f} {mq:13.4f} {cov:8.1%}")
        n_perfect = sum(1 for r in rows_d if r[0] >= 0.99)
        print(f"   features with univariate AUC >= 0.99: {n_perfect} "
              f"of {len(rows_d)}")

    # ---- primary: negative-balanced grouped CV, repeated -----------------
    n_neg_groups = len(set(g[y == 0]))
    nsp = min(a.splits, n_neg_groups)
    print(f"\n-- {nsp}-fold grouped CV by client_ip, negative-balanced, "
          f"{a.repeats} repeats (model={a.model}) --")
    print(f"   (every fold holds out {n_neg_groups // nsp} of the "
          f"{n_neg_groups} negative-class client_ip groups)")

    rep_pooled, rep_fold, oof, models = [], [], None, None
    for rep in range(a.repeats):
        rng = np.random.default_rng(a.seed + rep)
        splits = negbal_splits(y, g, nsp, rng)
        o, fa, mo, _ = oof_scores(X, y, g, a.model, splits, a.seed + rep)
        pooled = roc_auc_score(y, o)
        per = [x[3] for x in fa if x[3] == x[3]]
        rep_pooled.append(pooled)
        rep_fold.extend(per)
        print(f"   repeat {rep}: per-fold AUC "
              f"{[f'{v:.4f}' for v in per]}  pooled {pooled:.4f}")
        if rep == 0:                       # emit scores from the first repeat
            oof, models = o, mo

    print(f"   pooled out-of-fold AUC   : mean {np.mean(rep_pooled):.4f} "
          f"+- {np.std(rep_pooled):.4f}  (over {a.repeats} repeats, "
          f"min {min(rep_pooled):.4f} max {max(rep_pooled):.4f})")
    print(f"   per-fold  AUC            : mean {np.mean(rep_fold):.4f} "
          f"+- {np.std(rep_fold):.4f}  (n={len(rep_fold)} folds, "
          f"min {min(rep_fold):.4f} max {max(rep_fold):.4f})")
    print(f"   pooled out-of-fold PR-AUC: "
          f"{average_precision_score(y, oof):.4f} "
          f"(positive prevalence {y.mean():.4f})")

    for tgt in (0.002, 0.01, 0.05):
        t, fp, th = tpr_at_fpr(y, oof, tgt)
        # precision at BALANCED prevalence, derived from OOF TPR/FPR:
        prec = t / (t + fp) if (t + fp) > 0 else float("nan")
        print(f"   TPR @ FPR<={tgt*100:4.1f}% : {t*100:6.2f}%  "
              f"(actual FPR {fp*100:.2f}%, derived precision at 50% "
              f"prevalence {prec*100:.2f}%)")

    # ---- transparency: the off-the-shelf splitters ------------------------
    print("\n-- off-the-shelf splitters, for transparency --")
    for nm, sp in (("GroupKFold",
                    GroupKFold(n_splits=a.splits)),
                   ("StratifiedGroupKFold",
                    StratifiedGroupKFold(n_splits=a.splits, shuffle=True,
                                         random_state=a.seed))):
        try:
            spl = list(sp.split(X, y, g))
            o, fa, _, _ = oof_scores(X, y, g, a.model, spl, a.seed)
            nneg = [x[2] for x in fa]
            per = [x[3] for x in fa if x[3] == x[3]]
            print(f"   {nm:22s} negatives/fold={nneg} "
                  f"folds_with_negatives={len(per)}/{len(fa)} "
                  f"pooled_OOF_AUC={roc_auc_score(y, o):.4f}")
        except Exception as e:                            # pragma: no cover
            print(f"   {nm:22s} failed: {e}")

    # ---- strict >=20-packet subset (the paper's actual requirement) ------
    strict = applicable & np.isin(cls, [POS_CLASS, NEG_CLASS]) & \
        np.asarray([r["n_packets"] >= a.window for r in recs])
    sy = (cls[strict] == POS_CLASS).astype(int)
    sg = groups_all[strict]
    print(f"\n-- strict '>= {a.window} packets' subset (paper's literal "
          f"requirement) --")
    print(f"   {int(strict.sum())} flows: {int(sy.sum())} {POS_CLASS}, "
          f"{int((sy==0).sum())} {NEG_CLASS} from "
          f"{len(set(sg[sy==0]))} client_ip group(s)")
    if len(set(sg[sy == 0])) < 2:
        print("   NOT EVALUABLE: the negatives come from fewer than 2 "
              "client_ip groups, so any client_ip-grouped split leaves at "
              "least one training fold with zero negatives.  No number is "
              "reported rather than a meaningless one.")

    # ---- feature importance (RF, impurity-based, averaged over folds) ----
    rf_splits = negbal_splits(y, g, nsp, np.random.default_rng(a.seed))
    rf_oof, rf_fauc, rf_models, _ = oof_scores(X, y, g, "rf", rf_splits,
                                               a.seed)
    imp = np.mean([m.feature_importances_ for m, _ in rf_models], axis=0)
    print(f"\n-- random-forest variant (paper offers GBT *or* RF) --")
    print(f"   pooled out-of-fold AUC      : {roc_auc_score(y, rf_oof):.4f}")
    print("   top-15 impurity importances (RF, mean over folds):")
    for i in np.argsort(imp)[::-1][:15]:
        print(f"     {names[i]:24s} {imp[i]:.4f}")

    # ---- score every connection ------------------------------------------
    # resproxy/direct  -> out-of-fold score (never seen in its own training)
    # vpn/benign_tunnel-> mean over fold models whose TRAINING GROUPS exclude
    #                     that client_ip (they are not in the binary training
    #                     set at all, so this stays leakage-free)
    score = np.full(len(recs), np.nan)
    score[idx] = oof
    other = np.nonzero(applicable & ~np.isin(cls, [POS_CLASS, NEG_CLASS]))[0]
    if len(other):
        Xo = X_all[other]
        preds = np.full((len(models), len(other)), np.nan)
        for j, (m, tg) in enumerate(models):
            ok = np.asarray([groups_all[i] not in tg for i in other])
            if ok.any():
                preds[j, ok] = m.predict_proba(Xo[ok])[:, 1]
        with np.errstate(invalid="ignore"):
            score[other] = np.nanmean(preds, axis=0)
        n_nomodel = int(np.isnan(score[other]).sum())
        if n_nomodel:
            print(f"\n   {n_nomodel} non-training-class flows had no "
                  f"group-disjoint fold model -> left unscored")

    os.makedirs(os.path.dirname(a.out) or ".", exist_ok=True)
    n_written = n_app = 0
    with open(a.out, "w") as w:
        for i, r in enumerate(recs):
            s = score[i]
            app = bool(applicable[i] and s == s)
            w.write(json.dumps({
                "conn_key": r["conn_key"],
                "score": float(s) if app else None,
                "applicable": app,
                "pkts_used": int(pkts_used[i]),
                "label_class": r["label_class"],
                "label_family": r["label_family"],
            }) + "\n")
            n_written += 1
            n_app += app
    print(f"\nwrote {n_written} rows -> {a.out}  ({n_app} scoreable, "
          f"{n_written - n_app} not)")

    # ---- how the non-target classes land ---------------------------------
    print("\n-- score distribution by class (median / mean, scoreable only) --")
    for c in ("resproxy", "direct", "benign_tunnel", "vpn"):
        m = (cls == c) & ~np.isnan(score)
        if m.any():
            print(f"   {c:14s} n={int(m.sum()):6d}  median="
                  f"{np.median(score[m]):.4f}  mean={score[m].mean():.4f}")

    print("\nNOTE: the Corr / CorrTransform tier of Beyond RTT is NOT "
          "implemented -- it needs an ISP vantage observing both legs of the "
          "relay; we only see the exit->server leg.")


if __name__ == "__main__":
    sys.exit(main())
