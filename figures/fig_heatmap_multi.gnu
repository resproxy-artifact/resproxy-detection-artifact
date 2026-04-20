load 'style.gnu'
set terminal postscript enhanced color eps font "Helvetica, 12"
set size 1.3, 0.85
set output '../figures/heatmap_multi_provider.eps'

set multiplot layout 2,3 margins 0.08,0.92,0.08,0.92 spacing 0.04,0.06

# --- Panel 1: brightdata ---
set xrange [-0.5:3.5]
set yrange [-0.5:14.5]
set xtics ("" 0, "" 1, "" 2, "" 3)
set ytics ("US" 0, "CA" 1, "MX" 2, "GB" 3, "DE" 4, "FR" 5, "RU" 6, "BR" 7, "JP" 8, "SG" 9, "ID" 10, "KR" 11, "IN" 12, "AU" 13, "ZA" 14) font "Helvetica, 9"
set title "{/Helvetica-Bold BrightData (Super-proxy)}" font "Helvetica-Bold, 10"
unset key
unset colorbox
unset grid
set arrow from -0.5,2.5 to 3.5,2.5 nohead lw 0.8 lc rgb "#aaaaaa" front
set arrow from -0.5,6.5 to 3.5,6.5 nohead lw 0.8 lc rgb "#aaaaaa" front
set arrow from -0.5,7.5 to 3.5,7.5 nohead lw 0.8 lc rgb "#aaaaaa" front
set arrow from -0.5,12.5 to 3.5,12.5 nohead lw 0.8 lc rgb "#aaaaaa" front
set arrow from -0.5,13.5 to 3.5,13.5 nohead lw 0.8 lc rgb "#aaaaaa" front
set object 1 rect from -0.48,-0.45 to 0.48,0.45 fc rgb "#82a8d0" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 1000 "103" at 0,0 center font "Helvetica, 7" tc rgb "#333333" front
set object 2 rect from 0.52,-0.45 to 1.48,0.45 fc rgb "#81a8d0" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 1001 "103" at 1,0 center font "Helvetica, 7" tc rgb "#333333" front
set object 3 rect from 1.52,-0.45 to 2.48,0.45 fc rgb "#9ebcdb" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 1002 "128" at 2,0 center font "Helvetica, 7" tc rgb "#333333" front
set object 4 rect from 2.52,-0.45 to 3.48,0.45 fc rgb "#b6cce3" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 1003 "148" at 3,0 center font "Helvetica, 7" tc rgb "#333333" front
set object 5 rect from -0.48,0.55 to 0.48,1.45 fc rgb "#6f9bc9" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 1004 "87" at 0,1 center font "Helvetica, 7" tc rgb "#333333" front
set object 6 rect from 0.52,0.55 to 1.48,1.45 fc rgb "#6695c5" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 1005 "80" at 1,1 center font "Helvetica, 7" tc rgb "#333333" front
set object 7 rect from 1.52,0.55 to 2.48,1.45 fc rgb "#5b8ec1" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 1006 "70" at 2,1 center font "Helvetica, 7" tc rgb "#333333" front
set object 8 rect from 2.52,0.55 to 3.48,1.45 fc rgb "#6c9ac8" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 1007 "85" at 3,1 center font "Helvetica, 7" tc rgb "#333333" front
set object 9 rect from -0.48,1.55 to 0.48,2.45 fc rgb "#b5cce3" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 1008 "147" at 0,2 center font "Helvetica, 7" tc rgb "#333333" front
set object 10 rect from 0.52,1.55 to 1.48,2.45 fc rgb "#b2cae2" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 1009 "144" at 1,2 center font "Helvetica, 7" tc rgb "#333333" front
set object 11 rect from 1.52,1.55 to 2.48,2.45 fc rgb "#acc6e0" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 1010 "139" at 2,2 center font "Helvetica, 7" tc rgb "#333333" front
set object 12 rect from 2.52,1.55 to 3.48,2.45 fc rgb "#a5c0dd" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 1011 "133" at 3,2 center font "Helvetica, 7" tc rgb "#333333" front
set object 13 rect from -0.48,2.55 to 0.48,3.45 fc rgb "#92b4d6" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 1012 "117" at 0,3 center font "Helvetica, 7" tc rgb "#333333" front
set object 14 rect from 0.52,2.55 to 1.48,3.45 fc rgb "#8db0d4" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 1013 "113" at 1,3 center font "Helvetica, 7" tc rgb "#333333" front
set object 15 rect from 1.52,2.55 to 2.48,3.45 fc rgb "#8eb1d4" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 1014 "114" at 2,3 center font "Helvetica, 7" tc rgb "#333333" front
set object 16 rect from 2.52,2.55 to 3.48,3.45 fc rgb "#87acd2" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 1015 "108" at 3,3 center font "Helvetica, 7" tc rgb "#333333" front
set object 17 rect from -0.48,3.55 to 0.48,4.45 fc rgb "#9cbada" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 1016 "125" at 0,4 center font "Helvetica, 7" tc rgb "#333333" front
set object 18 rect from 0.52,3.55 to 1.48,4.45 fc rgb "#a1bedc" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 1017 "130" at 1,4 center font "Helvetica, 7" tc rgb "#333333" front
set object 19 rect from 1.52,3.55 to 2.48,4.45 fc rgb "#a0bedb" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 1018 "129" at 2,4 center font "Helvetica, 7" tc rgb "#333333" front
set object 20 rect from 2.52,3.55 to 3.48,4.45 fc rgb "#a4c0dd" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 1019 "132" at 3,4 center font "Helvetica, 7" tc rgb "#333333" front
set object 21 rect from -0.48,4.55 to 0.48,5.45 fc rgb "#8eb1d4" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 1020 "114" at 0,5 center font "Helvetica, 7" tc rgb "#333333" front
set object 22 rect from 0.52,4.55 to 1.48,5.45 fc rgb "#92b4d6" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 1021 "117" at 1,5 center font "Helvetica, 7" tc rgb "#333333" front
set object 23 rect from 1.52,4.55 to 2.48,5.45 fc rgb "#87acd2" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 1022 "108" at 2,5 center font "Helvetica, 7" tc rgb "#333333" front
set object 24 rect from 2.52,4.55 to 3.48,5.45 fc rgb "#89aed3" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 1023 "110" at 3,5 center font "Helvetica, 7" tc rgb "#333333" front
set object 25 rect from -0.48,5.55 to 0.48,6.45 fc rgb "#f0f0f0" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 1024 "--" at 0,6 center font "Helvetica, 7" tc rgb "#999999" front
set object 26 rect from 0.52,5.55 to 1.48,6.45 fc rgb "#f0f0f0" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 1025 "--" at 1,6 center font "Helvetica, 7" tc rgb "#999999" front
set object 27 rect from 1.52,5.55 to 2.48,6.45 fc rgb "#f0f0f0" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 1026 "--" at 2,6 center font "Helvetica, 7" tc rgb "#999999" front
set object 28 rect from 2.52,5.55 to 3.48,6.45 fc rgb "#f0f0f0" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 1027 "--" at 3,6 center font "Helvetica, 7" tc rgb "#999999" front
set object 29 rect from -0.48,6.55 to 0.48,7.45 fc rgb "#f2f6fa" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 1028 "199" at 0,7 center font "Helvetica, 7" tc rgb "#333333" front
set object 30 rect from 0.52,6.55 to 1.48,7.45 fc rgb "#eef3f8" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 1029 "196" at 1,7 center font "Helvetica, 7" tc rgb "#333333" front
set object 31 rect from 1.52,6.55 to 2.48,7.45 fc rgb "#e5edf5" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 1030 "188" at 2,7 center font "Helvetica, 7" tc rgb "#333333" front
set object 32 rect from 2.52,6.55 to 3.48,7.45 fc rgb "#faeaea" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 1031 "227" at 3,7 center font "Helvetica, 7" tc rgb "#333333" front
set object 33 rect from -0.48,7.55 to 0.48,8.45 fc rgb "#eff4f9" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 1032 "197" at 0,8 center font "Helvetica, 7" tc rgb "#333333" front
set object 34 rect from 0.52,7.55 to 1.48,8.45 fc rgb "#f0f5f9" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 1033 "198" at 1,8 center font "Helvetica, 7" tc rgb "#333333" front
set object 35 rect from 1.52,7.55 to 2.48,8.45 fc rgb "#f3f7fa" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 1034 "200" at 2,8 center font "Helvetica, 7" tc rgb "#333333" front
set object 36 rect from 2.52,7.55 to 3.48,8.45 fc rgb "#f6f9fb" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 1035 "203" at 3,8 center font "Helvetica, 7" tc rgb "#333333" front
set object 37 rect from -0.48,8.55 to 0.48,9.45 fc rgb "#f7dfdf" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 1036 "236" at 0,9 center font "Helvetica, 7" tc rgb "#333333" front
set object 38 rect from 0.52,8.55 to 1.48,9.45 fc rgb "#e79597" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 1037 "297" at 1,9 center font "Helvetica, 7" tc rgb "#ffffff" front
set object 39 rect from 1.52,8.55 to 2.48,9.45 fc rgb "#f2c6c7" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 1038 "257" at 2,9 center font "Helvetica, 7" tc rgb "#333333" front
set object 40 rect from 2.52,8.55 to 3.48,9.45 fc rgb "#f2c7c8" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 1039 "256" at 3,9 center font "Helvetica, 7" tc rgb "#333333" front
set object 41 rect from -0.48,9.55 to 0.48,10.45 fc rgb "#e7989a" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 1040 "295" at 0,10 center font "Helvetica, 7" tc rgb "#ffffff" front
set object 42 rect from 0.52,9.55 to 1.48,10.45 fc rgb "#e58c8e" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 1041 "304" at 1,10 center font "Helvetica, 7" tc rgb "#ffffff" front
set object 43 rect from 1.52,9.55 to 2.48,10.45 fc rgb "#e89c9e" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 1042 "291" at 2,10 center font "Helvetica, 7" tc rgb "#ffffff" front
set object 44 rect from 2.52,9.55 to 3.48,10.45 fc rgb "#e99fa1" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 1043 "288" at 3,10 center font "Helvetica, 7" tc rgb "#ffffff" front
set object 45 rect from -0.48,10.55 to 0.48,11.45 fc rgb "#efbbbc" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 1044 "266" at 0,11 center font "Helvetica, 7" tc rgb "#333333" front
set object 46 rect from 0.52,10.55 to 1.48,11.45 fc rgb "#ecadaf" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 1045 "277" at 1,11 center font "Helvetica, 7" tc rgb "#333333" front
set object 47 rect from 1.52,10.55 to 2.48,11.45 fc rgb "#eeb4b6" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 1046 "271" at 2,11 center font "Helvetica, 7" tc rgb "#333333" front
set object 48 rect from 2.52,10.55 to 3.48,11.45 fc rgb "#edb1b2" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 1047 "274" at 3,11 center font "Helvetica, 7" tc rgb "#333333" front
set object 49 rect from -0.48,11.55 to 0.48,12.45 fc rgb "#df7376" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 1048 "325" at 0,12 center font "Helvetica, 7" tc rgb "#ffffff" front
set object 50 rect from 0.52,11.55 to 1.48,12.45 fc rgb "#e58f92" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 1049 "302" at 1,12 center font "Helvetica, 7" tc rgb "#ffffff" front
set object 51 rect from 1.52,11.55 to 2.48,12.45 fc rgb "#e4888b" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 1050 "307" at 2,12 center font "Helvetica, 7" tc rgb "#ffffff" front
set object 52 rect from 2.52,11.55 to 3.48,12.45 fc rgb "#e38587" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 1051 "310" at 3,12 center font "Helvetica, 7" tc rgb "#ffffff" front
set object 53 rect from -0.48,12.55 to 0.48,13.45 fc rgb "#eaa3a5" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 1052 "286" at 0,13 center font "Helvetica, 7" tc rgb "#ffffff" front
set object 54 rect from 0.52,12.55 to 1.48,13.45 fc rgb "#e38486" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 1053 "311" at 1,13 center font "Helvetica, 7" tc rgb "#ffffff" front
set object 55 rect from 1.52,12.55 to 2.48,13.45 fc rgb "#ecacae" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 1054 "278" at 2,13 center font "Helvetica, 7" tc rgb "#333333" front
set object 56 rect from 2.52,12.55 to 3.48,13.45 fc rgb "#eaa5a7" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 1055 "283" at 3,13 center font "Helvetica, 7" tc rgb "#ffffff" front
set object 57 rect from -0.48,13.55 to 0.48,14.45 fc rgb "#e0787b" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 1056 "321" at 0,14 center font "Helvetica, 7" tc rgb "#ffffff" front
set object 58 rect from 0.52,13.55 to 1.48,14.45 fc rgb "#e58f92" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 1057 "301" at 1,14 center font "Helvetica, 7" tc rgb "#ffffff" front
set object 59 rect from 1.52,13.55 to 2.48,14.45 fc rgb "#e48789" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 1058 "309" at 2,14 center font "Helvetica, 7" tc rgb "#ffffff" front
set object 60 rect from 2.52,13.55 to 3.48,14.45 fc rgb "#e27f82" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 1059 "315" at 3,14 center font "Helvetica, 7" tc rgb "#ffffff" front
plot NaN notitle

