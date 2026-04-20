load 'style.gnu'
set terminal postscript enhanced color eps font "Helvetica, 14"
set size 0.6, 0.4
set output '../figures/timing_cdf_multiserver.eps'

set xlabel "{/Helvetica-Bold TCP-to-TLS Gap (ms)}"
set ylabel "{/Helvetica-Bold CDF}"
set key right bottom samplen 2 font "Helvetica, 12"

set xrange [0:500]
set yrange [0:1.05]
set xtics 100
set ytics 0.2
set grid ytics

# Threshold line at 10 ms
set arrow from 10,0 to 10,1.05 nohead lw 2 lc rgb "#888888" dt 4
set label "t = 10 ms" at 16,0.5 font "Helvetica, 11" tc rgb "#888888"

plot 'data/cdf_direct_multi.dat' using 1:2 title "Direct (RIPE Atlas)" \
        with lines ls 3 lw 3, \
     'data/cdf_multiserver_us.dat' using 1:2 title "Proxied — US" \
        with lines ls 1 lw 3, \
     'data/cdf_multiserver_ap.dat' using 1:2 title "Proxied — Tokyo" \
        with lines ls 2 lw 3, \
     'data/cdf_multiserver_eu.dat' using 1:2 title "Proxied — Paris" \
        with lines lc rgb "#984EA3" lw 3 dt 1, \
     'data/cdf_multiserver_sa.dat' using 1:2 title "Proxied — S{/Symbol \343}o Paulo" \
        with lines lc rgb "#000000" lw 3 dt 2
