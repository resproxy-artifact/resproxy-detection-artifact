#!/usr/bin/env python3
"""
method_huang.py -- Huang, Zhao, Mi, Wang, "Shining Light into the Tunnel:
Understanding and Classifying Network Traffic of Residential Proxies"
(arXiv:2404.10610), Appendix G hand-crafted feature family, re-implemented and
applied to our destination-server vantage point.

WHAT THE PAPER SPECIFIES (and what we implement)
------------------------------------------------
186 payload-independent features at N=64, all anchored to ORDINAL PACKET
POSITION (never to a protocol message).  With the exponential index sequence
I(N) = {2, 4, 8, ..., N} (|I(64)| = 6) the count decomposes exactly as:

    UpRatio_i                                 6      (up sequence only)
    PAT_{up,down,all},i,{mean,min,max,std}   72      (3 x 6 x 4)
    BPS_{up,down,all},i                      18      (3 x 6)
    PPS_{up,down,all},i                      18      (3 x 6)
    PS_{up,down,all},i,{mean,min,max,std}    72      (3 x 6 x 4)
                                            ---
                                            186

  * UpRatio_i  = cumulative upstream bytes / (upstream + downstream bytes)
                 evaluated at the instant of the i-th UPSTREAM packet.  The
                 denominator counts every packet in the flow whose timestamp is
                 <= the timestamp of that i-th upstream packet.
  * PAT_D,i,*  = statistics of the inter-packet arrival gaps among the first i
                 packets of direction D (i-1 gaps).
  * BPS_D,i    = sum of the sizes of the first i packets of direction D divided
                 by the elapsed time between the 1st and the i-th of them.
  * PPS_D,i    = i divided by that same elapsed time.
  * PS_D,i,*   = statistics of the sizes of the first i packets of direction D.
  * Short flows are padded by repeating the last valid value: if direction D has
    only k < i packets, the feature at index i equals the feature at index k.

Configurations evaluated: (Nup, Ndown, Nall) = (4,0,4), (4,4,4), (8,8,8),
(64,64,64).  Because the feature at (direction, i, stat) does not depend on N,
we compute the full N=64 block once and column-subset per configuration.

Classifier: Random Forest, as in the paper.  Evaluation is out-of-fold
GroupKFold(5) grouped by client_ip, class_weight="balanced".

DEVIATIONS FORCED BY OUR DATA / VANTAGE POINT  (all reported in the summary)
---------------------------------------------------------------------------
D1. VANTAGE POINT.  Their positive traffic is captured ON the residential proxy
    node itself (the proxy peer); their negatives come from the public VNAT and
    ISCXVPN2016 corpora captured elsewhere.  We capture BOTH classes at the
    destination server.  Their positive/negative split therefore also separates
    two capture environments; ours does not.
D2. PACKET SIZE == TCP PAYLOAD LENGTH.  Our per-packet record stores
    len(tcp.data) (see scripts/extract.py), not the on-wire frame size.  We do
    NOT add an estimated header length -- that would be an invented number.
    Consequence: pure-ACK / handshake packets have size 0 here where the paper
    would score them ~54-66 B.  This affects PS_*, BPS_* and UpRatio_*.
D3. UpRatio 0/0.  As a direct consequence of D2, the UpRatio denominator is 0
    whenever the prefix considered contains no payload at all (the common
    SYN / SYN-ACK / ACK prefix, i.e. essentially every flow at i=2).  We set
    those to 0.0 and report how often it happens per index; the paper's
    frame-size denominator can never be 0.
D4. ZERO-DURATION WINDOWS.  BPS/PPS divide by an elapsed time that can be 0
    when two packets share a capture timestamp.  We floor the divisor at 1e-6 s
    (the pcap timestamp resolution) rather than dropping the flow, and report
    how often the floor is hit.
D5. FLOW LENGTH.  Our per-connection packet detail is capped at the first 128
    packets by the extractor, but the real limit is that these are short
    request/response flows; see the native-coverage table printed at run time.
    Padding (the paper's own rule) covers the rest, so no flow is dropped for
    length, but at (64,64,64) nearly every index above the flow length is a
    replica of an earlier one -- the run-time table makes that explicit.

OUTPUT
------
out/scores_huang.jsonl                  primary config, fixed A PRIORI to (8,8,8)
out/scores_huang_N<u>-<d>-<a>.jsonl     one file per configuration
"""
import json
import os
import sys
from collections import Counter, defaultdict