unset arrow
unset object
unset label
# --- Panel 2: soax ---
set xrange [-0.5:3.5]
set yrange [-0.5:14.5]
set xtics ("" 0, "" 1, "" 2, "" 3)
set ytics ("" 0, "" 1, "" 2, "" 3, "" 4, "" 5, "" 6, "" 7, "" 8, "" 9, "" 10, "" 11, "" 12, "" 13, "" 14) font "Helvetica, 9"
set title "{/Helvetica-Bold SOAX (Super-proxy)}" font "Helvetica-Bold, 10"
unset key
unset colorbox
unset grid
set arrow from -0.5,2.5 to 3.5,2.5 nohead lw 0.8 lc rgb "#aaaaaa" front
set arrow from -0.5,6.5 to 3.5,6.5 nohead lw 0.8 lc rgb "#aaaaaa" front
set arrow from -0.5,7.5 to 3.5,7.5 nohead lw 0.8 lc rgb "#aaaaaa" front
set arrow from -0.5,12.5 to 3.5,12.5 nohead lw 0.8 lc rgb "#aaaaaa" front
set arrow from -0.5,13.5 to 3.5,13.5 nohead lw 0.8 lc rgb "#aaaaaa" front
set object 1 rect from -0.48,-0.45 to 0.48,0.45 fc rgb "#a9c4df" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 2060 "137" at 0,0 center font "Helvetica, 7" tc rgb "#333333" front
set object 2 rect from 0.52,-0.45 to 1.48,0.45 fc rgb "#a9c3de" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 2061 "137" at 1,0 center font "Helvetica, 7" tc rgb "#333333" front
set object 3 rect from 1.52,-0.45 to 2.48,0.45 fc rgb "#a3bfdc" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 2062 "131" at 2,0 center font "Helvetica, 7" tc rgb "#333333" front
set object 4 rect from 2.52,-0.45 to 3.48,0.45 fc rgb "#97b7d8" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 2063 "122" at 3,0 center font "Helvetica, 7" tc rgb "#333333" front
set object 5 rect from -0.48,0.55 to 0.48,1.45 fc rgb "#abc5df" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 2064 "139" at 0,1 center font "Helvetica, 7" tc rgb "#333333" front
set object 6 rect from 0.52,0.55 to 1.48,1.45 fc rgb "#aac4df" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 2065 "137" at 1,1 center font "Helvetica, 7" tc rgb "#333333" front
set object 7 rect from 1.52,0.55 to 2.48,1.45 fc rgb "#acc6e0" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 2066 "140" at 2,1 center font "Helvetica, 7" tc rgb "#333333" front
set object 8 rect from 2.52,0.55 to 3.48,1.45 fc rgb "#abc5df" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 2067 "138" at 3,1 center font "Helvetica, 7" tc rgb "#333333" front
set object 9 rect from -0.48,1.55 to 0.48,2.45 fc rgb "#aac4df" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 2068 "138" at 0,2 center font "Helvetica, 7" tc rgb "#333333" front
set object 10 rect from 0.52,1.55 to 1.48,2.45 fc rgb "#aac4df" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 2069 "137" at 1,2 center font "Helvetica, 7" tc rgb "#333333" front
set object 11 rect from 1.52,1.55 to 2.48,2.45 fc rgb "#aac4df" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 2070 "137" at 2,2 center font "Helvetica, 7" tc rgb "#333333" front
set object 12 rect from 2.52,1.55 to 3.48,2.45 fc rgb "#adc6e0" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 2071 "140" at 3,2 center font "Helvetica, 7" tc rgb "#333333" front
set object 13 rect from -0.48,2.55 to 0.48,3.45 fc rgb "#aec7e0" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 2072 "141" at 0,3 center font "Helvetica, 7" tc rgb "#333333" front
set object 14 rect from 0.52,2.55 to 1.48,3.45 fc rgb "#adc6e0" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 2073 "140" at 1,3 center font "Helvetica, 7" tc rgb "#333333" front
set object 15 rect from 1.52,2.55 to 2.48,3.45 fc rgb "#b0c8e1" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 2074 "143" at 2,3 center font "Helvetica, 7" tc rgb "#333333" front
set object 16 rect from 2.52,2.55 to 3.48,3.45 fc rgb "#adc6e0" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 2075 "140" at 3,3 center font "Helvetica, 7" tc rgb "#333333" front
set object 17 rect from -0.48,3.55 to 0.48,4.45 fc rgb "#dd686b" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 2076 "334" at 0,4 center font "Helvetica, 7" tc rgb "#ffffff" front
set object 18 rect from 0.52,3.55 to 1.48,4.45 fc rgb "#95b6d7" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 2077 "120" at 1,4 center font "Helvetica, 7" tc rgb "#333333" front
set object 19 rect from 1.52,3.55 to 2.48,4.45 fc rgb "#dc676a" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 2078 "335" at 2,4 center font "Helvetica, 7" tc rgb "#ffffff" front
set object 20 rect from 2.52,3.55 to 3.48,4.45 fc rgb "#dc6468" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 2079 "337" at 3,4 center font "Helvetica, 7" tc rgb "#ffffff" front
set object 21 rect from -0.48,4.55 to 0.48,5.45 fc rgb "#e0797c" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 2080 "320" at 0,5 center font "Helvetica, 7" tc rgb "#ffffff" front
set object 22 rect from 0.52,4.55 to 1.48,5.45 fc rgb "#e0797b" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 2081 "320" at 1,5 center font "Helvetica, 7" tc rgb "#ffffff" front
set object 23 rect from 1.52,4.55 to 2.48,5.45 fc rgb "#e38587" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 2082 "310" at 2,5 center font "Helvetica, 7" tc rgb "#ffffff" front
set object 24 rect from 2.52,4.55 to 3.48,5.45 fc rgb "#df7275" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 2083 "325" at 3,5 center font "Helvetica, 7" tc rgb "#ffffff" front
set object 25 rect from -0.48,5.55 to 0.48,6.45 fc rgb "#e38487" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 2084 "311" at 0,6 center font "Helvetica, 7" tc rgb "#ffffff" front
set object 26 rect from 0.52,5.55 to 1.48,6.45 fc rgb "#abc5df" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 2085 "138" at 1,6 center font "Helvetica, 7" tc rgb "#333333" front
set object 27 rect from 1.52,5.55 to 2.48,6.45 fc rgb "#e79598" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 2086 "296" at 2,6 center font "Helvetica, 7" tc rgb "#ffffff" front
set object 28 rect from 2.52,5.55 to 3.48,6.45 fc rgb "#e27e81" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 2087 "316" at 3,6 center font "Helvetica, 7" tc rgb "#ffffff" front
set object 29 rect from -0.48,6.55 to 0.48,7.45 fc rgb "#bacfe5" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 2088 "151" at 0,7 center font "Helvetica, 7" tc rgb "#333333" front
set object 30 rect from 0.52,6.55 to 1.48,7.45 fc rgb "#adc6e0" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 2089 "140" at 1,7 center font "Helvetica, 7" tc rgb "#333333" front
set object 31 rect from 1.52,6.55 to 2.48,7.45 fc rgb "#b4cbe3" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 2090 "146" at 2,7 center font "Helvetica, 7" tc rgb "#333333" front
set object 32 rect from 2.52,6.55 to 3.48,7.45 fc rgb "#aec7e1" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 2091 "142" at 3,7 center font "Helvetica, 7" tc rgb "#333333" front
set object 33 rect from -0.48,7.55 to 0.48,8.45 fc rgb "#dc6367" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 2092 "338" at 0,8 center font "Helvetica, 7" tc rgb "#ffffff" front
set object 34 rect from 0.52,7.55 to 1.48,8.45 fc rgb "#fcf2f2" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 2093 "220" at 1,8 center font "Helvetica, 7" tc rgb "#333333" front
set object 35 rect from 1.52,7.55 to 2.48,8.45 fc rgb "#fefafa" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 2094 "214" at 2,8 center font "Helvetica, 7" tc rgb "#333333" front
set object 36 rect from 2.52,7.55 to 3.48,8.45 fc rgb "#dc676a" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 2095 "335" at 3,8 center font "Helvetica, 7" tc rgb "#ffffff" front
set object 37 rect from -0.48,8.55 to 0.48,9.45 fc rgb "#bbd0e5" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 2096 "152" at 0,9 center font "Helvetica, 7" tc rgb "#333333" front
set object 38 rect from 0.52,8.55 to 1.48,9.45 fc rgb "#e17b7e" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 2097 "318" at 1,9 center font "Helvetica, 7" tc rgb "#ffffff" front
set object 39 rect from 1.52,8.55 to 2.48,9.45 fc rgb "#e99da0" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 2098 "290" at 2,9 center font "Helvetica, 7" tc rgb "#ffffff" front
set object 40 rect from 2.52,8.55 to 3.48,9.45 fc rgb "#d9e5f1" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 2099 "178" at 3,9 center font "Helvetica, 7" tc rgb "#333333" front
set object 41 rect from -0.48,9.55 to 0.48,10.45 fc rgb "#aac4df" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 2100 "137" at 0,10 center font "Helvetica, 7" tc rgb "#333333" front
set object 42 rect from 0.52,9.55 to 1.48,10.45 fc rgb "#abc5df" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 2101 "139" at 1,10 center font "Helvetica, 7" tc rgb "#333333" front
set object 43 rect from 1.52,9.55 to 2.48,10.45 fc rgb "#abc5df" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 2102 "138" at 2,10 center font "Helvetica, 7" tc rgb "#333333" front
set object 44 rect from 2.52,9.55 to 3.48,10.45 fc rgb "#abc5df" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 2103 "139" at 3,10 center font "Helvetica, 7" tc rgb "#333333" front
set object 45 rect from -0.48,10.55 to 0.48,11.45 fc rgb "#9dbbda" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 2104 "126" at 0,11 center font "Helvetica, 7" tc rgb "#333333" front
set object 46 rect from 0.52,10.55 to 1.48,11.45 fc rgb "#e17c7f" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 2105 "317" at 1,11 center font "Helvetica, 7" tc rgb "#ffffff" front
set object 47 rect from 1.52,10.55 to 2.48,11.45 fc rgb "#c6d7e9" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 2106 "161" at 2,11 center font "Helvetica, 7" tc rgb "#333333" front
set object 48 rect from 2.52,10.55 to 3.48,11.45 fc rgb "#dc6669" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 2107 "335" at 3,11 center font "Helvetica, 7" tc rgb "#ffffff" front
set object 49 rect from -0.48,11.55 to 0.48,12.45 fc rgb "#adc6e0" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 2108 "140" at 0,12 center font "Helvetica, 7" tc rgb "#333333" front
set object 50 rect from 0.52,11.55 to 1.48,12.45 fc rgb "#f3cdce" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 2109 "251" at 1,12 center font "Helvetica, 7" tc rgb "#333333" front
set object 51 rect from 1.52,11.55 to 2.48,12.45 fc rgb "#acc6e0" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 2110 "140" at 2,12 center font "Helvetica, 7" tc rgb "#333333" front
set object 52 rect from 2.52,11.55 to 3.48,12.45 fc rgb "#b9cee4" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 2111 "150" at 3,12 center font "Helvetica, 7" tc rgb "#333333" front
set object 53 rect from -0.48,12.55 to 0.48,13.45 fc rgb "#b7cde4" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 2112 "149" at 0,13 center font "Helvetica, 7" tc rgb "#333333" front
set object 54 rect from 0.52,12.55 to 1.48,13.45 fc rgb "#aec7e0" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 2113 "141" at 1,13 center font "Helvetica, 7" tc rgb "#333333" front
set object 55 rect from 1.52,12.55 to 2.48,13.45 fc rgb "#b9cfe5" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 2114 "151" at 2,13 center font "Helvetica, 7" tc rgb "#333333" front
set object 56 rect from 2.52,12.55 to 3.48,13.45 fc rgb "#a4c0dd" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 2115 "133" at 3,13 center font "Helvetica, 7" tc rgb "#333333" front
set object 57 rect from -0.48,13.55 to 0.48,14.45 fc rgb "#db6164" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 2116 "340" at 0,14 center font "Helvetica, 7" tc rgb "#ffffff" front
set object 58 rect from 0.52,13.55 to 1.48,14.45 fc rgb "#e38588" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 2117 "310" at 1,14 center font "Helvetica, 7" tc rgb "#ffffff" front
set object 59 rect from 1.52,13.55 to 2.48,14.45 fc rgb "#dc6468" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 2118 "337" at 2,14 center font "Helvetica, 7" tc rgb "#ffffff" front
set object 60 rect from 2.52,13.55 to 3.48,14.45 fc rgb "#cb181d" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 2119 "401" at 3,14 center font "Helvetica, 7" tc rgb "#ffffff" front
plot NaN notitle

