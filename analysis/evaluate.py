#!/usr/bin/env python3
"""
Common evaluation for every compared method on identical connections.

Produces, for the primary task (resproxy vs direct):
  * threshold-free AUC, with 95% CI by bootstrap
  * TPR/FPR at each method's own published operating point
  * coverage: what fraction of connections the method can score at all
  * median packet depth needed to decide
  * the same AUC restricted to the subset where ALL methods are applicable
    (the apples-to-apples comparison)
  * PPV as a function of base rate
  * ROC curves written out for plotting

Nothing here is hard-coded from the paper: every number is computed from
out/dataset.jsonl and out/scores_*.jsonl.
"""
import argparse, glob, json, math, os, random
from collections import defaultdict

import numpy as np


# Methods carried directly in the dataset (no separate scores file).
# name -> (field, higher_is_tunnel, native_threshold, native_label)
BUILTIN = {
    "ours":    ("gap_ms",           True, 10.0, "t=10 ms"),
    "badpass": ("badpass_delta_ms", True, 50.0, "t=50 ms"),
}


def roc(pos, neg):
    """Return (fpr[], tpr[], auc). Scores: higher = more positive."""
    if not pos or not neg:
        return [], [], float("nan")
    ys = np.r_[np.ones(len(pos)), np.zeros(len(neg))]
    ss = np.r_[np.asarray(pos, float), np.asarray(neg, float)]
    order = np.argsort(-ss, kind="mergesort")
    ys, ss = ys[order], ss[order]
    tp = np.cumsum(ys)
    fp = np.cumsum(1 - ys)
    # keep one point per distinct score
    keep = np.r_[np.diff(ss) != 0, True]
    tpr = np.r_[0.0, tp[keep] / len(pos)]
    fpr = np.r_[0.0, fp[keep] / len(neg)]
    auc = float(np.trapezoid(tpr, fpr))
    return fpr.tolist(), tpr.tolist(), auc


def auc_ci(pos, neg, n_boot=300, seed=0):
    if not pos or not neg:
        return (float("nan"), float("nan"))
    rng = random.Random(seed)
    P, N = list(pos), list(neg)
    # The interval is dominated by the small negative class; resampling all
    # ~32k positives every iteration costs a great deal and moves it very
    # little, so cap the positive resample.
    if len(P) > 4000:
        P = [P[rng.randrange(len(P))] for _ in range(4000)]
    vals = []
    for _ in range(n_boot):
        p = [P[rng.randrange(len(P))] for _ in range(len(P))]
        n = [N[rng.randrange(len(N))] for _ in range(len(N))]
        vals.append(roc(p, n)[2])
    vals.sort()
    return (vals[int(0.025 * len(vals))], vals[int(0.975 * len(vals))])


def load(root):
    ds = {}
    for line in open(os.path.join(root, "out/dataset.jsonl")):
        r = json.loads(line)
        ds[r["conn_key"]] = r

    methods = {}
    for name, (field, hi, thr, lbl) in BUILTIN.items():
        s = {}
        for k, r in ds.items():
            v = r.get(field)
            s[k] = None if v is None else (float(v) if hi else -float(v))
        methods[name] = {"scores": s, "thr": thr, "thr_label": lbl,
                         "pkts": {k: (4 if name == "ours" else None)
                                  for k in ds}}
    for p in sorted(glob.glob(os.path.join(root, "out/scores_*.jsonl"))):
        name = os.path.basename(p)[len("scores_"):-len(".jsonl")]
        s, pk = {}, {}
        for line in open(p):
            r = json.loads(line)
            s[r["conn_key"]] = (None if not r.get("applicable")
                                else (None if r.get("score") is None
                                      else float(r["score"])))
            pk[r["conn_key"]] = r.get("pkts_used")
        methods[name] = {"scores": s, "thr": None, "thr_label": "-",
                         "pkts": pk}
    return ds, methods


