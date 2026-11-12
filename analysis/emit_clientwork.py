#!/usr/bin/env python3
"""
Emit tab:clientwork -- the table that isolates client processing time from
network time, and the PPV-vs-base-rate data file for fig:ppv.

Both are generated so that the numbers in the paper cannot drift from the data.
  python3 scripts/emit_clientwork.py            # writes out/tab_clientwork.tex
                                                #    and out/ppv.dat
"""
import json, statistics
import numpy as np

DATASET = "out/dataset.jsonl"
T_OURS, T_BP = 10.0, 50.0

POPS = [
    ("20260327_browser_full", r"real browser, short path", None),
    ("pcap_direct_baseline_v3", r"real browser, long path", None),
    ("unified", r"\texttt{curl}, short path", None),
]


def med(xs):
    xs = [x for x in xs if x is not None]
    return statistics.median(xs) if xs else float("nan")


def main():
    rows = [json.loads(l) for l in open(DATASET)]
    direct = [r for r in rows if r["label_class"] == "direct"]

    lines = [
        r"\begin{table}[t]", r"\centering\footnotesize",
        r"\caption{Isolating the client's own processing from network time.",
        r"All three populations are \emph{direct} connections. BADPASS's interval",
        r"spans the client's work on the server flight; ours closes before the",
        r"server sends anything. When the network term is small, that work is what",
        r"BADPASS measures. Thresholds are each method's own",
        r"($t=\SI{10}{\milli\second}$ and $t=\SI{50}{\milli\second}$).}",
        r"\label{tab:clientwork}",
        r"\begin{tabular}{@{}lrrrrr@{}}", r"\toprule",
        r"\textbf{Direct population} & \textbf{$n$} & \textbf{TCP RTT} &"
        r" \textbf{TLS RTT} & \textbf{BADPASS} & \textbf{ours}\\",
        r" & & (ms) & (ms) & FPR & FPR\\",
        r"\midrule",
    ]
    for prefix, label, _ in POPS:
        v = [r for r in direct if (r.get("src_pcap") or "").startswith(prefix)]
        if not v:
            continue
        tcp = med([r["tcp_rtt_ms"] for r in v])
        tls = med([r["tls_rtt_ms"] for r in v])
        g = [r["gap_ms"] for r in v if r["gap_ms"] is not None]
        d = [r["badpass_delta_ms"] for r in v if r["badpass_delta_ms"] is not None]
        ofp = 100 * np.mean(np.asarray(g) > T_OURS) if g else float("nan")
        bfp = 100 * np.mean(np.asarray(d) > T_BP) if d else float("nan")
        lines.append(f"{label} & {len(v)} & {tcp:.2f} & {tls:.2f} & "
                     f"\\textbf{{{bfp:.0f}\\%}} & {ofp:.0f}\\%\\\\")
    lines += [r"\bottomrule", r"\end{tabular}", r"\end{table}"]
    open("out/tab_clientwork.tex", "w").write("\n".join(lines) + "\n")
    print("wrote out/tab_clientwork.tex")

    # PPV vs base rate, at our measured operating point
    pos = [r["gap_ms"] for r in rows
           if r["label_class"] == "resproxy" and r["gap_ms"] is not None]
    neg = [r["gap_ms"] for r in direct if r["gap_ms"] is not None]
    tpr = float(np.mean(np.asarray(pos) > T_OURS))
    fpr = float(np.mean(np.asarray(neg) > T_OURS))
    with open("out/ppv.dat", "w") as w:
        w.write(f"# prevalence ppv   (TPR={tpr:.4f} FPR={fpr:.4f})\n")
        for p in np.logspace(-3.3, 0, 200):
            w.write(f"{p:.6f} {tpr*p/(tpr*p+fpr*(1-p)):.6f}\n")
    print(f"wrote out/ppv.dat  (TPR={tpr:.3f}, FPR={fpr:.4f})")


if __name__ == "__main__":
    main()