import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import GroupKFold, StratifiedGroupKFold

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATASET = os.path.join(ROOT, "out", "dataset.jsonl")
OUTDIR = os.path.join(ROOT, "out")

MAX_N = 64
EPS_DUR = 1e-6          # D4: pcap timestamp resolution, used as divisor floor
STATS = ("mean", "min", "max", "std")
DIRS = ("up", "down", "all")

# (Nup, Ndown, Nall)
CONFIGS = [(4, 0, 4), (4, 4, 4), (8, 8, 8), (64, 64, 64)]
PRIMARY = (8, 8, 8)     # fixed before looking at any AUC

RF_KW = dict(n_estimators=100, class_weight="balanced",
             random_state=0, n_jobs=-1)
N_SPLITS = 5


def idx_seq(n):
    """Exponential index sequence {2,4,8,...,n}; empty when n < 2."""
    out, i = [], 2
    while i <= n:
        out.append(i)
        i *= 2
    return out


FULL_SEQ = idx_seq(MAX_N)               # [2,4,8,16,32,64]


def build_columns():
    """Column names for the full N=64 block, in a fixed order."""
    cols = []
    for i in FULL_SEQ:
        cols.append(("UpRatio", "up", i, None))
    for d in DIRS:
        for i in FULL_SEQ:
            for s in STATS:
                cols.append(("PAT", d, i, s))
    for d in DIRS:
        for i in FULL_SEQ:
            cols.append(("BPS", d, i, None))
    for d in DIRS:
        for i in FULL_SEQ:
            cols.append(("PPS", d, i, None))
    for d in DIRS:
        for i in FULL_SEQ:
            for s in STATS:
                cols.append(("PS", d, i, s))
    return cols


COLS = build_columns()
COLNAME = ["_".join(str(x) for x in c if x is not None) for c in COLS]


def col_mask(nup, ndown, nall):
    """Boolean mask selecting the columns of configuration (nup, ndown, nall)."""
    keep = {"up": set(idx_seq(nup)), "down": set(idx_seq(ndown)),
            "all": set(idx_seq(nall))}
    return np.array([c[2] in keep[c[1]] for c in COLS], dtype=bool)


class Diag:
    """Run-time counters so nothing in the report is asserted from memory."""

    def __init__(self):
        self.upratio_zero_denom = Counter()   # index -> n flows with 0/0
        self.zero_dur = Counter()             # (dir, index) -> n floor hits
        self.native = defaultdict(Counter)    # dir -> index -> n flows with k>=i
        self.klen = defaultdict(list)         # dir -> per-flow packet count