unset arrow
unset object
unset label
# --- Panel 3: iproyal ---
set xrange [-0.5:3.5]
set yrange [-0.5:14.5]
set xtics ("" 0, "" 1, "" 2, "" 3)
set ytics ("" 0, "" 1, "" 2, "" 3, "" 4, "" 5, "" 6, "" 7, "" 8, "" 9, "" 10, "" 11, "" 12, "" 13, "" 14) font "Helvetica, 9"
set title "{/Helvetica-Bold IPRoyal (P2P)}" font "Helvetica-Bold, 10"
unset key
unset colorbox
unset grid
set arrow from -0.5,2.5 to 3.5,2.5 nohead lw 0.8 lc rgb "#aaaaaa" front
set arrow from -0.5,6.5 to 3.5,6.5 nohead lw 0.8 lc rgb "#aaaaaa" front
set arrow from -0.5,7.5 to 3.5,7.5 nohead lw 0.8 lc rgb "#aaaaaa" front
set arrow from -0.5,12.5 to 3.5,12.5 nohead lw 0.8 lc rgb "#aaaaaa" front
set arrow from -0.5,13.5 to 3.5,13.5 nohead lw 0.8 lc rgb "#aaaaaa" front
set object 1 rect from -0.48,-0.45 to 0.48,0.45 fc rgb "#87acd2" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 3120 "108" at 0,0 center font "Helvetica, 7" tc rgb "#333333" front
set object 2 rect from 0.52,-0.45 to 1.48,0.45 fc rgb "#86abd1" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 3121 "107" at 1,0 center font "Helvetica, 7" tc rgb "#333333" front
set object 3 rect from 1.52,-0.45 to 2.48,0.45 fc rgb "#6695c5" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 3122 "79" at 2,0 center font "Helvetica, 7" tc rgb "#333333" front
set object 4 rect from 2.52,-0.45 to 3.48,0.45 fc rgb "#6796c6" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 3123 "80" at 3,0 center font "Helvetica, 7" tc rgb "#333333" front
set object 5 rect from -0.48,0.55 to 0.48,1.45 fc rgb "#6494c5" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 3124 "78" at 0,1 center font "Helvetica, 7" tc rgb "#333333" front
set object 6 rect from 0.52,0.55 to 1.48,1.45 fc rgb "#b7cde4" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 3125 "149" at 1,1 center font "Helvetica, 7" tc rgb "#333333" front
set object 7 rect from 1.52,0.55 to 2.48,1.45 fc rgb "#9bbad9" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 3126 "125" at 2,1 center font "Helvetica, 7" tc rgb "#333333" front
set object 8 rect from 2.52,0.55 to 3.48,1.45 fc rgb "#a1bedb" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 3127 "130" at 3,1 center font "Helvetica, 7" tc rgb "#333333" front
set object 9 rect from -0.48,1.55 to 0.48,2.45 fc rgb "#e3ecf4" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 3128 "187" at 0,2 center font "Helvetica, 7" tc rgb "#333333" front
set object 10 rect from 0.52,1.55 to 1.48,2.45 fc rgb "#d9e5f1" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 3129 "178" at 1,2 center font "Helvetica, 7" tc rgb "#333333" front
set object 11 rect from 1.52,1.55 to 2.48,2.45 fc rgb "#dfe9f3" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 3130 "183" at 2,2 center font "Helvetica, 7" tc rgb "#333333" front
set object 12 rect from 2.52,1.55 to 3.48,2.45 fc rgb "#e7eef6" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 3131 "190" at 3,2 center font "Helvetica, 7" tc rgb "#333333" front
set object 13 rect from -0.48,2.55 to 0.48,3.45 fc rgb "#e2ebf4" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 3132 "186" at 0,3 center font "Helvetica, 7" tc rgb "#333333" front
set object 14 rect from 0.52,2.55 to 1.48,3.45 fc rgb "#dae5f1" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 3133 "179" at 1,3 center font "Helvetica, 7" tc rgb "#333333" front
set object 15 rect from 1.52,2.55 to 2.48,3.45 fc rgb "#e7eef6" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 3134 "190" at 2,3 center font "Helvetica, 7" tc rgb "#333333" front
set object 16 rect from 2.52,2.55 to 3.48,3.45 fc rgb "#eef3f8" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 3135 "196" at 3,3 center font "Helvetica, 7" tc rgb "#333333" front
set object 17 rect from -0.48,3.55 to 0.48,4.45 fc rgb "#ecf2f8" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 3136 "194" at 0,4 center font "Helvetica, 7" tc rgb "#333333" front
set object 18 rect from 0.52,3.55 to 1.48,4.45 fc rgb "#f0f5f9" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 3137 "198" at 1,4 center font "Helvetica, 7" tc rgb "#333333" front
set object 19 rect from 1.52,3.55 to 2.48,4.45 fc rgb "#e9eff6" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 3138 "191" at 2,4 center font "Helvetica, 7" tc rgb "#333333" front
set object 20 rect from 2.52,3.55 to 3.48,4.45 fc rgb "#eaf0f7" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 3139 "192" at 3,4 center font "Helvetica, 7" tc rgb "#333333" front
set object 21 rect from -0.48,4.55 to 0.48,5.45 fc rgb "#eef3f8" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 3140 "196" at 0,5 center font "Helvetica, 7" tc rgb "#333333" front
set object 22 rect from 0.52,4.55 to 1.48,5.45 fc rgb "#dbe6f1" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 3141 "179" at 1,5 center font "Helvetica, 7" tc rgb "#333333" front
set object 23 rect from 1.52,4.55 to 2.48,5.45 fc rgb "#eff4f9" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 3142 "197" at 2,5 center font "Helvetica, 7" tc rgb "#333333" front
set object 24 rect from 2.52,4.55 to 3.48,5.45 fc rgb "#b8cee4" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 3143 "150" at 3,5 center font "Helvetica, 7" tc rgb "#333333" front
set object 25 rect from -0.48,5.55 to 0.48,6.45 fc rgb "#f8fafc" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 3144 "205" at 0,6 center font "Helvetica, 7" tc rgb "#333333" front
set object 26 rect from 0.52,5.55 to 1.48,6.45 fc rgb "#fefbfb" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 3145 "213" at 1,6 center font "Helvetica, 7" tc rgb "#333333" front
set object 27 rect from 1.52,5.55 to 2.48,6.45 fc rgb "#fdf8f8" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 3146 "215" at 2,6 center font "Helvetica, 7" tc rgb "#333333" front
set object 28 rect from 2.52,5.55 to 3.48,6.45 fc rgb "#e2ebf4" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 3147 "185" at 3,6 center font "Helvetica, 7" tc rgb "#333333" front
set object 29 rect from -0.48,6.55 to 0.48,7.45 fc rgb "#f0bfc0" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 3148 "262" at 0,7 center font "Helvetica, 7" tc rgb "#333333" front
set object 30 rect from 0.52,6.55 to 1.48,7.45 fc rgb "#f5d3d4" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 3149 "246" at 1,7 center font "Helvetica, 7" tc rgb "#333333" front
set object 31 rect from 1.52,6.55 to 2.48,7.45 fc rgb "#f7ddde" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 3150 "237" at 2,7 center font "Helvetica, 7" tc rgb "#333333" front
set object 32 rect from 2.52,6.55 to 3.48,7.45 fc rgb "#f7ddde" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 3151 "238" at 3,7 center font "Helvetica, 7" tc rgb "#333333" front
set object 33 rect from -0.48,7.55 to 0.48,8.45 fc rgb "#d54549" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 3152 "363" at 0,8 center font "Helvetica, 7" tc rgb "#ffffff" front
set object 34 rect from 0.52,7.55 to 1.48,8.45 fc rgb "#da5d60" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 3153 "343" at 1,8 center font "Helvetica, 7" tc rgb "#ffffff" front
set object 35 rect from 1.52,7.55 to 2.48,8.45 fc rgb "#cd2328" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 3154 "390" at 2,8 center font "Helvetica, 7" tc rgb "#ffffff" front
set object 36 rect from 2.52,7.55 to 3.48,8.45 fc rgb "#dc6467" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 3155 "337" at 3,8 center font "Helvetica, 7" tc rgb "#ffffff" front
set object 37 rect from -0.48,8.55 to 0.48,9.45 fc rgb "#de6f72" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 3156 "328" at 0,9 center font "Helvetica, 7" tc rgb "#ffffff" front
set object 38 rect from 0.52,8.55 to 1.48,9.45 fc rgb "#e17b7e" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 3157 "318" at 1,9 center font "Helvetica, 7" tc rgb "#ffffff" front
set object 39 rect from 1.52,8.55 to 2.48,9.45 fc rgb "#e28083" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 3158 "314" at 2,9 center font "Helvetica, 7" tc rgb "#ffffff" front
set object 40 rect from 2.52,8.55 to 3.48,9.45 fc rgb "#e17b7e" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 3159 "318" at 3,9 center font "Helvetica, 7" tc rgb "#ffffff" front
set object 41 rect from -0.48,9.55 to 0.48,10.45 fc rgb "#d9585b" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 3160 "347" at 0,10 center font "Helvetica, 7" tc rgb "#ffffff" front
set object 42 rect from 0.52,9.55 to 1.48,10.45 fc rgb "#e48b8d" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 3161 "305" at 1,10 center font "Helvetica, 7" tc rgb "#ffffff" front
set object 43 rect from 1.52,9.55 to 2.48,10.45 fc rgb "#df7477" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 3162 "324" at 2,10 center font "Helvetica, 7" tc rgb "#ffffff" front
set object 44 rect from 2.52,9.55 to 3.48,10.45 fc rgb "#e17c7f" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 3163 "318" at 3,10 center font "Helvetica, 7" tc rgb "#ffffff" front
set object 45 rect from -0.48,10.55 to 0.48,11.45 fc rgb "#cb181d" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 3164 "402" at 0,11 center font "Helvetica, 7" tc rgb "#ffffff" front
set object 46 rect from 0.52,10.55 to 1.48,11.45 fc rgb "#d5484c" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 3165 "360" at 1,11 center font "Helvetica, 7" tc rgb "#ffffff" front
set object 47 rect from 1.52,10.55 to 2.48,11.45 fc rgb "#da5c60" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 3166 "343" at 2,11 center font "Helvetica, 7" tc rgb "#ffffff" front
set object 48 rect from 2.52,10.55 to 3.48,11.45 fc rgb "#cd2227" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 3167 "391" at 3,11 center font "Helvetica, 7" tc rgb "#ffffff" front
set object 49 rect from -0.48,11.55 to 0.48,12.45 fc rgb "#cb181d" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 3168 "437" at 0,12 center font "Helvetica, 7" tc rgb "#ffffff" front
set object 50 rect from 0.52,11.55 to 1.48,12.45 fc rgb "#cb181d" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 3169 "407" at 1,12 center font "Helvetica, 7" tc rgb "#ffffff" front
set object 51 rect from 1.52,11.55 to 2.48,12.45 fc rgb "#cb181d" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 3170 "400" at 2,12 center font "Helvetica, 7" tc rgb "#ffffff" front
set object 52 rect from 2.52,11.55 to 3.48,12.45 fc rgb "#cb181d" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 3171 "425" at 3,12 center font "Helvetica, 7" tc rgb "#ffffff" front
set object 53 rect from -0.48,12.55 to 0.48,13.45 fc rgb "#d13237" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 3172 "378" at 0,13 center font "Helvetica, 7" tc rgb "#ffffff" front
set object 54 rect from 0.52,12.55 to 1.48,13.45 fc rgb "#d74d51" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 3173 "356" at 1,13 center font "Helvetica, 7" tc rgb "#ffffff" front
set object 55 rect from 1.52,12.55 to 2.48,13.45 fc rgb "#da5c60" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 3174 "343" at 2,13 center font "Helvetica, 7" tc rgb "#ffffff" front
set object 56 rect from 2.52,12.55 to 3.48,13.45 fc rgb "#db6063" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 3175 "341" at 3,13 center font "Helvetica, 7" tc rgb "#ffffff" front
set object 57 rect from -0.48,13.55 to 0.48,14.45 fc rgb "#d74f53" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 3176 "354" at 0,14 center font "Helvetica, 7" tc rgb "#ffffff" front
set object 58 rect from 0.52,13.55 to 1.48,14.45 fc rgb "#d75155" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 3177 "353" at 1,14 center font "Helvetica, 7" tc rgb "#ffffff" front
set object 59 rect from 1.52,13.55 to 2.48,14.45 fc rgb "#d44448" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 3178 "364" at 2,14 center font "Helvetica, 7" tc rgb "#ffffff" front
set object 60 rect from 2.52,13.55 to 3.48,14.45 fc rgb "#d74d51" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 3179 "356" at 3,14 center font "Helvetica, 7" tc rgb "#ffffff" front
plot NaN notitle

