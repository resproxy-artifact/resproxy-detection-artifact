load 'style.gnu'
set terminal postscript enhanced color eps font "Helvetica, 14"
set size 0.6, 0.4
set output '../figures/labproxy_gap_vs_rtt.eps'

set xlabel "{/Helvetica-Bold TCP RTT to Proxy (ms)}"
set ylabel "{/Helvetica-Bold ACK{/Symbol \256}ClientHello Gap (ms)}"
set key top left samplen 2 font "Helvetica, 12"

set xrange [0:170]
set yrange [0:180]
set xtics 40
set ytics 40
set grid ytics

f(x) = 0.9744 * x + 7.1632

plot 'data/labproxy_gap_vs_rtt.dat' using 1:2 title "Measured" \
        with points pt 7 ps 1.0 lc rgb "#5f97d2" lw 3, \
     f(x) title sprintf("y = 0.97x + 7.2 (R^2 = 0.953)") \
        with lines ls 1 lw 3 dt 2
