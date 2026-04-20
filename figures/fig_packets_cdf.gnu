load 'style.gnu'
set terminal postscript enhanced color eps font "Helvetica, 14"
set size 0.6, 0.4
set output '../figures/packets_cdf_ours.eps'

set xlabel "{/Helvetica-Bold Packets to Decision}"
set ylabel "{/Helvetica-Bold CDF}"
set key right bottom samplen 2 font "Helvetica, 12"

set xrange [0:20]
set yrange [0:1.05]
set xtics 4
set ytics 0.2
set grid ytics

# Median annotation
set arrow from 4,0 to 4,0.95 nohead lw 1.5 lc rgb "#888888" dt 4
set label "median = 4" at 4.5,0.5 font "Helvetica, 10" tc rgb "#888888"

plot 'data/packets_clean_our.dat' using 1:2 title "Our Method" \
        with lines ls 2 lw 3