unset arrow
unset object
unset label
# --- Panel 4: oxylabs ---
set xrange [-0.5:3.5]
set yrange [-0.5:14.5]
set xtics ("VA" 0, "TK" 1, "PA" 2, "SP" 3) font "Helvetica, 9"
set ytics ("US" 0, "CA" 1, "MX" 2, "GB" 3, "DE" 4, "FR" 5, "RU" 6, "BR" 7, "JP" 8, "SG" 9, "ID" 10, "KR" 11, "IN" 12, "AU" 13, "ZA" 14) font "Helvetica, 9"
set title "{/Helvetica-Bold Oxylabs (Residential)}" font "Helvetica-Bold, 10"
unset key
unset colorbox
unset grid
set arrow from -0.5,2.5 to 3.5,2.5 nohead lw 0.8 lc rgb "#aaaaaa" front
set arrow from -0.5,6.5 to 3.5,6.5 nohead lw 0.8 lc rgb "#aaaaaa" front
set arrow from -0.5,7.5 to 3.5,7.5 nohead lw 0.8 lc rgb "#aaaaaa" front
set arrow from -0.5,12.5 to 3.5,12.5 nohead lw 0.8 lc rgb "#aaaaaa" front
set arrow from -0.5,13.5 to 3.5,13.5 nohead lw 0.8 lc rgb "#aaaaaa" front
set object 1 rect from -0.48,-0.45 to 0.48,0.45 fc rgb "#87acd2" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 4180 "108" at 0,0 center font "Helvetica, 7" tc rgb "#333333" front
set object 2 rect from 0.52,-0.45 to 1.48,0.45 fc rgb "#6897c6" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 4181 "81" at 1,0 center font "Helvetica, 7" tc rgb "#333333" front
set object 3 rect from 1.52,-0.45 to 2.48,0.45 fc rgb "#5a8dc1" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 4182 "69" at 2,0 center font "Helvetica, 7" tc rgb "#333333" front
set object 4 rect from 2.52,-0.45 to 3.48,0.45 fc rgb "#5389bf" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 4183 "64" at 3,0 center font "Helvetica, 7" tc rgb "#333333" front
set object 5 rect from -0.48,0.55 to 0.48,1.45 fc rgb "#5b8ec1" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 4184 "70" at 0,1 center font "Helvetica, 7" tc rgb "#333333" front
set object 6 rect from 0.52,0.55 to 1.48,1.45 fc rgb "#5086bd" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 4185 "61" at 1,1 center font "Helvetica, 7" tc rgb "#333333" front
set object 7 rect from 1.52,0.55 to 2.48,1.45 fc rgb "#4c84bc" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 4186 "58" at 2,1 center font "Helvetica, 7" tc rgb "#333333" front
set object 8 rect from 2.52,0.55 to 3.48,1.45 fc rgb "#5b8ec1" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 4187 "70" at 3,1 center font "Helvetica, 7" tc rgb "#333333" front
set object 9 rect from -0.48,1.55 to 0.48,2.45 fc rgb "#8fb2d5" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 4188 "114" at 0,2 center font "Helvetica, 7" tc rgb "#333333" front
set object 10 rect from 0.52,1.55 to 1.48,2.45 fc rgb "#95b5d7" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 4189 "119" at 1,2 center font "Helvetica, 7" tc rgb "#333333" front
set object 11 rect from 1.52,1.55 to 2.48,2.45 fc rgb "#9cbada" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 4190 "126" at 2,2 center font "Helvetica, 7" tc rgb "#333333" front
set object 12 rect from 2.52,1.55 to 3.48,2.45 fc rgb "#9fbddb" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 4191 "129" at 3,2 center font "Helvetica, 7" tc rgb "#333333" front
set object 13 rect from -0.48,2.55 to 0.48,3.45 fc rgb "#cadbeb" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 4192 "165" at 0,3 center font "Helvetica, 7" tc rgb "#333333" front
set object 14 rect from 0.52,2.55 to 1.48,3.45 fc rgb "#447eb9" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 4193 "50" at 1,3 center font "Helvetica, 7" tc rgb "#333333" front
set object 15 rect from 1.52,2.55 to 2.48,3.45 fc rgb "#f4f7fa" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 4194 "201" at 2,3 center font "Helvetica, 7" tc rgb "#333333" front
set object 16 rect from 2.52,2.55 to 3.48,3.45 fc rgb "#2d6eb0" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 4195 "31" at 3,3 center font "Helvetica, 7" tc rgb "#333333" front
set object 17 rect from -0.48,3.55 to 0.48,4.45 fc rgb "#cb181d" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 4196 "446" at 0,4 center font "Helvetica, 7" tc rgb "#ffffff" front
set object 18 rect from 0.52,3.55 to 1.48,4.45 fc rgb "#cb181d" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 4197 "477" at 1,4 center font "Helvetica, 7" tc rgb "#ffffff" front
set object 19 rect from 1.52,3.55 to 2.48,4.45 fc rgb "#cb181d" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 4198 "467" at 2,4 center font "Helvetica, 7" tc rgb "#ffffff" front
set object 20 rect from 2.52,3.55 to 3.48,4.45 fc rgb "#cb181d" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 4199 "445" at 3,4 center font "Helvetica, 7" tc rgb "#ffffff" front
set object 21 rect from -0.48,4.55 to 0.48,5.45 fc rgb "#d6e3f0" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 4200 "176" at 0,5 center font "Helvetica, 7" tc rgb "#333333" front
set object 22 rect from 0.52,4.55 to 1.48,5.45 fc rgb "#e6edf5" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 4201 "189" at 1,5 center font "Helvetica, 7" tc rgb "#333333" front
set object 23 rect from 1.52,4.55 to 2.48,5.45 fc rgb "#e5edf5" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 4202 "188" at 2,5 center font "Helvetica, 7" tc rgb "#333333" front
set object 24 rect from 2.52,4.55 to 3.48,5.45 fc rgb "#e0eaf3" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 4203 "184" at 3,5 center font "Helvetica, 7" tc rgb "#333333" front
set object 25 rect from -0.48,5.55 to 0.48,6.45 fc rgb "#f8e3e4" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 4204 "233" at 0,6 center font "Helvetica, 7" tc rgb "#333333" front
set object 26 rect from 0.52,5.55 to 1.48,6.45 fc rgb "#fefefe" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 4205 "210" at 1,6 center font "Helvetica, 7" tc rgb "#333333" front
set object 27 rect from 1.52,5.55 to 2.48,6.45 fc rgb "#f4d1d2" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 4206 "247" at 2,6 center font "Helvetica, 7" tc rgb "#333333" front
set object 28 rect from 2.52,5.55 to 3.48,6.45 fc rgb "#f5d6d7" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 4207 "244" at 3,6 center font "Helvetica, 7" tc rgb "#333333" front
set object 29 rect from -0.48,6.55 to 0.48,7.45 fc rgb "#efbcbd" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 4208 "265" at 0,7 center font "Helvetica, 7" tc rgb "#333333" front
set object 30 rect from 0.52,6.55 to 1.48,7.45 fc rgb "#f2c8c9" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 4209 "255" at 1,7 center font "Helvetica, 7" tc rgb "#333333" front
set object 31 rect from 1.52,6.55 to 2.48,7.45 fc rgb "#ecacae" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 4210 "278" at 2,7 center font "Helvetica, 7" tc rgb "#333333" front
set object 32 rect from 2.52,6.55 to 3.48,7.45 fc rgb "#f0bec0" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 4211 "263" at 3,7 center font "Helvetica, 7" tc rgb "#333333" front
set object 33 rect from -0.48,7.55 to 0.48,8.45 fc rgb "#cb181d" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 4212 "451" at 0,8 center font "Helvetica, 7" tc rgb "#ffffff" front
set object 34 rect from 0.52,7.55 to 1.48,8.45 fc rgb "#cb181d" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 4213 "434" at 1,8 center font "Helvetica, 7" tc rgb "#ffffff" front
set object 35 rect from 1.52,7.55 to 2.48,8.45 fc rgb "#cb181d" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 4214 "466" at 2,8 center font "Helvetica, 7" tc rgb "#ffffff" front
set object 36 rect from 2.52,7.55 to 3.48,8.45 fc rgb "#cb181d" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 4215 "426" at 3,8 center font "Helvetica, 7" tc rgb "#ffffff" front
set object 37 rect from -0.48,8.55 to 0.48,9.45 fc rgb "#eaa4a6" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 4216 "285" at 0,9 center font "Helvetica, 7" tc rgb "#ffffff" front
set object 38 rect from 0.52,8.55 to 1.48,9.45 fc rgb "#de6f73" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 4217 "328" at 1,9 center font "Helvetica, 7" tc rgb "#ffffff" front
set object 39 rect from 1.52,8.55 to 2.48,9.45 fc rgb "#e99ea0" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 4218 "289" at 2,9 center font "Helvetica, 7" tc rgb "#ffffff" front
set object 40 rect from 2.52,8.55 to 3.48,9.45 fc rgb "#eaa2a4" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 4219 "286" at 3,9 center font "Helvetica, 7" tc rgb "#ffffff" front
set object 41 rect from -0.48,9.55 to 0.48,10.45 fc rgb "#e27e81" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 4220 "316" at 0,10 center font "Helvetica, 7" tc rgb "#ffffff" front
set object 42 rect from 0.52,9.55 to 1.48,10.45 fc rgb "#e28285" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 4221 "312" at 1,10 center font "Helvetica, 7" tc rgb "#ffffff" front
set object 43 rect from 1.52,9.55 to 2.48,10.45 fc rgb "#de6e71" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 4222 "329" at 2,10 center font "Helvetica, 7" tc rgb "#ffffff" front
set object 44 rect from 2.52,9.55 to 3.48,10.45 fc rgb "#e4878a" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 4223 "308" at 3,10 center font "Helvetica, 7" tc rgb "#ffffff" front
set object 45 rect from -0.48,10.55 to 0.48,11.45 fc rgb "#cb181d" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 4224 "435" at 0,11 center font "Helvetica, 7" tc rgb "#ffffff" front
set object 46 rect from 0.52,10.55 to 1.48,11.45 fc rgb "#cb181d" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 4225 "448" at 1,11 center font "Helvetica, 7" tc rgb "#ffffff" front
set object 47 rect from 1.52,10.55 to 2.48,11.45 fc rgb "#cb181d" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 4226 "442" at 2,11 center font "Helvetica, 7" tc rgb "#ffffff" front
set object 48 rect from 2.52,10.55 to 3.48,11.45 fc rgb "#cb181d" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 4227 "445" at 3,11 center font "Helvetica, 7" tc rgb "#ffffff" front
set object 49 rect from -0.48,11.55 to 0.48,12.45 fc rgb "#cb181d" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 4228 "450" at 0,12 center font "Helvetica, 7" tc rgb "#ffffff" front
set object 50 rect from 0.52,11.55 to 1.48,12.45 fc rgb "#cb181d" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 4229 "425" at 1,12 center font "Helvetica, 7" tc rgb "#ffffff" front
set object 51 rect from 1.52,11.55 to 2.48,12.45 fc rgb "#cb181d" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 4230 "487" at 2,12 center font "Helvetica, 7" tc rgb "#ffffff" front
set object 52 rect from 2.52,11.55 to 3.48,12.45 fc rgb "#cb181d" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 4231 "406" at 3,12 center font "Helvetica, 7" tc rgb "#ffffff" front
set object 53 rect from -0.48,12.55 to 0.48,13.45 fc rgb "#cb181d" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 4232 "450" at 0,13 center font "Helvetica, 7" tc rgb "#ffffff" front
set object 54 rect from 0.52,12.55 to 1.48,13.45 fc rgb "#cb181d" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 4233 "462" at 1,13 center font "Helvetica, 7" tc rgb "#ffffff" front
set object 55 rect from 1.52,12.55 to 2.48,13.45 fc rgb "#cb181d" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 4234 "447" at 2,13 center font "Helvetica, 7" tc rgb "#ffffff" front
set object 56 rect from 2.52,12.55 to 3.48,13.45 fc rgb "#cb181d" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 4235 "439" at 3,13 center font "Helvetica, 7" tc rgb "#ffffff" front
set object 57 rect from -0.48,13.55 to 0.48,14.45 fc rgb "#db5f62" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 4236 "341" at 0,14 center font "Helvetica, 7" tc rgb "#ffffff" front
set object 58 rect from 0.52,13.55 to 1.48,14.45 fc rgb "#db6266" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 4237 "339" at 1,14 center font "Helvetica, 7" tc rgb "#ffffff" front
set object 59 rect from 1.52,13.55 to 2.48,14.45 fc rgb "#d95a5d" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 4238 "345" at 2,14 center font "Helvetica, 7" tc rgb "#ffffff" front
set object 60 rect from 2.52,13.55 to 3.48,14.45 fc rgb "#d9585b" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 4239 "347" at 3,14 center font "Helvetica, 7" tc rgb "#ffffff" front
plot NaN notitle

