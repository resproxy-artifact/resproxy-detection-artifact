load 'style.gnu'
set terminal postscript enhanced color eps font "Helvetica, 14"
set size 0.6, 0.4
set output '../figures/roc_ours.eps'

set xlabel "{/Helvetica-Bold False Positive Rate}"
set ylabel "{/Helvetica-Bold True Positive Rate}"
set key right bottom samplen 2 font "Helvetica, 12"

set xrange [0:1]
set yrange [0:1]
set xtics 0.2
set ytics 0.2
set grid ytics

# Operating point annotation
set arrow from 0.007,0 to 0.007,0.968 nohead lw 1.5 lc rgb "#888888" dt 4
set label "t = 10 ms" at 0.03,0.5 font "Helvetica, 10" tc rgb "#888888"

plot x title "" with lines lw 1 lc rgb "#bbbbbb" dt 4, \
     'data/roc_clean_our.dat' using 1:2 title "Our Method (AUC = 0.974)" \
        with lines ls 2 lw 3
