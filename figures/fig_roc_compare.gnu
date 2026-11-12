# ROC of both origin-computable detectors on identical connections (fig 3,
# usx06 fig:roc-compare). Paper-standard style: style.gnu + size 0.6,0.4,
# Helvetica 14, bold axis labels -- matches fig_causal / timing_cdf.
# Data: data/roc_compare_{ours,badpass}.dat  (from revision/analysis/out/roc/,
# produced by scripts/evaluate.py on dataset.jsonl).
# Axes clipped to the operationally relevant low-FPR corner.
load 'style.gnu'
set terminal postscript enhanced color eps font "Helvetica, 14"
set size 0.6, 0.4
set output '../figures/fig_roc_multi.eps'

set xlabel "{/Helvetica-Bold False Positive Rate}"
set ylabel "{/Helvetica-Bold True Positive Rate}"
set key bottom right samplen 2 font "Helvetica, 12"

set xrange [0:0.05]
set yrange [0.90:1.0]
set xtics 0.01
set ytics 0.05
set format x "%.2f"
set format y "%.2f"
set grid ytics

plot 'data/roc_compare_ours.dat'    using 1:2 title "Ours (4 pkt)" \
        with lines ls 1 lw 3, \
     'data/roc_compare_badpass.dat' using 1:2 title "BADPASS (10 pkt)" \
        with lines ls 2 lw 3 dt 2