unset arrow
unset object
unset label
# --- Panel 5: oxylabs_isp ---
set xrange [-0.5:3.5]
set yrange [-0.5:14.5]
set xtics ("VA" 0, "TK" 1, "PA" 2, "SP" 3) font "Helvetica, 9"
set ytics ("" 0, "" 1, "" 2, "" 3, "" 4, "" 5, "" 6, "" 7, "" 8, "" 9, "" 10, "" 11, "" 12, "" 13, "" 14) font "Helvetica, 9"
set title "{/Helvetica-Bold Oxylabs (ISP)}" font "Helvetica-Bold, 10"
unset key
unset colorbox
unset grid
set arrow from -0.5,2.5 to 3.5,2.5 nohead lw 0.8 lc rgb "#aaaaaa" front
set arrow from -0.5,6.5 to 3.5,6.5 nohead lw 0.8 lc rgb "#aaaaaa" front
set arrow from -0.5,7.5 to 3.5,7.5 nohead lw 0.8 lc rgb "#aaaaaa" front
set arrow from -0.5,12.5 to 3.5,12.5 nohead lw 0.8 lc rgb "#aaaaaa" front
set arrow from -0.5,13.5 to 3.5,13.5 nohead lw 0.8 lc rgb "#aaaaaa" front
set object 1 rect from -0.48,-0.45 to 0.48,0.45 fc rgb "#bed2e7" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 5240 "155" at 0,0 center font "Helvetica, 7" tc rgb "#333333" front
set object 2 rect from 0.52,-0.45 to 1.48,0.45 fc rgb "#d3e1ee" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 5241 "173" at 1,0 center font "Helvetica, 7" tc rgb "#333333" front
set object 3 rect from 1.52,-0.45 to 2.48,0.45 fc rgb "#f5f8fb" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 5242 "202" at 2,0 center font "Helvetica, 7" tc rgb "#333333" front
set object 4 rect from 2.52,-0.45 to 3.48,0.45 fc rgb "#edf3f8" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 5243 "195" at 3,0 center font "Helvetica, 7" tc rgb "#333333" front
set object 5 rect from -0.48,0.55 to 0.48,1.45 fc rgb "#e7eef6" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 5244 "189" at 0,1 center font "Helvetica, 7" tc rgb "#333333" front
set object 6 rect from 0.52,0.55 to 1.48,1.45 fc rgb "#eaf0f7" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 5245 "192" at 1,1 center font "Helvetica, 7" tc rgb "#333333" front
set object 7 rect from 1.52,0.55 to 2.48,1.45 fc rgb "#f1f5f9" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 5246 "198" at 2,1 center font "Helvetica, 7" tc rgb "#333333" front
set object 8 rect from 2.52,0.55 to 3.48,1.45 fc rgb "#cadaeb" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 5247 "165" at 3,1 center font "Helvetica, 7" tc rgb "#333333" front
set object 9 rect from -0.48,1.55 to 0.48,2.45 fc rgb "#edf2f8" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 5248 "195" at 0,2 center font "Helvetica, 7" tc rgb "#333333" front
set object 10 rect from 0.52,1.55 to 1.48,2.45 fc rgb "#fbfcfd" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 5249 "207" at 1,2 center font "Helvetica, 7" tc rgb "#333333" front
set object 11 rect from 1.52,1.55 to 2.48,2.45 fc rgb "#f6f9fb" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 5250 "203" at 2,2 center font "Helvetica, 7" tc rgb "#333333" front
set object 12 rect from 2.52,1.55 to 3.48,2.45 fc rgb "#f4f7fb" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 5251 "201" at 3,2 center font "Helvetica, 7" tc rgb "#333333" front
set object 13 rect from -0.48,2.55 to 0.48,3.45 fc rgb "#e8eff6" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 5252 "191" at 0,3 center font "Helvetica, 7" tc rgb "#333333" front
set object 14 rect from 0.52,2.55 to 1.48,3.45 fc rgb "#e8eff6" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 5253 "191" at 1,3 center font "Helvetica, 7" tc rgb "#333333" front
set object 15 rect from 1.52,2.55 to 2.48,3.45 fc rgb "#fefefe" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 5254 "210" at 2,3 center font "Helvetica, 7" tc rgb "#333333" front
set object 16 rect from 2.52,2.55 to 3.48,3.45 fc rgb "#f1f5f9" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 5255 "198" at 3,3 center font "Helvetica, 7" tc rgb "#333333" front
set object 17 rect from -0.48,3.55 to 0.48,4.45 fc rgb "#d5e2ef" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 5256 "175" at 0,4 center font "Helvetica, 7" tc rgb "#333333" front
set object 18 rect from 0.52,3.55 to 1.48,4.45 fc rgb "#eef3f8" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 5257 "195" at 1,4 center font "Helvetica, 7" tc rgb "#333333" front
set object 19 rect from 1.52,3.55 to 2.48,4.45 fc rgb "#f4f8fb" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 5258 "201" at 2,4 center font "Helvetica, 7" tc rgb "#333333" front
set object 20 rect from 2.52,3.55 to 3.48,4.45 fc rgb "#f9fbfd" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 5259 "205" at 3,4 center font "Helvetica, 7" tc rgb "#333333" front
set object 21 rect from -0.48,4.55 to 0.48,5.45 fc rgb "#e7eef6" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 5260 "190" at 0,5 center font "Helvetica, 7" tc rgb "#333333" front
set object 22 rect from 0.52,4.55 to 1.48,5.45 fc rgb "#e2ebf4" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 5261 "186" at 1,5 center font "Helvetica, 7" tc rgb "#333333" front
set object 23 rect from 1.52,4.55 to 2.48,5.45 fc rgb "#f3f7fa" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 5262 "200" at 2,5 center font "Helvetica, 7" tc rgb "#333333" front
set object 24 rect from 2.52,4.55 to 3.48,5.45 fc rgb "#ebf1f7" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 5263 "193" at 3,5 center font "Helvetica, 7" tc rgb "#333333" front
set object 25 rect from -0.48,5.55 to 0.48,6.45 fc rgb "#f2f6fa" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 5264 "199" at 0,6 center font "Helvetica, 7" tc rgb "#333333" front
set object 26 rect from 0.52,5.55 to 1.48,6.45 fc rgb "#e3ecf4" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 5265 "187" at 1,6 center font "Helvetica, 7" tc rgb "#333333" front
set object 27 rect from 1.52,5.55 to 2.48,6.45 fc rgb "#f4f7fa" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 5266 "201" at 2,6 center font "Helvetica, 7" tc rgb "#333333" front
set object 28 rect from 2.52,5.55 to 3.48,6.45 fc rgb "#e7eef6" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 5267 "190" at 3,6 center font "Helvetica, 7" tc rgb "#333333" front
set object 29 rect from -0.48,6.55 to 0.48,7.45 fc rgb "#eef3f8" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 5268 "196" at 0,7 center font "Helvetica, 7" tc rgb "#333333" front
set object 30 rect from 0.52,6.55 to 1.48,7.45 fc rgb "#e3ecf4" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 5269 "187" at 1,7 center font "Helvetica, 7" tc rgb "#333333" front
set object 31 rect from 1.52,6.55 to 2.48,7.45 fc rgb "#fdf9f9" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 5270 "215" at 2,7 center font "Helvetica, 7" tc rgb "#333333" front
set object 32 rect from 2.52,6.55 to 3.48,7.45 fc rgb "#dae6f1" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 5271 "179" at 3,7 center font "Helvetica, 7" tc rgb "#333333" front
set object 33 rect from -0.48,7.55 to 0.48,8.45 fc rgb "#f2f6fa" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 5272 "199" at 0,8 center font "Helvetica, 7" tc rgb "#333333" front
set object 34 rect from 0.52,7.55 to 1.48,8.45 fc rgb "#eff4f9" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 5273 "197" at 1,8 center font "Helvetica, 7" tc rgb "#333333" front
set object 35 rect from 1.52,7.55 to 2.48,8.45 fc rgb "#f1f5f9" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 5274 "198" at 2,8 center font "Helvetica, 7" tc rgb "#333333" front
set object 36 rect from 2.52,7.55 to 3.48,8.45 fc rgb "#dce7f2" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 5275 "180" at 3,8 center font "Helvetica, 7" tc rgb "#333333" front
set object 37 rect from -0.48,8.55 to 0.48,9.45 fc rgb "#e0eaf3" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 5276 "184" at 0,9 center font "Helvetica, 7" tc rgb "#333333" front
set object 38 rect from 0.52,8.55 to 1.48,9.45 fc rgb "#e3ebf4" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 5277 "186" at 1,9 center font "Helvetica, 7" tc rgb "#333333" front
set object 39 rect from 1.52,8.55 to 2.48,9.45 fc rgb "#e1eaf3" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 5278 "184" at 2,9 center font "Helvetica, 7" tc rgb "#333333" front
set object 40 rect from 2.52,8.55 to 3.48,9.45 fc rgb "#eaf0f7" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 5279 "192" at 3,9 center font "Helvetica, 7" tc rgb "#333333" front
set object 41 rect from -0.48,9.55 to 0.48,10.45 fc rgb "#eef3f8" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 5280 "196" at 0,10 center font "Helvetica, 7" tc rgb "#333333" front
set object 42 rect from 0.52,9.55 to 1.48,10.45 fc rgb "#d6e3ef" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 5281 "175" at 1,10 center font "Helvetica, 7" tc rgb "#333333" front
set object 43 rect from 1.52,9.55 to 2.48,10.45 fc rgb "#f1f5f9" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 5282 "198" at 2,10 center font "Helvetica, 7" tc rgb "#333333" front
set object 44 rect from 2.52,9.55 to 3.48,10.45 fc rgb "#dfe9f3" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 5283 "183" at 3,10 center font "Helvetica, 7" tc rgb "#333333" front
set object 45 rect from -0.48,10.55 to 0.48,11.45 fc rgb "#f2f6fa" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 5284 "199" at 0,11 center font "Helvetica, 7" tc rgb "#333333" front
set object 46 rect from 0.52,10.55 to 1.48,11.45 fc rgb "#ebf1f7" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 5285 "193" at 1,11 center font "Helvetica, 7" tc rgb "#333333" front
set object 47 rect from 1.52,10.55 to 2.48,11.45 fc rgb "#f1f5fa" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 5286 "199" at 2,11 center font "Helvetica, 7" tc rgb "#333333" front
set object 48 rect from 2.52,10.55 to 3.48,11.45 fc rgb "#ebf1f7" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 5287 "193" at 3,11 center font "Helvetica, 7" tc rgb "#333333" front
set object 49 rect from -0.48,11.55 to 0.48,12.45 fc rgb "#dfe9f3" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 5288 "183" at 0,12 center font "Helvetica, 7" tc rgb "#333333" front
set object 50 rect from 0.52,11.55 to 1.48,12.45 fc rgb "#f7fafc" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 5289 "204" at 1,12 center font "Helvetica, 7" tc rgb "#333333" front
set object 51 rect from 1.52,11.55 to 2.48,12.45 fc rgb "#f3f7fa" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 5290 "201" at 2,12 center font "Helvetica, 7" tc rgb "#333333" front
set object 52 rect from 2.52,11.55 to 3.48,12.45 fc rgb "#e2ebf4" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 5291 "185" at 3,12 center font "Helvetica, 7" tc rgb "#333333" front
set object 53 rect from -0.48,12.55 to 0.48,13.45 fc rgb "#f1f5f9" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 5292 "198" at 0,13 center font "Helvetica, 7" tc rgb "#333333" front
set object 54 rect from 0.52,12.55 to 1.48,13.45 fc rgb "#e6edf5" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 5293 "189" at 1,13 center font "Helvetica, 7" tc rgb "#333333" front
set object 55 rect from 1.52,12.55 to 2.48,13.45 fc rgb "#fafcfd" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 5294 "206" at 2,13 center font "Helvetica, 7" tc rgb "#333333" front
set object 56 rect from 2.52,12.55 to 3.48,13.45 fc rgb "#e3ebf4" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 5295 "186" at 3,13 center font "Helvetica, 7" tc rgb "#333333" front
set object 57 rect from -0.48,13.55 to 0.48,14.45 fc rgb "#e8eff6" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 5296 "191" at 0,14 center font "Helvetica, 7" tc rgb "#333333" front
set object 58 rect from 0.52,13.55 to 1.48,14.45 fc rgb "#e9eff6" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 5297 "191" at 1,14 center font "Helvetica, 7" tc rgb "#333333" front
set object 59 rect from 1.52,13.55 to 2.48,14.45 fc rgb "#f6f9fb" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 5298 "203" at 2,14 center font "Helvetica, 7" tc rgb "#333333" front
set object 60 rect from 2.52,13.55 to 3.48,14.45 fc rgb "#f0f4f9" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 5299 "197" at 3,14 center font "Helvetica, 7" tc rgb "#333333" front
plot NaN notitle

