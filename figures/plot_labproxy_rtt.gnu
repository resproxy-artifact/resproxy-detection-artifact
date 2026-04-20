load 'style.gnu'
set terminal postscript enhanced color eps font "Helvetica, 14"
set size 0.6, 0.4
set output '../figures/labproxy_gap_vs_rtt.eps'

set xlabel "{/Helvetica-Bold TCP RTT to Proxy (ms)}"
set ylabel "{/Helvetica-Bold ACK{/Symbol \256}ClientHello Gap (ms)}"
set key top left samplen 2 font "Helvetica, 11"

set grid ytics

f(x) = 0.9933 * x + 2.8837

plot 'data/labproxy_gap_vs_rtt.dat' using 1:2 title "Normal proxy" \
        with points ls 1 pt 7 ps 0.6, \
     f(x) title sprintf("y = %.2fx + %.1f (R^2=%.3f)", 0.9933, 2.8837, 0.9927) \
        with lines ls 2 lw 2 dt 2
