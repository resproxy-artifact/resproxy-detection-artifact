load 'style.gnu'
set terminal postscript enhanced color eps font "Helvetica, 14"
set size 0.9, 0.55
set output '../figures/timing_cdf_providers.eps'

set xlabel "{/Helvetica-Bold TCP-to-TLS Gap (ms)}"
set ylabel "{/Helvetica-Bold CDF}"
set key right bottom samplen 2 font "Helvetica, 10" spacing 1.1 maxrows 5

set xrange [0:600]
set yrange [0:1.05]
set xtics 100
set ytics 0.2
set grid ytics

# Threshold line at 10 ms
set arrow from 10,0 to 10,1.05 nohead lw 2 lc rgb "#888888" dt 4
set label "t = 10 ms" at 20,0.5 font "Helvetica, 11" tc rgb "#888888"

# Provider family = color; product tier (resi/mobile/ISP) = dash pattern.
# ls 1=blue, ls 2=red, ls 3=green, ls 4=purple, ls 5=orange (from style.gnu)
plot 'data/cdf_provider_direct.dat' using 1:2 title "Direct (Chrome, N=100)" \
        with lines lw 3 lc rgb "#000000" dt 2, \
     'data/cdf_provider_brightdata.dat' using 1:2 title "BrightData (5501)" \
        with lines ls 2 lw 2.5 dt 1, \
     'data/cdf_provider_brightdata_mobile.dat' using 1:2 title "BD Mobile (1580)" \
        with lines ls 2 lw 2.5 dt 2, \
     'data/cdf_provider_brightdata_isp.dat' using 1:2 title "BD ISP (2217)" \
        with lines ls 2 lw 2.5 dt 3, \
     'data/cdf_provider_soax.dat' using 1:2 title "SOAX (5595)" \
        with lines ls 1 lw 2.5 dt 1, \
     'data/cdf_provider_oxylabs.dat' using 1:2 title "Oxylabs Resi (2936)" \
        with lines ls 3 lw 2.5 dt 1, \
     'data/cdf_provider_oxylabs_mobile.dat' using 1:2 title "Oxylabs Mobile (2968)" \
        with lines ls 3 lw 2.5 dt 2, \
     'data/cdf_provider_oxylabs_isp.dat' using 1:2 title "Oxylabs ISP (2967)" \
        with lines ls 3 lw 2.5 dt 3, \
     'data/cdf_provider_iproyal.dat' using 1:2 title "IPRoyal (5753)" \
        with lines ls 4 lw 2.5 dt 1, \
     'data/cdf_provider_netnut.dat' using 1:2 title "NetNut (5500)" \
        with lines ls 5 lw 2.5 dt 1
