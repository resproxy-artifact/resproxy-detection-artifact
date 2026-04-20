load 'style.gnu'
set terminal postscript enhanced color eps font "Helvetica, 14"
set size 0.6, 0.4
set output '../figures/labproxy_evasion_cdf.eps'

set xlabel "{/Helvetica-Bold TCP-to-TLS Gap (ms)}"
set ylabel "{/Helvetica-Bold CDF}"
set key right bottom samplen 2 font "Helvetica, 12"

set xrange [0:250]
set yrange [0:1.05]
set xtics 50
set ytics 0.2
set grid ytics

# Threshold line at 10 ms
set arrow from 10,0 to 10,1.05 nohead lw 2 lc rgb "#888888" dt 4
set label "t = 10 ms" at 16,0.5 font "Helvetica, 11" tc rgb "#888888"

plot 'data/labproxy_cdf_direct.dat' using 1:2 title "Direct" \
        with lines ls 3 lw 3, \
     'data/labproxy_cdf_normal_all.dat' using 1:2 title "Normal proxy" \
        with lines ls 1 lw 3, \
     'data/labproxy_cdf_speculative_all.dat' using 1:2 title "Speculative proxy" \
        with lines ls 2 lw 3 dt 2