def flow_features(pkts, diag):
    """Full N=64 feature vector for one flow, plus the number of packets of the
    flow actually consumed at each configuration granularity.

    Returns (vec, kcount, last_pos) where
      kcount[d]   = packets available in direction d
      last_pos[i] = 1-based ordinal position, within the whole flow, of the last
                    packet consumed when the index budget is i (max over the
                    three directions and over the UpRatio cut).
    """
    t_all = np.array([p[0] for p in pkts], dtype=np.float64)
    s_all = np.array([float(p[2]) for p in pkts], dtype=np.float64)
    is_up = np.array([p[1] == 1 for p in pkts], dtype=bool)

    pos = np.arange(1, len(pkts) + 1)        # 1-based ordinal position in flow
    arr = {
        "all": (t_all, s_all, pos),
        "up": (t_all[is_up], s_all[is_up], pos[is_up]),
        "down": (t_all[~is_up], s_all[~is_up], pos[~is_up]),
    }
    kcount = {d: len(arr[d][0]) for d in DIRS}
    for d in DIRS:
        diag.klen[d].append(kcount[d])
        for i in FULL_SEQ:
            if kcount[d] >= i:
                diag.native[d][i] += 1

    feats = {}
    last_pos = {}
    for d in DIRS:
        t, s, p = arr[d]
        k = len(t)
        for i in FULL_SEQ:
            j = min(i, k)                     # padding: repeat last valid value
            if j < 2:
                # Fewer than two packets in this direction: there is no valid
                # value to repeat, so the paper's padding rule cannot fire.
                # We fill placeholders ONLY so the matrix stays rectangular --
                # applicable_for() marks such a flow not-applicable for every
                # configuration that uses this direction, so these numbers are
                # never fed to the classifier and never scored.
                for name in STATS:
                    feats[("PAT", d, i, name)] = 0.0
                feats[("BPS", d, i, None)] = 0.0
                feats[("PPS", d, i, None)] = 0.0
                for name in STATS:
                    feats[("PS", d, i, name)] = 0.0
                last_pos[(d, i)] = int(p[j - 1]) if j == 1 else 0
                continue
            tt, ss = t[:j], s[:j]
            gaps = np.diff(tt)
            pat = (float(gaps.mean()), float(gaps.min()),
                   float(gaps.max()), float(gaps.std()))
            dur = float(tt[-1] - tt[0])
            if dur <= 0.0:
                diag.zero_dur[(d, i)] += 1
                dur = EPS_DUR
            for name, v in zip(STATS, pat):
                feats[("PAT", d, i, name)] = v
            feats[("BPS", d, i, None)] = float(ss.sum()) / dur
            feats[("PPS", d, i, None)] = float(j) / dur
            feats[("PS", d, i, "mean")] = float(ss.mean())
            feats[("PS", d, i, "min")] = float(ss.min())
            feats[("PS", d, i, "max")] = float(ss.max())
            feats[("PS", d, i, "std")] = float(ss.std())
            last_pos[(d, i)] = int(p[j - 1])

    # UpRatio, anchored to the i-th upstream packet
    t_up, s_up, p_up = arr["up"]
    k_up = len(t_up)
    for i in FULL_SEQ:
        if k_up == 0:
            feats[("UpRatio", "up", i, None)] = 0.0
            continue
        j = min(i, k_up)
        t_cut = t_up[j - 1]
        up_bytes = float(s_up[:j].sum())
        tot_bytes = float(s_all[t_all <= t_cut].sum())
        if tot_bytes <= 0.0:
            diag.upratio_zero_denom[i] += 1        # D3
            feats[("UpRatio", "up", i, None)] = 0.0
        else:
            feats[("UpRatio", "up", i, None)] = up_bytes / tot_bytes

    vec = np.array([feats[c] for c in COLS], dtype=np.float64)
    return vec, kcount, last_pos


def pkts_used_for(last_pos, kcount, nup, ndown, nall):
    """Ordinal position of the last flow packet consumed by this configuration."""
    used = 0
    for d, n in (("up", nup), ("down", ndown), ("all", nall)):
        seq = idx_seq(n)
        if not seq:
            continue
        i = seq[-1]
        used = max(used, last_pos[(d, i)])
    return used


def applicable_for(kcount, nup, ndown, nall):
    """A direction used by the configuration must have at least 2 packets, else
    every PAT/BPS/PPS feature for that direction is undefined."""
    reasons = []
    for d, n in (("up", nup), ("down", ndown), ("all", nall)):
        if n >= 2 and kcount[d] < 2:
            reasons.append(f"<2 {d} packets")
    return (len(reasons) == 0), reasons


