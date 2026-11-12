# PPV versus prevalence at the measured operating point (fig 8, usx08
# fig:ppv). Paper-standard style: style.gnu + size 0.6,0.4, Helvetica 14,
# bold axis labels. Data: data/ppv.dat (revision/analysis/out/ppv.dat,
# TPR/FPR at the published 10 ms threshold).
load 'style.gnu'
set terminal postscript enhanced color eps font "Helvetica, 14"
set size 0.6, 0.4
set output '../figures/fig_ppv.eps'

set xlabel "{/Helvetica-Bold Prevalence of Tunnelled Traffic}"
set ylabel "{/Helvetica-Bold PPV}"
set key off

set logscale x
set xrange [0.0005:1]
set yrange [0:1]
set ytics 0.25
set format x "%g"
set grid ytics

plot 'data/ppv.dat' using 1:2 with lines ls 1 lw 3