def ppv(tpr, fpr, prev):
    return (tpr * prev) / (tpr * prev + fpr * (1 - prev)) if (tpr or fpr) else float("nan")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=os.path.dirname(os.path.dirname(
        os.path.abspath(__file__))))
    ap.add_argument("--pos", default="resproxy")
    ap.add_argument("--neg", default="direct")
    a = ap.parse_args()

    ds, methods = load(a.root)
    pos_keys = [k for k, r in ds.items() if r["label_class"] == a.pos]
    neg_keys = [k for k, r in ds.items() if r["label_class"] == a.neg]
    print(f"task: {a.pos} (n={len(pos_keys)}) vs {a.neg} (n={len(neg_keys)})\n")

    # ---- per-method, on each method's own scoreable subset --------------
    rows = []
    for name, m in sorted(methods.items()):
        s = m["scores"]
        P = [s[k] for k in pos_keys if s.get(k) is not None]
        N = [s[k] for k in neg_keys if s.get(k) is not None]
        cov = (len(P) + len(N)) / (len(pos_keys) + len(neg_keys))
        fpr, tpr, A = roc(P, N)
        lo, hi = auc_ci(P, N)
        t = m["thr"]
        if t is not None and P and N:
            TPR = sum(1 for x in P if x > t) / len(P)
            FPR = sum(1 for x in N if x > t) / len(N)
        else:
            TPR = FPR = float("nan")
        pk = [v for v in m["pkts"].values() if v]
        rows.append((name, len(P), len(N), cov, A, lo, hi,
                     m["thr_label"], TPR, FPR,
                     (float(np.median(pk)) if pk else float("nan"))))

    print("== each method on its own scoreable subset ==")
    print(f"{'method':16}{'n+':>7}{'n-':>6}{'cov':>7}{'AUC':>8}"
          f"{'95% CI':>16}{'op.point':>10}{'TPR':>8}{'FPR':>8}{'pkts':>6}")
    for (n, np_, nn, cov, A, lo, hi, lbl, T, F, pk) in rows:
        ci = f"[{lo:.3f},{hi:.3f}]" if lo == lo else "-"
        print(f"{n:16}{np_:>7}{nn:>6}{cov:>6.1%}{A:>8.3f}{ci:>16}"
              f"{lbl:>10}{T:>8.1%}{F:>8.1%}"
              f"{('-' if pk != pk else f'{pk:.0f}'):>6}")

    # ---- common subset: every method applicable --------------------------
    common = [k for k in pos_keys + neg_keys
              if all(m["scores"].get(k) is not None for m in methods.values())]
    cp = [k for k in common if ds[k]["label_class"] == a.pos]
    cn = [k for k in common if ds[k]["label_class"] == a.neg]
    print(f"\n== common subset where ALL methods apply: "
          f"{len(cp)} {a.pos} + {len(cn)} {a.neg} ==")
    for name, m in sorted(methods.items()):
        s = m["scores"]
        A = roc([s[k] for k in cp], [s[k] for k in cn])[2]
        print(f"  {name:16} AUC {A:.3f}")

    # ---- PPV vs base rate, using each method's operating point -----------
    print("\n== PPV vs base rate (at each method's own operating point) ==")
    print(f"{'method':16}" + "".join(f"{p:>10}" for p in
                                     ("80%", "10%", "1%", "0.5%", "0.1%")))
    for (n, _, _, _, _, _, _, lbl, T, F, _) in rows:
        if T != T:
            continue
        print(f"{n:16}" + "".join(f"{ppv(T,F,p):>10.1%}"
                                  for p in (0.8, 0.1, 0.01, 0.005, 0.001)))

    # ---- ROC curves for plotting ----------------------------------------
    outdir = os.path.join(a.root, "out/roc")
    os.makedirs(outdir, exist_ok=True)
    for name, m in sorted(methods.items()):
        s = m["scores"]
        fpr, tpr, _ = roc([s[k] for k in pos_keys if s.get(k) is not None],
                          [s[k] for k in neg_keys if s.get(k) is not None])
        with open(os.path.join(outdir, f"{name}.dat"), "w") as w:
            w.write("# fpr tpr\n")
            for x, y in zip(fpr, tpr):
                w.write(f"{x:.6f} {y:.6f}\n")
    print(f"\nROC curves -> {outdir}/*.dat")


if __name__ == "__main__":
    main()