unset arrow
unset object
unset label
# --- Panel 6: oxylabs_mobile ---
set xrange [-0.5:3.5]
set yrange [-0.5:14.5]
set xtics ("VA" 0, "TK" 1, "PA" 2, "SP" 3) font "Helvetica, 9"
set ytics ("" 0, "" 1, "" 2, "" 3, "" 4, "" 5, "" 6, "" 7, "" 8, "" 9, "" 10, "" 11, "" 12, "" 13, "" 14) font "Helvetica, 9"
set title "{/Helvetica-Bold Oxylabs (Mobile)}" font "Helvetica-Bold, 10"
unset key
unset colorbox
unset grid
set arrow from -0.5,2.5 to 3.5,2.5 nohead lw 0.8 lc rgb "#aaaaaa" front
set arrow from -0.5,6.5 to 3.5,6.5 nohead lw 0.8 lc rgb "#aaaaaa" front
set arrow from -0.5,7.5 to 3.5,7.5 nohead lw 0.8 lc rgb "#aaaaaa" front
set arrow from -0.5,12.5 to 3.5,12.5 nohead lw 0.8 lc rgb "#aaaaaa" front
set arrow from -0.5,13.5 to 3.5,13.5 nohead lw 0.8 lc rgb "#aaaaaa" front
set object 1 rect from -0.48,-0.45 to 0.48,0.45 fc rgb "#f3f6fa" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 6300 "200" at 0,0 center font "Helvetica, 7" tc rgb "#333333" front
set object 2 rect from 0.52,-0.45 to 1.48,0.45 fc rgb "#e9f0f6" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 6301 "192" at 1,0 center font "Helvetica, 7" tc rgb "#333333" front
set object 3 rect from 1.52,-0.45 to 2.48,0.45 fc rgb "#f4f7fb" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 6302 "201" at 2,0 center font "Helvetica, 7" tc rgb "#333333" front
set object 4 rect from 2.52,-0.45 to 3.48,0.45 fc rgb "#f9fbfc" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 6303 "205" at 3,0 center font "Helvetica, 7" tc rgb "#333333" front
set object 5 rect from -0.48,0.55 to 0.48,1.45 fc rgb "#d7e3f0" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 6304 "176" at 0,1 center font "Helvetica, 7" tc rgb "#333333" front
set object 6 rect from 0.52,0.55 to 1.48,1.45 fc rgb "#ebf1f7" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 6305 "193" at 1,1 center font "Helvetica, 7" tc rgb "#333333" front
set object 7 rect from 1.52,0.55 to 2.48,1.45 fc rgb "#e6edf5" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 6306 "189" at 2,1 center font "Helvetica, 7" tc rgb "#333333" front
set object 8 rect from 2.52,0.55 to 3.48,1.45 fc rgb "#e0eaf3" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 6307 "184" at 3,1 center font "Helvetica, 7" tc rgb "#333333" front
set object 9 rect from -0.48,1.55 to 0.48,2.45 fc rgb "#f1f5f9" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 6308 "198" at 0,2 center font "Helvetica, 7" tc rgb "#333333" front
set object 10 rect from 0.52,1.55 to 1.48,2.45 fc rgb "#eaf0f7" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 6309 "193" at 1,2 center font "Helvetica, 7" tc rgb "#333333" front
set object 11 rect from 1.52,1.55 to 2.48,2.45 fc rgb "#f1f5f9" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 6310 "198" at 2,2 center font "Helvetica, 7" tc rgb "#333333" front
set object 12 rect from 2.52,1.55 to 3.48,2.45 fc rgb "#e9f0f7" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 6311 "192" at 3,2 center font "Helvetica, 7" tc rgb "#333333" front
set object 13 rect from -0.48,2.55 to 0.48,3.45 fc rgb "#e2ebf4" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 6312 "186" at 0,3 center font "Helvetica, 7" tc rgb "#333333" front
set object 14 rect from 0.52,2.55 to 1.48,3.45 fc rgb "#f0f5f9" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 6313 "198" at 1,3 center font "Helvetica, 7" tc rgb "#333333" front
set object 15 rect from 1.52,2.55 to 2.48,3.45 fc rgb "#e2ebf4" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 6314 "185" at 2,3 center font "Helvetica, 7" tc rgb "#333333" front
set object 16 rect from 2.52,2.55 to 3.48,3.45 fc rgb "#eef3f8" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 6315 "196" at 3,3 center font "Helvetica, 7" tc rgb "#333333" front
set object 17 rect from -0.48,3.55 to 0.48,4.45 fc rgb "#edf2f8" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 6316 "195" at 0,4 center font "Helvetica, 7" tc rgb "#333333" front
set object 18 rect from 0.52,3.55 to 1.48,4.45 fc rgb "#eff4f9" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 6317 "197" at 1,4 center font "Helvetica, 7" tc rgb "#333333" front
set object 19 rect from 1.52,3.55 to 2.48,4.45 fc rgb "#f5f8fb" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 6318 "202" at 2,4 center font "Helvetica, 7" tc rgb "#333333" front
set object 20 rect from 2.52,3.55 to 3.48,4.45 fc rgb "#ecf2f8" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 6319 "194" at 3,4 center font "Helvetica, 7" tc rgb "#333333" front
set object 21 rect from -0.48,4.55 to 0.48,5.45 fc rgb "#e5edf5" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 6320 "189" at 0,5 center font "Helvetica, 7" tc rgb "#333333" front
set object 22 rect from 0.52,4.55 to 1.48,5.45 fc rgb "#dae5f1" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 6321 "179" at 1,5 center font "Helvetica, 7" tc rgb "#333333" front
set object 23 rect from 1.52,4.55 to 2.48,5.45 fc rgb "#ecf2f8" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 6322 "194" at 2,5 center font "Helvetica, 7" tc rgb "#333333" front
set object 24 rect from 2.52,4.55 to 3.48,5.45 fc rgb "#e8eff6" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 6323 "191" at 3,5 center font "Helvetica, 7" tc rgb "#333333" front
set object 25 rect from -0.48,5.55 to 0.48,6.45 fc rgb "#c7d8ea" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 6324 "162" at 0,6 center font "Helvetica, 7" tc rgb "#333333" front
set object 26 rect from 0.52,5.55 to 1.48,6.45 fc rgb "#e6eef6" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 6325 "189" at 1,6 center font "Helvetica, 7" tc rgb "#333333" front
set object 27 rect from 1.52,5.55 to 2.48,6.45 fc rgb "#edf3f8" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 6326 "195" at 2,6 center font "Helvetica, 7" tc rgb "#333333" front
set object 28 rect from 2.52,5.55 to 3.48,6.45 fc rgb "#fefefe" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 6327 "210" at 3,6 center font "Helvetica, 7" tc rgb "#333333" front
set object 29 rect from -0.48,6.55 to 0.48,7.45 fc rgb "#f7f9fc" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 6328 "203" at 0,7 center font "Helvetica, 7" tc rgb "#333333" front
set object 30 rect from 0.52,6.55 to 1.48,7.45 fc rgb "#f7f9fc" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 6329 "204" at 1,7 center font "Helvetica, 7" tc rgb "#333333" front
set object 31 rect from 1.52,6.55 to 2.48,7.45 fc rgb "#f1f5f9" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 6330 "198" at 2,7 center font "Helvetica, 7" tc rgb "#333333" front
set object 32 rect from 2.52,6.55 to 3.48,7.45 fc rgb "#e0eaf3" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 6331 "184" at 3,7 center font "Helvetica, 7" tc rgb "#333333" front
set object 33 rect from -0.48,7.55 to 0.48,8.45 fc rgb "#ecf1f7" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 6332 "194" at 0,8 center font "Helvetica, 7" tc rgb "#333333" front
set object 34 rect from 0.52,7.55 to 1.48,8.45 fc rgb "#ebf1f7" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 6333 "194" at 1,8 center font "Helvetica, 7" tc rgb "#333333" front
set object 35 rect from 1.52,7.55 to 2.48,8.45 fc rgb "#f6f8fb" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 6334 "202" at 2,8 center font "Helvetica, 7" tc rgb "#333333" front
set object 36 rect from 2.52,7.55 to 3.48,8.45 fc rgb "#e3ebf4" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 6335 "186" at 3,8 center font "Helvetica, 7" tc rgb "#333333" front
set object 37 rect from -0.48,8.55 to 0.48,9.45 fc rgb "#f0f4f9" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 6336 "197" at 0,9 center font "Helvetica, 7" tc rgb "#333333" front
set object 38 rect from 0.52,8.55 to 1.48,9.45 fc rgb "#ebf1f7" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 6337 "193" at 1,9 center font "Helvetica, 7" tc rgb "#333333" front
set object 39 rect from 1.52,8.55 to 2.48,9.45 fc rgb "#f6f8fb" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 6338 "203" at 2,9 center font "Helvetica, 7" tc rgb "#333333" front
set object 40 rect from 2.52,8.55 to 3.48,9.45 fc rgb "#e2ebf4" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 6339 "185" at 3,9 center font "Helvetica, 7" tc rgb "#333333" front
set object 41 rect from -0.48,9.55 to 0.48,10.45 fc rgb "#f1f5f9" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 6340 "198" at 0,10 center font "Helvetica, 7" tc rgb "#333333" front
set object 42 rect from 0.52,9.55 to 1.48,10.45 fc rgb "#f1f5fa" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 6341 "199" at 1,10 center font "Helvetica, 7" tc rgb "#333333" front
set object 43 rect from 1.52,9.55 to 2.48,10.45 fc rgb "#edf2f8" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 6342 "195" at 2,10 center font "Helvetica, 7" tc rgb "#333333" front
set object 44 rect from 2.52,9.55 to 3.48,10.45 fc rgb "#d1dfed" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 6343 "171" at 3,10 center font "Helvetica, 7" tc rgb "#333333" front
set object 45 rect from -0.48,10.55 to 0.48,11.45 fc rgb "#e1eaf4" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 6344 "185" at 0,11 center font "Helvetica, 7" tc rgb "#333333" front
set object 46 rect from 0.52,10.55 to 1.48,11.45 fc rgb "#e4ecf4" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 6345 "187" at 1,11 center font "Helvetica, 7" tc rgb "#333333" front
set object 47 rect from 1.52,10.55 to 2.48,11.45 fc rgb "#fefefe" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 6346 "209" at 2,11 center font "Helvetica, 7" tc rgb "#333333" front
set object 48 rect from 2.52,10.55 to 3.48,11.45 fc rgb "#f3f7fa" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 6347 "200" at 3,11 center font "Helvetica, 7" tc rgb "#333333" front
set object 49 rect from -0.48,11.55 to 0.48,12.45 fc rgb "#eaf0f7" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 6348 "192" at 0,12 center font "Helvetica, 7" tc rgb "#333333" front
set object 50 rect from 0.52,11.55 to 1.48,12.45 fc rgb "#e8eff6" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 6349 "191" at 1,12 center font "Helvetica, 7" tc rgb "#333333" front
set object 51 rect from 1.52,11.55 to 2.48,12.45 fc rgb "#f3f7fa" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 6350 "200" at 2,12 center font "Helvetica, 7" tc rgb "#333333" front
set object 52 rect from 2.52,11.55 to 3.48,12.45 fc rgb "#e7eff6" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 6351 "190" at 3,12 center font "Helvetica, 7" tc rgb "#333333" front
set object 53 rect from -0.48,12.55 to 0.48,13.45 fc rgb "#edf3f8" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 6352 "195" at 0,13 center font "Helvetica, 7" tc rgb "#333333" front
set object 54 rect from 0.52,12.55 to 1.48,13.45 fc rgb "#ecf2f8" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 6353 "194" at 1,13 center font "Helvetica, 7" tc rgb "#333333" front
set object 55 rect from 1.52,12.55 to 2.48,13.45 fc rgb "#e7eef6" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 6354 "190" at 2,13 center font "Helvetica, 7" tc rgb "#333333" front
set object 56 rect from 2.52,12.55 to 3.48,13.45 fc rgb "#e5edf5" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 6355 "188" at 3,13 center font "Helvetica, 7" tc rgb "#333333" front
set object 57 rect from -0.48,13.55 to 0.48,14.45 fc rgb "#e3ecf4" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 6356 "187" at 0,14 center font "Helvetica, 7" tc rgb "#333333" front
set object 58 rect from 0.52,13.55 to 1.48,14.45 fc rgb "#e4ecf4" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 6357 "187" at 1,14 center font "Helvetica, 7" tc rgb "#333333" front
set object 59 rect from 1.52,13.55 to 2.48,14.45 fc rgb "#f9fbfc" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 6358 "205" at 2,14 center font "Helvetica, 7" tc rgb "#333333" front
set object 60 rect from 2.52,13.55 to 3.48,14.45 fc rgb "#e4ecf4" fs solid 1.0 border lc rgb "#dddddd" lw 0.2 behind
set label 6359 "187" at 3,14 center font "Helvetica, 7" tc rgb "#333333" front
plot NaN notitle

unset arrow
unset object
unset label
unset multiplot
