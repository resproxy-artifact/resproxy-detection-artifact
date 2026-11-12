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
set arrow from 10,0 to 10,1.05 nohead lw 2 lc rgb "#888888" dt 4
set label "t = 10 ms" at 20,0.5 font "Helvetica, 11" tc rgb "#888888"
plot 'data/cdf_provider_direct.dat' using 1:2 title "Direct (550)" \
        with lines lw 3 lc rgb "#000000" dt 2, \
     'data/cdf_provider_brightdata.dat' using 1:2 title "BrightData (6142)" \
        with lines ls 2 lw 2.5 dt 1, \
     'data/cdf_provider_brightdata_mobile.dat' using 1:2 title "BD Mobile (304)" \
        with lines ls 2 lw 2.5 dt 2, \
     'data/cdf_provider_brightdata_isp.dat' using 1:2 title "BD ISP (358)" \
        with lines ls 2 lw 2.5 dt 3, \
     'data/cdf_provider_soax.dat' using 1:2 title "SOAX (6350)" \
        with lines ls 1 lw 2.5 dt 1, \
     'data/cdf_provider_oxylabs.dat' using 1:2 title "Oxylabs Resi (3388)" \
        with lines ls 3 lw 2.5 dt 1, \
     'data/cdf_provider_oxylabs_mobile.dat' using 1:2 title "Oxylabs Mobile (3422)" \
        with lines ls 3 lw 2.5 dt 2, \
     'data/cdf_provider_oxylabs_isp.dat' using 1:2 title "Oxylabs ISP (3425)" \
        with lines ls 3 lw 2.5 dt 3, \
     'data/cdf_provider_iproyal.dat' using 1:2 title "IPRoyal (6238)" \
        with lines ls 4 lw 2.5 dt 1, \
     'data/cdf_provider_netnut.dat' using 1:2 title "NetNut (5902)" \
        with lines ls 5 lw 2.5 dt 1