def main():
    print("=" * 78)
    print("Huang et al. (arXiv:2404.10610) Appendix G features -- our vantage point")
    print("=" * 78)

    rows, X = [], []
    diag = Diag()
    n_read = 0
    for line in open(DATASET):
        r = json.loads(line)
        n_read += 1
        vec, kcount, last_pos = flow_features(r["pkts"], diag)
        X.append(vec)
        rows.append(dict(conn_key=r["conn_key"], client_ip=r["client_ip"],
                         label_class=r["label_class"],
                         label_family=r["label_family"],
                         kcount=kcount, last_pos=last_pos,
                         n_packets=r["n_packets"], n_pkts_detail=len(r["pkts"])))
    X = np.vstack(X)
    st = os.stat(DATASET)
    print(f"\nread {n_read} connections from {DATASET}")
    print(f"  dataset fingerprint: {st.st_size} bytes, mtime {int(st.st_mtime)}")
    assert not np.isnan(X).any(), "NaN in feature matrix"
    print(f"full N={MAX_N} feature block: {X.shape[1]} columns "
          f"(paper states 186)  -> {'MATCH' if X.shape[1] == 186 else 'MISMATCH'}")

    cls = Counter(r["label_class"] for r in rows)
    print("class counts:", dict(cls))
    ndup = n_read - len({r["conn_key"] for r in rows})
    print(f"duplicate conn_key values in the dataset: {ndup} "
          f"(kept as separate rows, one output line per input row)")
    deg = Counter()
    for r in rows:
        for d in DIRS:
            if r["kcount"][d] == 0:
                deg[f"{d}==0"] += 1
            elif r["kcount"][d] == 1:
                deg[f"{d}==1"] += 1
    print(f"flows with a degenerate direction (no valid value to pad from): "
          f"{dict(deg) if deg else 'none'}")

    # ---- flow-length reality check ---------------------------------------
    print("\n-- native index coverage (fraction of flows with >= i packets) --")
    print(f"{'i':>4} {'up':>10} {'down':>10} {'all':>10}")
    for i in FULL_SEQ:
        print(f"{i:>4} " + " ".join(
            f"{diag.native[d][i] / n_read:>10.4f}" for d in DIRS))
    for d in DIRS:
        a = np.array(diag.klen[d])
        print(f"  {d:<5} packets per flow: median {np.median(a):.0f} "
              f"mean {a.mean():.2f} max {a.max()}")

    print("\n-- UpRatio 0/0 (deviation D3), per index --")
    for i in FULL_SEQ:
        c = diag.upratio_zero_denom[i]
        print(f"  i={i:<3} {c:>6} / {n_read} flows ({c / n_read:.4f}) "
              f"forced to 0.0")
    print("-- BPS/PPS zero-duration windows floored at 1e-6 s (deviation D4) --")
    for d in DIRS:
        tot = sum(diag.zero_dur[(d, i)] for i in FULL_SEQ)
        per = ", ".join(f"i={i}:{diag.zero_dur[(d, i)]}" for i in FULL_SEQ)
        print(f"  {d:<5} total {tot} feature-cells across {n_read} flows  ({per})")

    label_class = np.array([r["label_class"] for r in rows])
    groups = np.array([r["client_ip"] for r in rows])
    eval_mask = np.isin(label_class, ["resproxy", "direct"])
    y = (label_class == "resproxy").astype(int)

    print(f"\nevaluation subset (resproxy vs direct): {eval_mask.sum()} flows, "
          f"{int(y[eval_mask].sum())} positive / "
          f"{int((1 - y[eval_mask]).sum())} negative")
    print(f"unique client_ip groups: overall {len(set(groups))}, "
          f"resproxy {len(set(groups[label_class == 'resproxy']))}, "
          f"direct {len(set(groups[label_class == 'direct']))}")

    results = {}
    for cfg in CONFIGS:
        nup, ndown, nall = cfg
        tag = f"N{nup}-{ndown}-{nall}"
        mask = col_mask(*cfg)
        Xc = X[:, mask]
        print("\n" + "-" * 78)
        print(f"CONFIG (Nup,Ndown,Nall) = {cfg}   features = {int(mask.sum())}")

        # applicability + native support
        appl = np.zeros(len(rows), dtype=bool)
        reason_ct = Counter()
        pkts_used = np.zeros(len(rows), dtype=int)
        native_full = 0
        for n, r in enumerate(rows):
            ok, why = applicable_for(r["kcount"], *cfg)
            appl[n] = ok
            if not ok:
                reason_ct[";".join(why)] += 1
            pkts_used[n] = pkts_used_for(r["last_pos"], r["kcount"], *cfg)
            if all(r["kcount"][d] >= v for d, v in
                   (("up", nup), ("down", ndown), ("all", nall))):
                native_full += 1
        print(f"  applicable: {int(appl.sum())}/{len(rows)}"
              + ("" if not reason_ct else f"  not applicable: {dict(reason_ct)}"))
        print(f"  flows reaching every index NATIVELY (no padding): "
              f"{native_full}/{len(rows)} ({native_full / len(rows):.4f})")
        ev = eval_mask & appl
        nat_pos = sum(1 for n, r in enumerate(rows)
                      if ev[n] and label_class[n] == "resproxy"
                      and all(r["kcount"][d] >= v for d, v in
                              (("up", nup), ("down", ndown), ("all", nall))))
        nat_neg = sum(1 for n, r in enumerate(rows)
                      if ev[n] and label_class[n] == "direct"
                      and all(r["kcount"][d] >= v for d, v in
                              (("up", nup), ("down", ndown), ("all", nall))))
        print(f"    of which resproxy {nat_pos}, direct {nat_neg}")

        # ---- out-of-fold GroupKFold(client_ip) -----------------------------
        idx = np.where(ev)[0]
        Xe, ye, ge = Xc[idx], y[idx], groups[idx]
        oof = np.full(len(idx), np.nan)
        gkf = GroupKFold(n_splits=N_SPLITS)
        fold_models = []
        fold_lines = []
        for f, (tr, te) in enumerate(gkf.split(Xe, ye, ge)):
            clf = RandomForestClassifier(**RF_KW)
            clf.fit(Xe[tr], ye[tr])
            oof[te] = clf.predict_proba(Xe[te])[:, 1]
            fold_models.append(clf)
            npos, nneg = int(ye[te].sum()), int((1 - ye[te]).sum())
            if npos and nneg:
                a = roc_auc_score(ye[te], oof[te])
                fold_lines.append(f"    fold {f}: n={len(te)} pos={npos} "
                                  f"neg={nneg} AUC={a:.4f}")
            else:
                fold_lines.append(f"    fold {f}: n={len(te)} pos={npos} "
                                  f"neg={nneg} AUC=undefined (single class)")
        auc = roc_auc_score(ye, oof)
        print(f"  GroupKFold({N_SPLITS}) by client_ip, RF{RF_KW['n_estimators']} "
              f"class_weight=balanced")
        for l in fold_lines:
            print(l)
        print(f"  >> pooled out-of-fold AUC (resproxy vs direct) = {auc:.4f}")

        # per-negative-client_ip breakdown: only 4 direct IPs exist, so a single
        # host driving the number would be invisible in the pooled AUC
        pos_scores = oof[ye == 1]
        for nip in sorted(set(ge[ye == 0])):
            m = (ye == 0) & (ge == nip)
            sub_y = np.concatenate([np.ones(len(pos_scores)),
                                    np.zeros(int(m.sum()))])
            sub_s = np.concatenate([pos_scores, oof[m]])
            print(f"    negatives from {nip}: n={int(m.sum())} "
                  f"AUC vs all positives = {roc_auc_score(sub_y, sub_s):.4f}")

        # what is the forest actually keying on?  With only 4 negative hosts
        # this is the difference between "detects tunnelling" and "detects
        # that our negatives are nearby cloud machines".
        imp = np.mean([m.feature_importances_ for m in fold_models], axis=0)
        cn = np.array(COLNAME)[mask]
        top = np.argsort(imp)[::-1][:8]
        print("  top-8 mean fold-model feature importance:")
        for t in top:
            col = np.where(mask)[0][t]
            mp = float(np.median(X[(label_class == "resproxy") & appl, col]))
            mn = float(np.median(X[(label_class == "direct") & appl, col]))
            print(f"    {cn[t]:<20} imp={imp[t]:.4f}  "
                  f"median resproxy={mp:.6g}  direct={mn:.6g}")

        # Secondary CV.  Only 4 client_ip groups carry the negative class, so
        # plain GroupKFold leaves several folds with no negative at all and the
        # pooled AUC mixes positives scored by 5 models against negatives scored
        # by 2.  StratifiedGroupKFold still never splits a client_ip across
        # train/test, but forces every fold to contain negatives.
        # Repeated over several seeds, because with 4 negative hosts the pooled
        # AUC is a function of which host lands in which fold.
        aucs2 = []
        for seed in range(5):
            sgkf = StratifiedGroupKFold(n_splits=4, shuffle=True,
                                        random_state=seed)
            oof2 = np.full(len(idx), np.nan)
            for tr, te in sgkf.split(Xe, ye, ge):
                c2 = RandomForestClassifier(**RF_KW).fit(Xe[tr], ye[tr])
                oof2[te] = c2.predict_proba(Xe[te])[:, 1]
            aucs2.append(roc_auc_score(ye, oof2))
        aucs2 = np.array(aucs2)
        auc2 = float(aucs2.mean())
        print(f"  >> StratifiedGroupKFold(4) x 5 seeds, pooled OOF AUC "
              f"= {auc2:.4f} +/- {aucs2.std():.4f} "
              f"[min {aucs2.min():.4f}, max {aucs2.max():.4f}]  (secondary)")
        print(f"     per-seed: {' '.join(f'{a:.4f}' for a in aucs2)}")

        # Is the forest needed at all, or does one column already separate our
        # negative set?  Univariate AUC over the same rows, no model.
        uni = np.array([roc_auc_score(ye, Xe[:, j]) for j in range(Xe.shape[1])])
        uni = np.maximum(uni, 1.0 - uni)
        b = int(np.argmax(uni))
        print(f"  >> best SINGLE feature, no classifier: {cn[b]} "
              f"AUC={uni[b]:.4f}  (3rd best {np.sort(uni)[-3]:.4f})")

        results[cfg] = dict(auc=auc, auc2=auc2, auc2sd=float(aucs2.std()),
                            auc2min=float(aucs2.min()), auc2max=float(aucs2.max()),
                            nfeat=int(mask.sum()),
                            n_eval=len(idx), native_full=native_full,
                            best_uni=float(uni[b]), best_uni_name=cn[b])

        # ---- score every connection ---------------------------------------
        # resproxy/direct rows get their genuine out-of-fold score; the held-out
        # classes (benign_tunnel, vpn) were never in any training set and are
        # scored with the mean of the K fold models.
        score = np.full(len(rows), np.nan)
        score[idx] = oof
        other = np.where(appl & ~ev)[0]
        if len(other):
            P = np.mean([m.predict_proba(Xc[other])[:, 1] for m in fold_models],
                        axis=0)
            score[other] = P

        path = os.path.join(OUTDIR, f"scores_huang_{tag}.jsonl")
        with open(path, "w") as w:
            for n, r in enumerate(rows):
                w.write(json.dumps({
                    "conn_key": r["conn_key"],
                    "score": (float(score[n]) if appl[n] and
                              not np.isnan(score[n]) else None),
                    "applicable": bool(appl[n] and not np.isnan(score[n])),
                    "pkts_used": int(pkts_used[n]) if appl[n] else 0,
                    "label_class": r["label_class"],
                    "label_family": r["label_family"],
                }) + "\n")
        print(f"  wrote {path}")
        if cfg == PRIMARY:
            main_path = os.path.join(OUTDIR, "scores_huang.jsonl")
            with open(path) as f, open(main_path, "w") as w:
                w.write(f.read())
            print(f"  wrote {main_path}  (primary config, fixed a priori)")
            for cname in ("benign_tunnel", "vpn"):
                m = (label_class == cname) & appl
                if m.sum():
                    print(f"    held-out class {cname}: n={int(m.sum())} "
                          f"median score {np.median(score[m]):.4f} "
                          f"(never in training; fold-model mean)")

    print("\n" + "=" * 78)
    print("SUMMARY -- pooled out-of-fold AUC, resproxy (pos) vs direct (neg)")
    print(f"{'config':>14} {'#feat':>6} {'#scored':>8} {'native-full':>12} "
          f"{'GKF5 AUC':>9} {'SGKF4 mean':>11} {'SGKF4 range':>20} "
          f"{'best-1feat':>11}")
    for cfg in CONFIGS:
        r = results[cfg]
        print(f"{str(cfg):>14} {r['nfeat']:>6} {r['n_eval']:>8} "
              f"{r['native_full']:>12} {r['auc']:>9.4f} {r['auc2']:>11.4f} "
              f"{('[%.4f, %.4f]' % (r['auc2min'], r['auc2max'])):>20} "
              f"{r['best_uni']:>11.4f}")
    print("native-full = flows reaching every index of the config without the")
    print("paper's padding rule, counted over all", len(rows), "connections.")
    print("best-1feat  = highest univariate AUC of any single column, no model.")
    print("=" * 78)


if __name__ == "__main__":
    sys.exit(main())
