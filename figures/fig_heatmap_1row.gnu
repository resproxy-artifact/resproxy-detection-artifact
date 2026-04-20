load 'style.gnu'
set terminal postscript enhanced color eps font "Helvetica, 10"
set size 0.95, 0.90
set output '../figures/heatmap_1row.eps'

set multiplot

set xrange [-0.5:3.5]
set yrange [-0.3:7.4]
set xtics ("VA" 0, "TK" 1, "PA" 2, "SP" 3) font "Helvetica, 7" offset 0,0.3
set format y ""
set format x ""
set border 0
set tics scale 0

# --- Panel 1: BrightData ---
set ytics ("United States" 0.23, "Canada" 0.69, "Mexico" 1.15, "United Kingdom" 1.61, "Germany" 2.06, "France" 2.53, "Russia" 2.99, "Brazil" 3.45, "Japan" 3.91, "Singapore" 4.37, "Indonesia" 4.83, "South Korea" 5.29, "India" 5.75, "Australia" 6.21, "South Africa" 6.67) font "Helvetica, 6"
set label 999 "{/Helvetica-Bold BrightData (Super-proxy)}" at 1.5,7.1 center font "Helvetica-Bold, 7"
unset key; unset colorbox; unset grid; unset xlabel
set arrow 102 from -0.5,1.38 to 3.5,1.38 nohead lw 0.5 lc rgb "#bbbbbb" front
set arrow 106 from -0.5,3.22 to 3.5,3.22 nohead lw 0.5 lc rgb "#bbbbbb" front
set arrow 107 from -0.5,3.68 to 3.5,3.68 nohead lw 0.5 lc rgb "#bbbbbb" front
set arrow 113 from -0.5,6.44 to 3.5,6.44 nohead lw 0.5 lc rgb "#bbbbbb" front
set object 1 rect from -0.48,0.00 to 0.48,0.45 fc rgb "#7ca5ce" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 1000 "103" at 0,0.23 center font "Helvetica, 6" tc rgb "#333333" front
set object 2 rect from 0.52,0.00 to 1.48,0.45 fc rgb "#7ca4ce" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 1001 "103" at 1,0.23 center font "Helvetica, 6" tc rgb "#333333" front
set object 3 rect from 1.52,0.00 to 2.48,0.45 fc rgb "#92b4d6" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 1002 "128" at 2,0.23 center font "Helvetica, 6" tc rgb "#333333" front
set object 4 rect from 2.52,0.00 to 3.48,0.45 fc rgb "#a4c0dc" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 1003 "148" at 3,0.23 center font "Helvetica, 6" tc rgb "#333333" front
set object 5 rect from -0.48,0.46 to 0.48,0.91 fc rgb "#6e9bc8" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 1004 "87" at 0,0.69 center font "Helvetica, 6" tc rgb "#333333" front
set object 6 rect from 0.52,0.46 to 1.48,0.91 fc rgb "#6796c6" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 1005 "80" at 1,0.69 center font "Helvetica, 6" tc rgb "#333333" front
set object 7 rect from 1.52,0.46 to 2.48,0.91 fc rgb "#5f90c3" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 1006 "70" at 2,0.69 center font "Helvetica, 6" tc rgb "#333333" front
set object 8 rect from 2.52,0.46 to 3.48,0.91 fc rgb "#6c99c8" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 1007 "85" at 3,0.69 center font "Helvetica, 6" tc rgb "#333333" front
set object 9 rect from -0.48,0.92 to 0.48,1.37 fc rgb "#a3c0dc" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 1008 "147" at 0,1.15 center font "Helvetica, 6" tc rgb "#333333" front
set object 10 rect from 0.52,0.92 to 1.48,1.37 fc rgb "#a1bedb" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 1009 "144" at 1,1.15 center font "Helvetica, 6" tc rgb "#333333" front
set object 11 rect from 1.52,0.92 to 2.48,1.37 fc rgb "#9cbbda" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 1010 "139" at 2,1.15 center font "Helvetica, 6" tc rgb "#333333" front
set object 12 rect from 2.52,0.92 to 3.48,1.37 fc rgb "#97b7d8" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 1011 "133" at 3,1.15 center font "Helvetica, 6" tc rgb "#333333" front
set object 13 rect from -0.48,1.38 to 0.48,1.83 fc rgb "#88add2" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 1012 "117" at 0,1.61 center font "Helvetica, 6" tc rgb "#333333" front
set object 14 rect from 0.52,1.38 to 1.48,1.83 fc rgb "#85abd1" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 1013 "113" at 1,1.61 center font "Helvetica, 6" tc rgb "#333333" front
set object 15 rect from 1.52,1.38 to 2.48,1.83 fc rgb "#85abd1" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 1014 "114" at 2,1.61 center font "Helvetica, 6" tc rgb "#333333" front
set object 16 rect from 2.52,1.38 to 3.48,1.83 fc rgb "#80a7cf" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 1015 "108" at 3,1.61 center font "Helvetica, 6" tc rgb "#333333" front
set object 17 rect from -0.48,1.84 to 0.48,2.29 fc rgb "#90b2d5" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 1016 "125" at 0,2.06 center font "Helvetica, 6" tc rgb "#333333" front
set object 18 rect from 0.52,1.84 to 1.48,2.29 fc rgb "#94b5d7" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 1017 "130" at 1,2.06 center font "Helvetica, 6" tc rgb "#333333" front
set object 19 rect from 1.52,1.84 to 2.48,2.29 fc rgb "#93b5d6" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 1018 "129" at 2,2.06 center font "Helvetica, 6" tc rgb "#333333" front
set object 20 rect from 2.52,1.84 to 3.48,2.29 fc rgb "#96b6d7" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 1019 "132" at 3,2.06 center font "Helvetica, 6" tc rgb "#333333" front
set object 21 rect from -0.48,2.30 to 0.48,2.75 fc rgb "#85abd1" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 1020 "114" at 0,2.53 center font "Helvetica, 6" tc rgb "#333333" front
set object 22 rect from 0.52,2.30 to 1.48,2.75 fc rgb "#89add2" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 1021 "117" at 1,2.53 center font "Helvetica, 6" tc rgb "#333333" front
set object 23 rect from 1.52,2.30 to 2.48,2.75 fc rgb "#80a8cf" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 1022 "108" at 2,2.53 center font "Helvetica, 6" tc rgb "#333333" front
set object 24 rect from 2.52,2.30 to 3.48,2.75 fc rgb "#82a9d0" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 1023 "110" at 3,2.53 center font "Helvetica, 6" tc rgb "#333333" front
set object 25 rect from -0.48,2.76 to 0.48,3.21 fc rgb "#cccccc" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 1024 "-" at 0,2.99 center font "Helvetica, 6" tc rgb "#333333" front
set object 26 rect from 0.52,2.76 to 1.48,3.21 fc rgb "#cccccc" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 1025 "-" at 1,2.99 center font "Helvetica, 6" tc rgb "#333333" front
set object 27 rect from 1.52,2.76 to 2.48,3.21 fc rgb "#cccccc" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 1026 "-" at 2,2.99 center font "Helvetica, 6" tc rgb "#333333" front
set object 28 rect from 2.52,2.76 to 3.48,3.21 fc rgb "#cccccc" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 1027 "-" at 3,2.99 center font "Helvetica, 6" tc rgb "#333333" front
set object 29 rect from -0.48,3.22 to 0.48,3.67 fc rgb "#d1dfee" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 1028 "199" at 0,3.45 center font "Helvetica, 6" tc rgb "#333333" front
set object 30 rect from 0.52,3.22 to 1.48,3.67 fc rgb "#cfdded" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 1029 "196" at 1,3.45 center font "Helvetica, 6" tc rgb "#333333" front
set object 31 rect from 1.52,3.22 to 2.48,3.67 fc rgb "#c7d9ea" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 1030 "188" at 2,3.45 center font "Helvetica, 6" tc rgb "#333333" front
set object 32 rect from 2.52,3.22 to 3.48,3.67 fc rgb "#eaf0f7" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 1031 "227" at 3,3.45 center font "Helvetica, 6" tc rgb "#333333" front
set object 33 rect from -0.48,3.68 to 0.48,4.13 fc rgb "#cfdeed" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 1032 "197" at 0,3.91 center font "Helvetica, 6" tc rgb "#333333" front
set object 34 rect from 0.52,3.68 to 1.48,4.13 fc rgb "#d0deed" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 1033 "198" at 1,3.91 center font "Helvetica, 6" tc rgb "#333333" front
set object 35 rect from 1.52,3.68 to 2.48,4.13 fc rgb "#d3e0ee" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 1034 "200" at 2,3.91 center font "Helvetica, 6" tc rgb "#333333" front
set object 36 rect from 2.52,3.68 to 3.48,4.13 fc rgb "#d5e2ef" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 1035 "203" at 3,3.91 center font "Helvetica, 6" tc rgb "#333333" front
set object 37 rect from -0.48,4.14 to 0.48,4.59 fc rgb "#f2f6fa" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 1036 "236" at 0,4.37 center font "Helvetica, 6" tc rgb "#333333" front
set object 38 rect from 0.52,4.14 to 1.48,4.59 fc rgb "#f0d3d7" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 1037 "297" at 1,4.37 center font "Helvetica, 6" tc rgb "#333333" front
set object 39 rect from 1.52,4.14 to 2.48,4.59 fc rgb "#fcf8f9" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 1038 "257" at 2,4.37 center font "Helvetica, 6" tc rgb "#333333" front
set object 40 rect from 2.52,4.14 to 3.48,4.59 fc rgb "#fdf9fa" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 1039 "256" at 3,4.37 center font "Helvetica, 6" tc rgb "#333333" front
set object 41 rect from -0.48,4.60 to 0.48,5.05 fc rgb "#f1d5d9" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 1040 "295" at 0,4.83 center font "Helvetica, 6" tc rgb "#333333" front
set object 42 rect from 0.52,4.60 to 1.48,5.05 fc rgb "#eeccd0" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 1041 "304" at 1,4.83 center font "Helvetica, 6" tc rgb "#333333" front
set object 43 rect from 1.52,4.60 to 2.48,5.05 fc rgb "#f2d9dc" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 1042 "291" at 2,4.83 center font "Helvetica, 6" tc rgb "#333333" front
set object 44 rect from 2.52,4.60 to 3.48,5.05 fc rgb "#f3dbde" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 1043 "288" at 3,4.83 center font "Helvetica, 6" tc rgb "#333333" front
set object 45 rect from -0.48,5.06 to 0.48,5.51 fc rgb "#faf0f1" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 1044 "266" at 0,5.29 center font "Helvetica, 6" tc rgb "#333333" front
set object 46 rect from 0.52,5.06 to 1.48,5.51 fc rgb "#f6e5e7" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 1045 "277" at 1,5.29 center font "Helvetica, 6" tc rgb "#333333" front
set object 47 rect from 1.52,5.06 to 2.48,5.51 fc rgb "#f8ebec" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 1046 "271" at 2,5.29 center font "Helvetica, 6" tc rgb "#333333" front
set object 48 rect from 2.52,5.06 to 3.48,5.51 fc rgb "#f7e8ea" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 1047 "274" at 3,5.29 center font "Helvetica, 6" tc rgb "#333333" front
set object 49 rect from -0.48,5.52 to 0.48,5.97 fc rgb "#e8babf" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 1048 "325" at 0,5.75 center font "Helvetica, 6" tc rgb "#333333" front
set object 50 rect from 0.52,5.52 to 1.48,5.97 fc rgb "#efcfd3" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 1049 "302" at 1,5.75 center font "Helvetica, 6" tc rgb "#333333" front
set object 51 rect from 1.52,5.52 to 2.48,5.97 fc rgb "#edcace" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 1050 "307" at 2,5.75 center font "Helvetica, 6" tc rgb "#333333" front
set object 52 rect from 2.52,5.52 to 3.48,5.97 fc rgb "#ecc7cb" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 1051 "310" at 3,5.75 center font "Helvetica, 6" tc rgb "#333333" front
set object 53 rect from -0.48,5.98 to 0.48,6.43 fc rgb "#f4dee0" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 1052 "286" at 0,6.21 center font "Helvetica, 6" tc rgb "#333333" front
set object 54 rect from 0.52,5.98 to 1.48,6.43 fc rgb "#ecc6cb" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 1053 "311" at 1,6.21 center font "Helvetica, 6" tc rgb "#333333" front
set object 55 rect from 1.52,5.98 to 2.48,6.43 fc rgb "#f6e5e7" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 1054 "278" at 2,6.21 center font "Helvetica, 6" tc rgb "#333333" front
set object 56 rect from 2.52,5.98 to 3.48,6.43 fc rgb "#f4e0e2" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 1055 "283" at 3,6.21 center font "Helvetica, 6" tc rgb "#333333" front
set object 57 rect from -0.48,6.44 to 0.48,6.89 fc rgb "#e9bdc3" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 1056 "321" at 0,6.67 center font "Helvetica, 6" tc rgb "#333333" front
set object 58 rect from 0.52,6.44 to 1.48,6.89 fc rgb "#efcfd3" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 1057 "301" at 1,6.67 center font "Helvetica, 6" tc rgb "#333333" front
set object 59 rect from 1.52,6.44 to 2.48,6.89 fc rgb "#ecc8cd" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 1058 "309" at 2,6.67 center font "Helvetica, 6" tc rgb "#333333" front
set object 60 rect from 2.52,6.44 to 3.48,6.89 fc rgb "#ebc3c8" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 1059 "315" at 3,6.67 center font "Helvetica, 6" tc rgb "#333333" front
set lmargin at screen 0.070
set rmargin at screen 0.189
set bmargin at screen 0.08
set tmargin at screen 0.88
plot NaN notitle

# --- Panel 2: SOAX ---
unset label 999
unset object 1
unset label 1000
unset object 2
unset label 1001
unset object 3
unset label 1002
unset object 4
unset label 1003
unset object 5
unset label 1004
unset object 6
unset label 1005
unset object 7
unset label 1006
unset object 8
unset label 1007
unset object 9
unset label 1008
unset object 10
unset label 1009
unset object 11
unset label 1010
unset object 12
unset label 1011
unset object 13
unset label 1012
unset object 14
unset label 1013
unset object 15
unset label 1014
unset object 16
unset label 1015
unset object 17
unset label 1016
unset object 18
unset label 1017
unset object 19
unset label 1018
unset object 20
unset label 1019
unset object 21
unset label 1020
unset object 22
unset label 1021
unset object 23
unset label 1022
unset object 24
unset label 1023
unset object 25
unset label 1024
unset object 26
unset label 1025
unset object 27
unset label 1026
unset object 28
unset label 1027
unset object 29
unset label 1028
unset object 30
unset label 1029
unset object 31
unset label 1030
unset object 32
unset label 1031
unset object 33
unset label 1032
unset object 34
unset label 1033
unset object 35
unset label 1034
unset object 36
unset label 1035
unset object 37
unset label 1036
unset object 38
unset label 1037
unset object 39
unset label 1038
unset object 40
unset label 1039
unset object 41
unset label 1040
unset object 42
unset label 1041
unset object 43
unset label 1042
unset object 44
unset label 1043
unset object 45
unset label 1044
unset object 46
unset label 1045
unset object 47
unset label 1046
unset object 48
unset label 1047
unset object 49
unset label 1048
unset object 50
unset label 1049
unset object 51
unset label 1050
unset object 52
unset label 1051
unset object 53
unset label 1052
unset object 54
unset label 1053
unset object 55
unset label 1054
unset object 56
unset label 1055
unset object 57
unset label 1056
unset object 58
unset label 1057
unset object 59
unset label 1058
unset object 60
unset label 1059
unset ytics
set label 999 "{/Helvetica-Bold SOAX (Super-proxy)}" at 1.5,7.1 center font "Helvetica-Bold, 7"
unset key; unset colorbox; unset grid; unset xlabel
set arrow 102 from -0.5,1.38 to 3.5,1.38 nohead lw 0.5 lc rgb "#bbbbbb" front
set arrow 106 from -0.5,3.22 to 3.5,3.22 nohead lw 0.5 lc rgb "#bbbbbb" front
set arrow 107 from -0.5,3.68 to 3.5,3.68 nohead lw 0.5 lc rgb "#bbbbbb" front
set arrow 113 from -0.5,6.44 to 3.5,6.44 nohead lw 0.5 lc rgb "#bbbbbb" front
set object 1001 rect from -0.48,0.00 to 0.48,0.45 fc rgb "#9ab9d9" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 11000 "137" at 0,0.23 center font "Helvetica, 6" tc rgb "#333333" front
set object 1002 rect from 0.52,0.00 to 1.48,0.45 fc rgb "#9ab9d9" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 11001 "137" at 1,0.23 center font "Helvetica, 6" tc rgb "#333333" front
set object 1003 rect from 1.52,0.00 to 2.48,0.45 fc rgb "#95b6d7" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 11002 "131" at 2,0.23 center font "Helvetica, 6" tc rgb "#333333" front
set object 1004 rect from 2.52,0.00 to 3.48,0.45 fc rgb "#8db0d4" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 11003 "122" at 3,0.23 center font "Helvetica, 6" tc rgb "#333333" front
set object 1005 rect from -0.48,0.46 to 0.48,0.91 fc rgb "#9cbad9" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 11004 "139" at 0,0.69 center font "Helvetica, 6" tc rgb "#333333" front
set object 1006 rect from 0.52,0.46 to 1.48,0.91 fc rgb "#9bbad9" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 11005 "137" at 1,0.69 center font "Helvetica, 6" tc rgb "#333333" front
set object 1007 rect from 1.52,0.46 to 2.48,0.91 fc rgb "#9cbbda" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 11006 "140" at 2,0.69 center font "Helvetica, 6" tc rgb "#333333" front
set object 1008 rect from 2.52,0.46 to 3.48,0.91 fc rgb "#9bbad9" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 11007 "138" at 3,0.69 center font "Helvetica, 6" tc rgb "#333333" front
set object 1009 rect from -0.48,0.92 to 0.48,1.37 fc rgb "#9bbad9" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 11008 "138" at 0,1.15 center font "Helvetica, 6" tc rgb "#333333" front
set object 1010 rect from 0.52,0.92 to 1.48,1.37 fc rgb "#9abad9" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 11009 "137" at 1,1.15 center font "Helvetica, 6" tc rgb "#333333" front
set object 1011 rect from 1.52,0.92 to 2.48,1.37 fc rgb "#9bbad9" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 11010 "137" at 2,1.15 center font "Helvetica, 6" tc rgb "#333333" front
set object 1012 rect from 2.52,0.92 to 3.48,1.37 fc rgb "#9dbbda" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 11011 "140" at 3,1.15 center font "Helvetica, 6" tc rgb "#333333" front
set object 1013 rect from -0.48,1.38 to 0.48,1.83 fc rgb "#9ebcda" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 11012 "141" at 0,1.61 center font "Helvetica, 6" tc rgb "#333333" front
set object 1014 rect from 0.52,1.38 to 1.48,1.83 fc rgb "#9dbbda" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 11013 "140" at 1,1.61 center font "Helvetica, 6" tc rgb "#333333" front
set object 1015 rect from 1.52,1.38 to 2.48,1.83 fc rgb "#9fbddb" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 11014 "143" at 2,1.61 center font "Helvetica, 6" tc rgb "#333333" front
set object 1016 rect from 2.52,1.38 to 3.48,1.83 fc rgb "#9dbbda" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 11015 "140" at 3,1.61 center font "Helvetica, 6" tc rgb "#333333" front
set object 1017 rect from -0.48,1.84 to 0.48,2.29 fc rgb "#e5b1b7" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 11016 "334" at 0,2.06 center font "Helvetica, 6" tc rgb "#333333" front
set object 1018 rect from 0.52,1.84 to 1.48,2.29 fc rgb "#8bafd3" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 11017 "120" at 1,2.06 center font "Helvetica, 6" tc rgb "#333333" front
set object 1019 rect from 1.52,1.84 to 2.48,2.29 fc rgb "#e4b0b7" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 11018 "335" at 2,2.06 center font "Helvetica, 6" tc rgb "#333333" front
set object 1020 rect from 2.52,1.84 to 3.48,2.29 fc rgb "#e4aeb5" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 11019 "337" at 3,2.06 center font "Helvetica, 6" tc rgb "#333333" front
set object 1021 rect from -0.48,2.30 to 0.48,2.75 fc rgb "#e9bec3" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 11020 "320" at 0,2.53 center font "Helvetica, 6" tc rgb "#333333" front
set object 1022 rect from 0.52,2.30 to 1.48,2.75 fc rgb "#e9bec3" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 11021 "320" at 1,2.53 center font "Helvetica, 6" tc rgb "#333333" front
set object 1023 rect from 1.52,2.30 to 2.48,2.75 fc rgb "#ecc7cc" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 11022 "310" at 2,2.53 center font "Helvetica, 6" tc rgb "#333333" front
set object 1024 rect from 2.52,2.30 to 3.48,2.75 fc rgb "#e7b9bf" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 11023 "325" at 3,2.53 center font "Helvetica, 6" tc rgb "#333333" front
set object 1025 rect from -0.48,2.76 to 0.48,3.21 fc rgb "#ecc7cb" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 11024 "311" at 0,2.99 center font "Helvetica, 6" tc rgb "#333333" front
set object 1026 rect from 0.52,2.76 to 1.48,3.21 fc rgb "#9bbad9" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 11025 "138" at 1,2.99 center font "Helvetica, 6" tc rgb "#333333" front
set object 1027 rect from 1.52,2.76 to 2.48,3.21 fc rgb "#f0d4d7" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 11026 "296" at 2,2.99 center font "Helvetica, 6" tc rgb "#333333" front
set object 1028 rect from 2.52,2.76 to 3.48,3.21 fc rgb "#eac2c7" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 11027 "316" at 3,2.99 center font "Helvetica, 6" tc rgb "#333333" front
set object 1029 rect from -0.48,3.22 to 0.48,3.67 fc rgb "#a7c2de" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 11028 "151" at 0,3.45 center font "Helvetica, 6" tc rgb "#333333" front
set object 1030 rect from 0.52,3.22 to 1.48,3.67 fc rgb "#9dbbda" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 11029 "140" at 1,3.45 center font "Helvetica, 6" tc rgb "#333333" front
set object 1031 rect from 1.52,3.22 to 2.48,3.67 fc rgb "#a2bfdc" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 11030 "146" at 2,3.45 center font "Helvetica, 6" tc rgb "#333333" front
set object 1032 rect from 2.52,3.22 to 3.48,3.67 fc rgb "#9ebcda" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 11031 "142" at 3,3.45 center font "Helvetica, 6" tc rgb "#333333" front
set object 1033 rect from -0.48,3.68 to 0.48,4.13 fc rgb "#e3adb4" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 11032 "338" at 0,3.91 center font "Helvetica, 6" tc rgb "#333333" front
set object 1034 rect from 0.52,3.68 to 1.48,4.13 fc rgb "#e4ecf5" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 11033 "220" at 1,3.91 center font "Helvetica, 6" tc rgb "#333333" front
set object 1035 rect from 1.52,3.68 to 2.48,4.13 fc rgb "#dee8f2" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 11034 "214" at 2,3.91 center font "Helvetica, 6" tc rgb "#333333" front
set object 1036 rect from 2.52,3.68 to 3.48,4.13 fc rgb "#e4b0b7" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 11035 "335" at 3,3.91 center font "Helvetica, 6" tc rgb "#333333" front
set object 1037 rect from -0.48,4.14 to 0.48,4.59 fc rgb "#a8c3de" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 11036 "152" at 0,4.37 center font "Helvetica, 6" tc rgb "#333333" front
set object 1038 rect from 0.52,4.14 to 1.48,4.59 fc rgb "#eac0c5" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 11037 "318" at 1,4.37 center font "Helvetica, 6" tc rgb "#333333" front
set object 1039 rect from 1.52,4.14 to 2.48,4.59 fc rgb "#f2dadd" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 11038 "290" at 2,4.37 center font "Helvetica, 6" tc rgb "#333333" front
set object 1040 rect from 2.52,4.14 to 3.48,4.59 fc rgb "#bfd3e7" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 11039 "178" at 3,4.37 center font "Helvetica, 6" tc rgb "#333333" front
set object 1041 rect from -0.48,4.60 to 0.48,5.05 fc rgb "#9abad9" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 11040 "137" at 0,4.83 center font "Helvetica, 6" tc rgb "#333333" front
set object 1042 rect from 0.52,4.60 to 1.48,5.05 fc rgb "#9cbada" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 11041 "139" at 1,4.83 center font "Helvetica, 6" tc rgb "#333333" front
set object 1043 rect from 1.52,4.60 to 2.48,5.05 fc rgb "#9bbad9" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 11042 "138" at 2,4.83 center font "Helvetica, 6" tc rgb "#333333" front
set object 1044 rect from 2.52,4.60 to 3.48,5.05 fc rgb "#9cbada" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 11043 "139" at 3,4.83 center font "Helvetica, 6" tc rgb "#333333" front
set object 1045 rect from -0.48,5.06 to 0.48,5.51 fc rgb "#91b3d5" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 11044 "126" at 0,5.29 center font "Helvetica, 6" tc rgb "#333333" front
set object 1046 rect from 0.52,5.06 to 1.48,5.51 fc rgb "#eac0c5" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 11045 "317" at 1,5.29 center font "Helvetica, 6" tc rgb "#333333" front
set object 1047 rect from 1.52,5.06 to 2.48,5.51 fc rgb "#b0c8e1" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 11046 "161" at 2,5.29 center font "Helvetica, 6" tc rgb "#333333" front
set object 1048 rect from 2.52,5.06 to 3.48,5.51 fc rgb "#e4b0b6" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 11047 "335" at 3,5.29 center font "Helvetica, 6" tc rgb "#333333" front
set object 1049 rect from -0.48,5.52 to 0.48,5.97 fc rgb "#9dbbda" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 11048 "140" at 0,5.75 center font "Helvetica, 6" tc rgb "#333333" front
set object 1050 rect from 0.52,5.52 to 1.48,5.97 fc rgb "#fefefe" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 11049 "251" at 1,5.75 center font "Helvetica, 6" tc rgb "#333333" front
set object 1051 rect from 1.52,5.52 to 2.48,5.97 fc rgb "#9cbbda" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 11050 "140" at 2,5.75 center font "Helvetica, 6" tc rgb "#333333" front
set object 1052 rect from 2.52,5.52 to 3.48,5.97 fc rgb "#a6c1dd" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 11051 "150" at 3,5.75 center font "Helvetica, 6" tc rgb "#333333" front
set object 1053 rect from -0.48,5.98 to 0.48,6.43 fc rgb "#a5c1dd" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 11052 "149" at 0,6.21 center font "Helvetica, 6" tc rgb "#333333" front
set object 1054 rect from 0.52,5.98 to 1.48,6.43 fc rgb "#9dbcda" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 11053 "141" at 1,6.21 center font "Helvetica, 6" tc rgb "#333333" front
set object 1055 rect from 1.52,5.98 to 2.48,6.43 fc rgb "#a6c2de" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 11054 "151" at 2,6.21 center font "Helvetica, 6" tc rgb "#333333" front
set object 1056 rect from 2.52,5.98 to 3.48,6.43 fc rgb "#96b7d8" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 11055 "133" at 3,6.21 center font "Helvetica, 6" tc rgb "#333333" front
set object 1057 rect from -0.48,6.44 to 0.48,6.89 fc rgb "#e3acb3" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 11056 "340" at 0,6.67 center font "Helvetica, 6" tc rgb "#333333" front
set object 1058 rect from 0.52,6.44 to 1.48,6.89 fc rgb "#ecc7cc" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 11057 "310" at 1,6.67 center font "Helvetica, 6" tc rgb "#333333" front
set object 1059 rect from 1.52,6.44 to 2.48,6.89 fc rgb "#e4aeb5" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 11058 "337" at 2,6.67 center font "Helvetica, 6" tc rgb "#333333" front
set object 1060 rect from 2.52,6.44 to 3.48,6.89 fc rgb "#d0737f" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 11059 "401" at 3,6.67 center font "Helvetica, 6" tc rgb "#333333" front
set lmargin at screen 0.195
set rmargin at screen 0.314
set bmargin at screen 0.08
set tmargin at screen 0.88
plot NaN notitle

# --- Panel 3: Oxylabs Res. ---
unset label 999
unset object 1001
unset label 11000
unset object 1002
unset label 11001
unset object 1003
unset label 11002
unset object 1004
unset label 11003
unset object 1005
unset label 11004
unset object 1006
unset label 11005
unset object 1007
unset label 11006
unset object 1008
unset label 11007
unset object 1009
unset label 11008
unset object 1010
unset label 11009
unset object 1011
unset label 11010
unset object 1012
unset label 11011
unset object 1013
unset label 11012
unset object 1014
unset label 11013
unset object 1015
unset label 11014
unset object 1016
unset label 11015
unset object 1017
unset label 11016
unset object 1018
unset label 11017
unset object 1019
unset label 11018
unset object 1020
unset label 11019
unset object 1021
unset label 11020
unset object 1022
unset label 11021
unset object 1023
unset label 11022
unset object 1024
unset label 11023
unset object 1025
unset label 11024
unset object 1026
unset label 11025
unset object 1027
unset label 11026
unset object 1028
unset label 11027
unset object 1029
unset label 11028
unset object 1030
unset label 11029
unset object 1031
unset label 11030
unset object 1032
unset label 11031
unset object 1033
unset label 11032
unset object 1034
unset label 11033
unset object 1035
unset label 11034
unset object 1036
unset label 11035
unset object 1037
unset label 11036
unset object 1038
unset label 11037
unset object 1039
unset label 11038
unset object 1040
unset label 11039
unset object 1041
unset label 11040
unset object 1042
unset label 11041
unset object 1043
unset label 11042
unset object 1044
unset label 11043
unset object 1045
unset label 11044
unset object 1046
unset label 11045
unset object 1047
unset label 11046
unset object 1048
unset label 11047
unset object 1049
unset label 11048
unset object 1050
unset label 11049
unset object 1051
unset label 11050
unset object 1052
unset label 11051
unset object 1053
unset label 11052
unset object 1054
unset label 11053
unset object 1055
unset label 11054
unset object 1056
unset label 11055
unset object 1057
unset label 11056
unset object 1058
unset label 11057
unset object 1059
unset label 11058
unset object 1060
unset label 11059
unset ytics
set label 999 "{/Helvetica-Bold Oxylabs Res. (Super-proxy)}" at 1.5,7.1 center font "Helvetica-Bold, 7"
unset key; unset colorbox; unset grid; unset xlabel
set arrow 102 from -0.5,1.38 to 3.5,1.38 nohead lw 0.5 lc rgb "#bbbbbb" front
set arrow 106 from -0.5,3.22 to 3.5,3.22 nohead lw 0.5 lc rgb "#bbbbbb" front
set arrow 107 from -0.5,3.68 to 3.5,3.68 nohead lw 0.5 lc rgb "#bbbbbb" front
set arrow 113 from -0.5,6.44 to 3.5,6.44 nohead lw 0.5 lc rgb "#bbbbbb" front
set object 2001 rect from -0.48,0.00 to 0.48,0.45 fc rgb "#80a8cf" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 21000 "108" at 0,0.23 center font "Helvetica, 6" tc rgb "#333333" front
set object 2002 rect from 0.52,0.00 to 1.48,0.45 fc rgb "#6997c6" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 21001 "81" at 1,0.23 center font "Helvetica, 6" tc rgb "#333333" front
set object 2003 rect from 1.52,0.00 to 2.48,0.45 fc rgb "#5e90c2" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 21002 "69" at 2,0.23 center font "Helvetica, 6" tc rgb "#333333" front
set object 2004 rect from 2.52,0.00 to 3.48,0.45 fc rgb "#598cc1" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 21003 "64" at 3,0.23 center font "Helvetica, 6" tc rgb "#333333" front
set object 2005 rect from -0.48,0.46 to 0.48,0.91 fc rgb "#5f90c3" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 21004 "70" at 0,0.69 center font "Helvetica, 6" tc rgb "#333333" front
set object 2006 rect from 0.52,0.46 to 1.48,0.91 fc rgb "#568bc0" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 21005 "61" at 1,0.69 center font "Helvetica, 6" tc rgb "#333333" front
set object 2007 rect from 1.52,0.46 to 2.48,0.91 fc rgb "#5489bf" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 21006 "58" at 2,0.69 center font "Helvetica, 6" tc rgb "#333333" front
set object 2008 rect from 2.52,0.46 to 3.48,0.91 fc rgb "#5f90c3" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 21007 "70" at 3,0.69 center font "Helvetica, 6" tc rgb "#333333" front
set object 2009 rect from -0.48,0.92 to 0.48,1.37 fc rgb "#86acd1" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 21008 "114" at 0,1.15 center font "Helvetica, 6" tc rgb "#333333" front
set object 2010 rect from 0.52,0.92 to 1.48,1.37 fc rgb "#8aafd3" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 21009 "119" at 1,1.15 center font "Helvetica, 6" tc rgb "#333333" front
set object 2011 rect from 1.52,0.92 to 2.48,1.37 fc rgb "#90b2d5" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 21010 "126" at 2,1.15 center font "Helvetica, 6" tc rgb "#333333" front
set object 2012 rect from 2.52,0.92 to 3.48,1.37 fc rgb "#93b4d6" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 21011 "129" at 3,1.15 center font "Helvetica, 6" tc rgb "#333333" front
set object 2013 rect from -0.48,1.38 to 0.48,1.83 fc rgb "#b3cbe2" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 21012 "165" at 0,1.61 center font "Helvetica, 6" tc rgb "#333333" front
set object 2014 rect from 0.52,1.38 to 1.48,1.83 fc rgb "#4d84bc" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 21013 "50" at 1,1.61 center font "Helvetica, 6" tc rgb "#333333" front
set object 2015 rect from 1.52,1.38 to 2.48,1.83 fc rgb "#d3e0ee" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 21014 "201" at 2,1.61 center font "Helvetica, 6" tc rgb "#333333" front
set object 2016 rect from 2.52,1.38 to 3.48,1.83 fc rgb "#3c78b6" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 21015 "31" at 3,1.61 center font "Helvetica, 6" tc rgb "#333333" front
set object 2017 rect from -0.48,1.84 to 0.48,2.29 fc rgb "#c24958" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 21016 "446" at 0,2.06 center font "Helvetica, 6" tc rgb "#333333" front
set object 2018 rect from 0.52,1.84 to 1.48,2.29 fc rgb "#b92d3e" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 21017 "477" at 1,2.06 center font "Helvetica, 6" tc rgb "#333333" front
set object 2019 rect from 1.52,1.84 to 2.48,2.29 fc rgb "#bc3647" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 21018 "467" at 2,2.06 center font "Helvetica, 6" tc rgb "#333333" front
set object 2020 rect from 2.52,1.84 to 3.48,2.29 fc rgb "#c34b5a" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 21019 "445" at 3,2.06 center font "Helvetica, 6" tc rgb "#333333" front
set object 2021 rect from -0.48,2.30 to 0.48,2.75 fc rgb "#bdd1e6" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 21020 "176" at 0,2.53 center font "Helvetica, 6" tc rgb "#333333" front
set object 2022 rect from 0.52,2.30 to 1.48,2.75 fc rgb "#c8d9ea" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 21021 "189" at 1,2.53 center font "Helvetica, 6" tc rgb "#333333" front
set object 2023 rect from 1.52,2.30 to 2.48,2.75 fc rgb "#c8d9ea" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 21022 "188" at 2,2.53 center font "Helvetica, 6" tc rgb "#333333" front
set object 2024 rect from 2.52,2.30 to 3.48,2.75 fc rgb "#c4d6e9" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 21023 "184" at 3,2.53 center font "Helvetica, 6" tc rgb "#333333" front
set object 2025 rect from -0.48,2.76 to 0.48,3.21 fc rgb "#eff4f9" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 21024 "233" at 0,2.99 center font "Helvetica, 6" tc rgb "#333333" front
set object 2026 rect from 0.52,2.76 to 1.48,3.21 fc rgb "#dbe6f1" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 21025 "210" at 1,2.99 center font "Helvetica, 6" tc rgb "#333333" front
set object 2027 rect from 1.52,2.76 to 2.48,3.21 fc rgb "#fcfdfe" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 21026 "247" at 2,2.99 center font "Helvetica, 6" tc rgb "#333333" front
set object 2028 rect from 2.52,2.76 to 3.48,3.21 fc rgb "#f9fbfc" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 21027 "244" at 3,2.99 center font "Helvetica, 6" tc rgb "#333333" front
set object 2029 rect from -0.48,3.22 to 0.48,3.67 fc rgb "#faf1f2" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 21028 "265" at 0,3.45 center font "Helvetica, 6" tc rgb "#333333" front
set object 2030 rect from 0.52,3.22 to 1.48,3.67 fc rgb "#fdfafa" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 21029 "255" at 1,3.45 center font "Helvetica, 6" tc rgb "#333333" front
set object 2031 rect from 1.52,3.22 to 2.48,3.67 fc rgb "#f6e5e7" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 21030 "278" at 2,3.45 center font "Helvetica, 6" tc rgb "#333333" front
set object 2032 rect from 2.52,3.22 to 3.48,3.67 fc rgb "#fbf3f4" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 21031 "263" at 3,3.45 center font "Helvetica, 6" tc rgb "#333333" front
set object 2033 rect from -0.48,3.68 to 0.48,4.13 fc rgb "#c14554" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 21032 "451" at 0,3.91 center font "Helvetica, 6" tc rgb "#333333" front
set object 2034 rect from 0.52,3.68 to 1.48,4.13 fc rgb "#c65563" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 21033 "434" at 1,3.91 center font "Helvetica, 6" tc rgb "#333333" front
set object 2035 rect from 1.52,3.68 to 2.48,4.13 fc rgb "#bc3748" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 21034 "466" at 2,3.91 center font "Helvetica, 6" tc rgb "#333333" front
set object 2036 rect from 2.52,3.68 to 3.48,4.13 fc rgb "#c85c6a" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 21035 "426" at 3,3.91 center font "Helvetica, 6" tc rgb "#333333" front
set object 2037 rect from -0.48,4.14 to 0.48,4.59 fc rgb "#f4dee1" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 21036 "285" at 0,4.37 center font "Helvetica, 6" tc rgb "#333333" front
set object 2038 rect from 0.52,4.14 to 1.48,4.59 fc rgb "#e7b7bd" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 21037 "328" at 1,4.37 center font "Helvetica, 6" tc rgb "#333333" front
set object 2039 rect from 1.52,4.14 to 2.48,4.59 fc rgb "#f2dadd" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 21038 "289" at 2,4.37 center font "Helvetica, 6" tc rgb "#333333" front
set object 2040 rect from 2.52,4.14 to 3.48,4.59 fc rgb "#f3dde0" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 21039 "286" at 3,4.37 center font "Helvetica, 6" tc rgb "#333333" front
set object 2041 rect from -0.48,4.60 to 0.48,5.05 fc rgb "#eac2c7" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 21040 "316" at 0,4.83 center font "Helvetica, 6" tc rgb "#333333" front
set object 2042 rect from 0.52,4.60 to 1.48,5.05 fc rgb "#ebc5ca" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 21041 "312" at 1,4.83 center font "Helvetica, 6" tc rgb "#333333" front
set object 2043 rect from 1.52,4.60 to 2.48,5.05 fc rgb "#e6b6bc" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 21042 "329" at 2,4.83 center font "Helvetica, 6" tc rgb "#333333" front
set object 2044 rect from 2.52,4.60 to 3.48,5.05 fc rgb "#edc9cd" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 21043 "308" at 3,4.83 center font "Helvetica, 6" tc rgb "#333333" front
set object 2045 rect from -0.48,5.06 to 0.48,5.51 fc rgb "#c65462" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 21044 "435" at 0,5.29 center font "Helvetica, 6" tc rgb "#333333" front
set object 2046 rect from 0.52,5.06 to 1.48,5.51 fc rgb "#c14757" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 21045 "448" at 1,5.29 center font "Helvetica, 6" tc rgb "#333333" front
set object 2047 rect from 1.52,5.06 to 2.48,5.51 fc rgb "#c34d5c" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 21046 "442" at 2,5.29 center font "Helvetica, 6" tc rgb "#333333" front
set object 2048 rect from 2.52,5.06 to 3.48,5.51 fc rgb "#c24a59" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 21047 "445" at 3,5.29 center font "Helvetica, 6" tc rgb "#333333" front
set object 2049 rect from -0.48,5.52 to 0.48,5.97 fc rgb "#c14655" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 21048 "450" at 0,5.75 center font "Helvetica, 6" tc rgb "#333333" front
set object 2050 rect from 0.52,5.52 to 1.48,5.97 fc rgb "#c95d6a" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 21049 "425" at 1,5.75 center font "Helvetica, 6" tc rgb "#333333" front
set object 2051 rect from 1.52,5.52 to 2.48,5.97 fc rgb "#b52335" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 21050 "487" at 2,5.75 center font "Helvetica, 6" tc rgb "#333333" front
set object 2052 rect from 2.52,5.52 to 3.48,5.97 fc rgb "#cf6f7b" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 21051 "406" at 3,5.75 center font "Helvetica, 6" tc rgb "#333333" front
set object 2053 rect from -0.48,5.98 to 0.48,6.43 fc rgb "#c14555" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 21052 "450" at 0,6.21 center font "Helvetica, 6" tc rgb "#333333" front
set object 2054 rect from 0.52,5.98 to 1.48,6.43 fc rgb "#bd3a4b" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 21053 "462" at 1,6.21 center font "Helvetica, 6" tc rgb "#333333" front
set object 2055 rect from 1.52,5.98 to 2.48,6.43 fc rgb "#c24958" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 21054 "447" at 2,6.21 center font "Helvetica, 6" tc rgb "#333333" front
set object 2056 rect from 2.52,5.98 to 3.48,6.43 fc rgb "#c4505e" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 21055 "439" at 3,6.21 center font "Helvetica, 6" tc rgb "#333333" front
set object 2057 rect from -0.48,6.44 to 0.48,6.89 fc rgb "#e2aab1" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 21056 "341" at 0,6.67 center font "Helvetica, 6" tc rgb "#333333" front
set object 2058 rect from 0.52,6.44 to 1.48,6.89 fc rgb "#e3adb3" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 21057 "339" at 1,6.67 center font "Helvetica, 6" tc rgb "#333333" front
set object 2059 rect from 1.52,6.44 to 2.48,6.89 fc rgb "#e1a6ae" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 21058 "345" at 2,6.67 center font "Helvetica, 6" tc rgb "#333333" front
set object 2060 rect from 2.52,6.44 to 3.48,6.89 fc rgb "#e1a5ac" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 21059 "347" at 3,6.67 center font "Helvetica, 6" tc rgb "#333333" front
set lmargin at screen 0.320
set rmargin at screen 0.439
set bmargin at screen 0.08
set tmargin at screen 0.88
plot NaN notitle

# --- Panel 4: IPRoyal ---
unset label 999
unset object 2001
unset label 21000
unset object 2002
unset label 21001
unset object 2003
unset label 21002
unset object 2004
unset label 21003
unset object 2005
unset label 21004
unset object 2006
unset label 21005
unset object 2007
unset label 21006
unset object 2008
unset label 21007
unset object 2009
unset label 21008
unset object 2010
unset label 21009
unset object 2011
unset label 21010
unset object 2012
unset label 21011
unset object 2013
unset label 21012
unset object 2014
unset label 21013
unset object 2015
unset label 21014
unset object 2016
unset label 21015
unset object 2017
unset label 21016
unset object 2018
unset label 21017
unset object 2019
unset label 21018
unset object 2020
unset label 21019
unset object 2021
unset label 21020
unset object 2022
unset label 21021
unset object 2023
unset label 21022
unset object 2024
unset label 21023
unset object 2025
unset label 21024
unset object 2026
unset label 21025
unset object 2027
unset label 21026
unset object 2028
unset label 21027
unset object 2029
unset label 21028
unset object 2030
unset label 21029
unset object 2031
unset label 21030
unset object 2032
unset label 21031
unset object 2033
unset label 21032
unset object 2034
unset label 21033
unset object 2035
unset label 21034
unset object 2036
unset label 21035
unset object 2037
unset label 21036
unset object 2038
unset label 21037
unset object 2039
unset label 21038
unset object 2040
unset label 21039
unset object 2041
unset label 21040
unset object 2042
unset label 21041
unset object 2043
unset label 21042
unset object 2044
unset label 21043
unset object 2045
unset label 21044
unset object 2046
unset label 21045
unset object 2047
unset label 21046
unset object 2048
unset label 21047
unset object 2049
unset label 21048
unset object 2050
unset label 21049
unset object 2051
unset label 21050
unset object 2052
unset label 21051
unset object 2053
unset label 21052
unset object 2054
unset label 21053
unset object 2055
unset label 21054
unset object 2056
unset label 21055
unset object 2057
unset label 21056
unset object 2058
unset label 21057
unset object 2059
unset label 21058
unset object 2060
unset label 21059
unset ytics
set label 999 "{/Helvetica-Bold IPRoyal (P2P)}" at 1.5,7.1 center font "Helvetica-Bold, 7"
unset key; unset colorbox; unset grid; unset xlabel
set arrow 102 from -0.5,1.38 to 3.5,1.38 nohead lw 0.5 lc rgb "#bbbbbb" front
set arrow 106 from -0.5,3.22 to 3.5,3.22 nohead lw 0.5 lc rgb "#bbbbbb" front
set arrow 107 from -0.5,3.68 to 3.5,3.68 nohead lw 0.5 lc rgb "#bbbbbb" front
set arrow 113 from -0.5,6.44 to 3.5,6.44 nohead lw 0.5 lc rgb "#bbbbbb" front
set object 3001 rect from -0.48,0.00 to 0.48,0.45 fc rgb "#80a7cf" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 31000 "108" at 0,0.23 center font "Helvetica, 6" tc rgb "#333333" front
set object 3002 rect from 0.52,0.00 to 1.48,0.45 fc rgb "#7fa7cf" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 31001 "107" at 1,0.23 center font "Helvetica, 6" tc rgb "#333333" front
set object 3003 rect from 1.52,0.00 to 2.48,0.45 fc rgb "#6796c6" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 31002 "79" at 2,0.23 center font "Helvetica, 6" tc rgb "#333333" front
set object 3004 rect from 2.52,0.00 to 3.48,0.45 fc rgb "#6897c6" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 31003 "80" at 3,0.23 center font "Helvetica, 6" tc rgb "#333333" front
set object 3005 rect from -0.48,0.46 to 0.48,0.91 fc rgb "#6595c5" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 31004 "78" at 0,0.69 center font "Helvetica, 6" tc rgb "#333333" front
set object 3006 rect from 0.52,0.46 to 1.48,0.91 fc rgb "#a5c1dd" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 31005 "149" at 1,0.69 center font "Helvetica, 6" tc rgb "#333333" front
set object 3007 rect from 1.52,0.46 to 2.48,0.91 fc rgb "#90b2d5" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 31006 "125" at 2,0.69 center font "Helvetica, 6" tc rgb "#333333" front
set object 3008 rect from 2.52,0.46 to 3.48,0.91 fc rgb "#94b5d7" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 31007 "130" at 3,0.69 center font "Helvetica, 6" tc rgb "#333333" front
set object 3009 rect from -0.48,0.92 to 0.48,1.37 fc rgb "#c6d8e9" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 31008 "187" at 0,1.15 center font "Helvetica, 6" tc rgb "#333333" front
set object 3010 rect from 0.52,0.92 to 1.48,1.37 fc rgb "#bfd2e7" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 31009 "178" at 1,1.15 center font "Helvetica, 6" tc rgb "#333333" front
set object 3011 rect from 1.52,0.92 to 2.48,1.37 fc rgb "#c3d5e8" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 31010 "183" at 2,1.15 center font "Helvetica, 6" tc rgb "#333333" front
set object 3012 rect from 2.52,0.92 to 3.48,1.37 fc rgb "#c9daeb" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 31011 "190" at 3,1.15 center font "Helvetica, 6" tc rgb "#333333" front
set object 3013 rect from -0.48,1.38 to 0.48,1.83 fc rgb "#c5d7e9" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 31012 "186" at 0,1.61 center font "Helvetica, 6" tc rgb "#333333" front
set object 3014 rect from 0.52,1.38 to 1.48,1.83 fc rgb "#bfd3e7" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 31013 "179" at 1,1.61 center font "Helvetica, 6" tc rgb "#333333" front
set object 3015 rect from 1.52,1.38 to 2.48,1.83 fc rgb "#c9daeb" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 31014 "190" at 2,1.61 center font "Helvetica, 6" tc rgb "#333333" front
set object 3016 rect from 2.52,1.38 to 3.48,1.83 fc rgb "#ceddec" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 31015 "196" at 3,1.61 center font "Helvetica, 6" tc rgb "#333333" front
set object 3017 rect from -0.48,1.84 to 0.48,2.29 fc rgb "#cddcec" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 31016 "194" at 0,2.06 center font "Helvetica, 6" tc rgb "#333333" front
set object 3018 rect from 0.52,1.84 to 1.48,2.29 fc rgb "#d0dfed" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 31017 "198" at 1,2.06 center font "Helvetica, 6" tc rgb "#333333" front
set object 3019 rect from 1.52,1.84 to 2.48,2.29 fc rgb "#cadbeb" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 31018 "191" at 2,2.06 center font "Helvetica, 6" tc rgb "#333333" front
set object 3020 rect from 2.52,1.84 to 3.48,2.29 fc rgb "#cbdbeb" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 31019 "192" at 3,2.06 center font "Helvetica, 6" tc rgb "#333333" front
set object 3021 rect from -0.48,2.30 to 0.48,2.75 fc rgb "#ceddec" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 31020 "196" at 0,2.53 center font "Helvetica, 6" tc rgb "#333333" front
set object 3022 rect from 0.52,2.30 to 1.48,2.75 fc rgb "#c0d3e7" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 31021 "179" at 1,2.53 center font "Helvetica, 6" tc rgb "#333333" front
set object 3023 rect from 1.52,2.30 to 2.48,2.75 fc rgb "#cfdeed" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 31022 "197" at 2,2.53 center font "Helvetica, 6" tc rgb "#333333" front
set object 3024 rect from 2.52,2.30 to 3.48,2.75 fc rgb "#a5c1dd" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 31023 "150" at 3,2.53 center font "Helvetica, 6" tc rgb "#333333" front
set object 3025 rect from -0.48,2.76 to 0.48,3.21 fc rgb "#d6e3ef" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 31024 "205" at 0,2.99 center font "Helvetica, 6" tc rgb "#333333" front
set object 3026 rect from 0.52,2.76 to 1.48,3.21 fc rgb "#dee8f2" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 31025 "213" at 1,2.99 center font "Helvetica, 6" tc rgb "#333333" front
set object 3027 rect from 1.52,2.76 to 2.48,3.21 fc rgb "#e0e9f3" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 31026 "215" at 2,2.99 center font "Helvetica, 6" tc rgb "#333333" front
set object 3028 rect from 2.52,2.76 to 3.48,3.21 fc rgb "#c5d7e9" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 31027 "185" at 3,2.99 center font "Helvetica, 6" tc rgb "#333333" front
set object 3029 rect from -0.48,3.22 to 0.48,3.67 fc rgb "#fbf3f4" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 31028 "262" at 0,3.45 center font "Helvetica, 6" tc rgb "#333333" front
set object 3030 rect from 0.52,3.22 to 1.48,3.67 fc rgb "#fbfcfd" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 31029 "246" at 1,3.45 center font "Helvetica, 6" tc rgb "#333333" front
set object 3031 rect from 1.52,3.22 to 2.48,3.67 fc rgb "#f3f7fa" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 31030 "237" at 2,3.45 center font "Helvetica, 6" tc rgb "#333333" front
set object 3032 rect from 2.52,3.22 to 3.48,3.67 fc rgb "#f3f7fa" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 31031 "238" at 3,3.45 center font "Helvetica, 6" tc rgb "#333333" front
set object 3033 rect from -0.48,3.68 to 0.48,4.13 fc rgb "#dc969f" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 31032 "363" at 0,3.91 center font "Helvetica, 6" tc rgb "#333333" front
set object 3034 rect from 0.52,3.68 to 1.48,4.13 fc rgb "#e2a8b0" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 31033 "343" at 1,3.91 center font "Helvetica, 6" tc rgb "#333333" front
set object 3035 rect from 1.52,3.68 to 2.48,4.13 fc rgb "#d37d87" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 31034 "390" at 2,3.91 center font "Helvetica, 6" tc rgb "#333333" front
set object 3036 rect from 2.52,3.68 to 3.48,4.13 fc rgb "#e4aeb4" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 31035 "337" at 3,3.91 center font "Helvetica, 6" tc rgb "#333333" front
set object 3037 rect from -0.48,4.14 to 0.48,4.59 fc rgb "#e6b6bc" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 31036 "328" at 0,4.37 center font "Helvetica, 6" tc rgb "#333333" front
set object 3038 rect from 0.52,4.14 to 1.48,4.59 fc rgb "#eac0c5" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 31037 "318" at 1,4.37 center font "Helvetica, 6" tc rgb "#333333" front
set object 3039 rect from 1.52,4.14 to 2.48,4.59 fc rgb "#ebc4c9" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 31038 "314" at 2,4.37 center font "Helvetica, 6" tc rgb "#333333" front
set object 3040 rect from 2.52,4.14 to 3.48,4.59 fc rgb "#e9bfc5" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 31039 "318" at 3,4.37 center font "Helvetica, 6" tc rgb "#333333" front
set object 3041 rect from -0.48,4.60 to 0.48,5.05 fc rgb "#e1a5ac" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 31040 "347" at 0,4.83 center font "Helvetica, 6" tc rgb "#333333" front
set object 3042 rect from 0.52,4.60 to 1.48,5.05 fc rgb "#edcbd0" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 31041 "305" at 1,4.83 center font "Helvetica, 6" tc rgb "#333333" front
set object 3043 rect from 1.52,4.60 to 2.48,5.05 fc rgb "#e8bac0" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 31042 "324" at 2,4.83 center font "Helvetica, 6" tc rgb "#333333" front
set object 3044 rect from 2.52,4.60 to 3.48,5.05 fc rgb "#eac0c5" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 31043 "318" at 3,4.83 center font "Helvetica, 6" tc rgb "#333333" front
set object 3045 rect from -0.48,5.06 to 0.48,5.51 fc rgb "#d0727d" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 31044 "402" at 0,5.29 center font "Helvetica, 6" tc rgb "#333333" front
set object 3046 rect from 0.52,5.06 to 1.48,5.51 fc rgb "#dd99a1" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 31045 "360" at 1,5.29 center font "Helvetica, 6" tc rgb "#333333" front
set object 3047 rect from 1.52,5.06 to 2.48,5.51 fc rgb "#e2a8af" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 31046 "343" at 2,5.29 center font "Helvetica, 6" tc rgb "#333333" front
set object 3048 rect from 2.52,5.06 to 3.48,5.51 fc rgb "#d37c87" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 31047 "391" at 3,5.29 center font "Helvetica, 6" tc rgb "#333333" front
set object 3049 rect from -0.48,5.52 to 0.48,5.97 fc rgb "#c55260" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 31048 "437" at 0,5.75 center font "Helvetica, 6" tc rgb "#333333" front
set object 3050 rect from 0.52,5.52 to 1.48,5.97 fc rgb "#ce6e7a" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 31049 "407" at 1,5.75 center font "Helvetica, 6" tc rgb "#333333" front
set object 3051 rect from 1.52,5.52 to 2.48,5.97 fc rgb "#d0747f" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 31050 "400" at 2,5.75 center font "Helvetica, 6" tc rgb "#333333" front
set object 3052 rect from 2.52,5.52 to 3.48,5.97 fc rgb "#c95d6a" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 31051 "425" at 3,5.75 center font "Helvetica, 6" tc rgb "#333333" front
set object 3053 rect from -0.48,5.98 to 0.48,6.43 fc rgb "#d78892" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 31052 "378" at 0,6.21 center font "Helvetica, 6" tc rgb "#333333" front
set object 3054 rect from 0.52,5.98 to 1.48,6.43 fc rgb "#de9da5" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 31053 "356" at 1,6.21 center font "Helvetica, 6" tc rgb "#333333" front
set object 3055 rect from 1.52,5.98 to 2.48,6.43 fc rgb "#e2a8af" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 31054 "343" at 2,6.21 center font "Helvetica, 6" tc rgb "#333333" front
set object 3056 rect from 2.52,5.98 to 3.48,6.43 fc rgb "#e3abb2" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 31055 "341" at 3,6.21 center font "Helvetica, 6" tc rgb "#333333" front
set object 3057 rect from -0.48,6.44 to 0.48,6.89 fc rgb "#de9ea6" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 31056 "354" at 0,6.67 center font "Helvetica, 6" tc rgb "#333333" front
set object 3058 rect from 0.52,6.44 to 1.48,6.89 fc rgb "#dfa0a7" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 31057 "353" at 1,6.67 center font "Helvetica, 6" tc rgb "#333333" front
set object 3059 rect from 1.52,6.44 to 2.48,6.89 fc rgb "#db959e" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 31058 "364" at 2,6.67 center font "Helvetica, 6" tc rgb "#333333" front
set object 3060 rect from 2.52,6.44 to 3.48,6.89 fc rgb "#de9da5" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 31059 "356" at 3,6.67 center font "Helvetica, 6" tc rgb "#333333" front
set lmargin at screen 0.445
set rmargin at screen 0.564
set bmargin at screen 0.08
set tmargin at screen 0.88
plot NaN notitle

# --- Panel 5: NetNut ---
unset label 999
unset object 3001
unset label 31000
unset object 3002
unset label 31001
unset object 3003
unset label 31002
unset object 3004
unset label 31003
unset object 3005
unset label 31004
unset object 3006
unset label 31005
unset object 3007
unset label 31006
unset object 3008
unset label 31007
unset object 3009
unset label 31008
unset object 3010
unset label 31009
unset object 3011
unset label 31010
unset object 3012
unset label 31011
unset object 3013
unset label 31012
unset object 3014
unset label 31013
unset object 3015
unset label 31014
unset object 3016
unset label 31015
unset object 3017
unset label 31016
unset object 3018
unset label 31017
unset object 3019
unset label 31018
unset object 3020
unset label 31019
unset object 3021
unset label 31020
unset object 3022
unset label 31021
unset object 3023
unset label 31022
unset object 3024
unset label 31023
unset object 3025
unset label 31024
unset object 3026
unset label 31025
unset object 3027
unset label 31026
unset object 3028
unset label 31027
unset object 3029
unset label 31028
unset object 3030
unset label 31029
unset object 3031
unset label 31030
unset object 3032
unset label 31031
unset object 3033
unset label 31032
unset object 3034
unset label 31033
unset object 3035
unset label 31034
unset object 3036
unset label 31035
unset object 3037
unset label 31036
unset object 3038
unset label 31037
unset object 3039
unset label 31038
unset object 3040
unset label 31039
unset object 3041
unset label 31040
unset object 3042
unset label 31041
unset object 3043
unset label 31042
unset object 3044
unset label 31043
unset object 3045
unset label 31044
unset object 3046
unset label 31045
unset object 3047
unset label 31046
unset object 3048
unset label 31047
unset object 3049
unset label 31048
unset object 3050
unset label 31049
unset object 3051
unset label 31050
unset object 3052
unset label 31051
unset object 3053
unset label 31052
unset object 3054
unset label 31053
unset object 3055
unset label 31054
unset object 3056
unset label 31055
unset object 3057
unset label 31056
unset object 3058
unset label 31057
unset object 3059
unset label 31058
unset object 3060
unset label 31059
unset ytics
set label 999 "{/Helvetica-Bold NetNut (ISP)}" at 1.5,7.1 center font "Helvetica-Bold, 7"
unset key; unset colorbox; unset grid; unset xlabel
set arrow 102 from -0.5,1.38 to 3.5,1.38 nohead lw 0.5 lc rgb "#bbbbbb" front
set arrow 106 from -0.5,3.22 to 3.5,3.22 nohead lw 0.5 lc rgb "#bbbbbb" front
set arrow 107 from -0.5,3.68 to 3.5,3.68 nohead lw 0.5 lc rgb "#bbbbbb" front
set arrow 113 from -0.5,6.44 to 3.5,6.44 nohead lw 0.5 lc rgb "#bbbbbb" front
set object 4001 rect from -0.48,0.00 to 0.48,0.45 fc rgb "#92b4d6" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 41000 "128" at 0,0.23 center font "Helvetica, 6" tc rgb "#333333" front
set object 4002 rect from 0.52,0.00 to 1.48,0.45 fc rgb "#8eb1d4" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 41001 "123" at 1,0.23 center font "Helvetica, 6" tc rgb "#333333" front
set object 4003 rect from 1.52,0.00 to 2.48,0.45 fc rgb "#92b4d6" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 41002 "127" at 2,0.23 center font "Helvetica, 6" tc rgb "#333333" front
set object 4004 rect from 2.52,0.00 to 3.48,0.45 fc rgb "#76a0cb" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 41003 "96" at 3,0.23 center font "Helvetica, 6" tc rgb "#333333" front
set object 4005 rect from -0.48,0.46 to 0.48,0.91 fc rgb "#568abf" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 41004 "60" at 0,0.69 center font "Helvetica, 6" tc rgb "#333333" front
set object 4006 rect from 0.52,0.46 to 1.48,0.91 fc rgb "#5a8dc1" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 41005 "65" at 1,0.69 center font "Helvetica, 6" tc rgb "#333333" front
set object 4007 rect from 1.52,0.46 to 2.48,0.91 fc rgb "#558abf" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 41006 "59" at 2,0.69 center font "Helvetica, 6" tc rgb "#333333" front
set object 4008 rect from 2.52,0.46 to 3.48,0.91 fc rgb "#5c8fc2" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 41007 "68" at 3,0.69 center font "Helvetica, 6" tc rgb "#333333" front
set object 4009 rect from -0.48,0.92 to 0.48,1.37 fc rgb "#94b5d7" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 41008 "130" at 0,1.15 center font "Helvetica, 6" tc rgb "#333333" front
set object 4010 rect from 0.52,0.92 to 1.48,1.37 fc rgb "#85abd1" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 41009 "113" at 1,1.15 center font "Helvetica, 6" tc rgb "#333333" front
set object 4011 rect from 1.52,0.92 to 2.48,1.37 fc rgb "#91b3d5" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 41010 "126" at 2,1.15 center font "Helvetica, 6" tc rgb "#333333" front
set object 4012 rect from 2.52,0.92 to 3.48,1.37 fc rgb "#80a8cf" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 41011 "108" at 3,1.15 center font "Helvetica, 6" tc rgb "#333333" front
set object 4013 rect from -0.48,1.38 to 0.48,1.83 fc rgb "#99b8d8" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 41012 "135" at 0,1.61 center font "Helvetica, 6" tc rgb "#333333" front
set object 4014 rect from 0.52,1.38 to 1.48,1.83 fc rgb "#97b7d8" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 41013 "133" at 1,1.61 center font "Helvetica, 6" tc rgb "#333333" front
set object 4015 rect from 1.52,1.38 to 2.48,1.83 fc rgb "#9dbcda" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 41014 "141" at 2,1.61 center font "Helvetica, 6" tc rgb "#333333" front
set object 4016 rect from 2.52,1.38 to 3.48,1.83 fc rgb "#8db0d4" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 41015 "122" at 3,1.61 center font "Helvetica, 6" tc rgb "#333333" front
set object 4017 rect from -0.48,1.84 to 0.48,2.29 fc rgb "#a1bedc" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 41016 "145" at 0,2.06 center font "Helvetica, 6" tc rgb "#333333" front
set object 4018 rect from 0.52,1.84 to 1.48,2.29 fc rgb "#a0bddb" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 41017 "144" at 1,2.06 center font "Helvetica, 6" tc rgb "#333333" front
set object 4019 rect from 1.52,1.84 to 2.48,2.29 fc rgb "#9fbddb" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 41018 "143" at 2,2.06 center font "Helvetica, 6" tc rgb "#333333" front
set object 4020 rect from 2.52,1.84 to 3.48,2.29 fc rgb "#a1bedc" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 41019 "145" at 3,2.06 center font "Helvetica, 6" tc rgb "#333333" front
set object 4021 rect from -0.48,2.30 to 0.48,2.75 fc rgb "#9cbbda" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 41020 "139" at 0,2.53 center font "Helvetica, 6" tc rgb "#333333" front
set object 4022 rect from 0.52,2.30 to 1.48,2.75 fc rgb "#97b8d8" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 41021 "134" at 1,2.53 center font "Helvetica, 6" tc rgb "#333333" front
set object 4023 rect from 1.52,2.30 to 2.48,2.75 fc rgb "#97b7d8" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 41022 "133" at 2,2.53 center font "Helvetica, 6" tc rgb "#333333" front
set object 4024 rect from 2.52,2.30 to 3.48,2.75 fc rgb "#97b7d8" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 41023 "134" at 3,2.53 center font "Helvetica, 6" tc rgb "#333333" front
set object 4025 rect from -0.48,2.76 to 0.48,3.21 fc rgb "#d1dfed" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 41024 "199" at 0,2.99 center font "Helvetica, 6" tc rgb "#333333" front
set object 4026 rect from 0.52,2.76 to 1.48,3.21 fc rgb "#cddcec" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 41025 "194" at 1,2.99 center font "Helvetica, 6" tc rgb "#333333" front
set object 4027 rect from 1.52,2.76 to 2.48,3.21 fc rgb "#c9d9ea" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 41026 "189" at 2,2.99 center font "Helvetica, 6" tc rgb "#333333" front
set object 4028 rect from 2.52,2.76 to 3.48,3.21 fc rgb "#ceddec" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 41027 "195" at 3,2.99 center font "Helvetica, 6" tc rgb "#333333" front
set object 4029 rect from -0.48,3.22 to 0.48,3.67 fc rgb "#bfd3e7" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 41028 "179" at 0,3.45 center font "Helvetica, 6" tc rgb "#333333" front
set object 4030 rect from 0.52,3.22 to 1.48,3.67 fc rgb "#d0dfed" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 41029 "198" at 1,3.45 center font "Helvetica, 6" tc rgb "#333333" front
set object 4031 rect from 1.52,3.22 to 2.48,3.67 fc rgb "#c7d8ea" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 41030 "187" at 2,3.45 center font "Helvetica, 6" tc rgb "#333333" front
set object 4032 rect from 2.52,3.22 to 3.48,3.67 fc rgb "#cbdbeb" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 41031 "192" at 3,3.45 center font "Helvetica, 6" tc rgb "#333333" front
set object 4033 rect from -0.48,3.68 to 0.48,4.13 fc rgb "#f2f6fa" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 41032 "235" at 0,3.91 center font "Helvetica, 6" tc rgb "#333333" front
set object 4034 rect from 0.52,3.68 to 1.48,4.13 fc rgb "#f4dee1" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 41033 "285" at 1,3.91 center font "Helvetica, 6" tc rgb "#333333" front
set object 4035 rect from 1.52,3.68 to 2.48,4.13 fc rgb "#fefcfc" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 41034 "253" at 2,3.91 center font "Helvetica, 6" tc rgb "#333333" front
set object 4036 rect from 2.52,3.68 to 3.48,4.13 fc rgb "#f0f4f9" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 41035 "233" at 3,3.91 center font "Helvetica, 6" tc rgb "#333333" front
set object 4037 rect from -0.48,4.14 to 0.48,4.59 fc rgb "#f1d6d9" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 41036 "294" at 0,4.37 center font "Helvetica, 6" tc rgb "#333333" front
set object 4038 rect from 0.52,4.14 to 1.48,4.59 fc rgb "#f9edee" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 41037 "269" at 1,4.37 center font "Helvetica, 6" tc rgb "#333333" front
set object 4039 rect from 1.52,4.14 to 2.48,4.59 fc rgb "#f6e6e8" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 41038 "277" at 2,4.37 center font "Helvetica, 6" tc rgb "#333333" front
set object 4040 rect from 2.52,4.14 to 3.48,4.59 fc rgb "#f9edee" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 41039 "269" at 3,4.37 center font "Helvetica, 6" tc rgb "#333333" front
set object 4041 rect from -0.48,4.60 to 0.48,5.05 fc rgb "#f4dee1" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 41040 "285" at 0,4.83 center font "Helvetica, 6" tc rgb "#333333" front
set object 4042 rect from 0.52,4.60 to 1.48,5.05 fc rgb "#f3dcdf" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 41041 "287" at 1,4.83 center font "Helvetica, 6" tc rgb "#333333" front
set object 4043 rect from 1.52,4.60 to 2.48,5.05 fc rgb "#efd0d4" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 41042 "300" at 2,4.83 center font "Helvetica, 6" tc rgb "#333333" front
set object 4044 rect from 2.52,4.60 to 3.48,5.05 fc rgb "#f2d9dc" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 41043 "290" at 3,4.83 center font "Helvetica, 6" tc rgb "#333333" front
set object 4045 rect from -0.48,5.06 to 0.48,5.51 fc rgb "#fefdfd" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 41044 "252" at 0,5.29 center font "Helvetica, 6" tc rgb "#333333" front
set object 4046 rect from 0.52,5.06 to 1.48,5.51 fc rgb "#fbf5f5" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 41045 "261" at 1,5.29 center font "Helvetica, 6" tc rgb "#333333" front
set object 4047 rect from 1.52,5.06 to 2.48,5.51 fc rgb "#fdf9f9" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 41046 "256" at 2,5.29 center font "Helvetica, 6" tc rgb "#333333" front
set object 4048 rect from 2.52,5.06 to 3.48,5.51 fc rgb "#fcfdfe" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 41047 "247" at 3,5.29 center font "Helvetica, 6" tc rgb "#333333" front
set object 4049 rect from -0.48,5.52 to 0.48,5.97 fc rgb "#dd99a2" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 41048 "360" at 0,5.75 center font "Helvetica, 6" tc rgb "#333333" front
set object 4050 rect from 0.52,5.52 to 1.48,5.97 fc rgb "#d68690" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 41049 "380" at 1,5.75 center font "Helvetica, 6" tc rgb "#333333" front
set object 4051 rect from 1.52,5.52 to 2.48,5.97 fc rgb "#d88c95" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 41050 "374" at 2,5.75 center font "Helvetica, 6" tc rgb "#333333" front
set object 4052 rect from 2.52,5.52 to 3.48,5.97 fc rgb "#de9da5" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 41051 "355" at 3,5.75 center font "Helvetica, 6" tc rgb "#333333" front
set object 4053 rect from -0.48,5.98 to 0.48,6.43 fc rgb "#e8bac0" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 41052 "324" at 0,6.21 center font "Helvetica, 6" tc rgb "#333333" front
set object 4054 rect from 0.52,5.98 to 1.48,6.43 fc rgb "#f0d2d5" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 41053 "298" at 1,6.21 center font "Helvetica, 6" tc rgb "#333333" front
set object 4055 rect from 1.52,5.98 to 2.48,6.43 fc rgb "#f1d5d8" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 41054 "295" at 2,6.21 center font "Helvetica, 6" tc rgb "#333333" front
set object 4056 rect from 2.52,5.98 to 3.48,6.43 fc rgb "#ecc8cc" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 41055 "309" at 3,6.21 center font "Helvetica, 6" tc rgb "#333333" front
set object 4057 rect from -0.48,6.44 to 0.48,6.89 fc rgb "#eac2c7" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 41056 "316" at 0,6.67 center font "Helvetica, 6" tc rgb "#333333" front
set object 4058 rect from 0.52,6.44 to 1.48,6.89 fc rgb "#e4afb6" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 41057 "336" at 1,6.67 center font "Helvetica, 6" tc rgb "#333333" front
set object 4059 rect from 1.52,6.44 to 2.48,6.89 fc rgb "#e6b4ba" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 41058 "330" at 2,6.67 center font "Helvetica, 6" tc rgb "#333333" front
set object 4060 rect from 2.52,6.44 to 3.48,6.89 fc rgb "#e6b6bc" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 41059 "329" at 3,6.67 center font "Helvetica, 6" tc rgb "#333333" front
set lmargin at screen 0.570
set rmargin at screen 0.689
set bmargin at screen 0.08
set tmargin at screen 0.88
plot NaN notitle

# --- Panel 6: Oxylabs ISP ---
unset label 999
unset object 4001
unset label 41000
unset object 4002
unset label 41001
unset object 4003
unset label 41002
unset object 4004
unset label 41003
unset object 4005
unset label 41004
unset object 4006
unset label 41005
unset object 4007
unset label 41006
unset object 4008
unset label 41007
unset object 4009
unset label 41008
unset object 4010
unset label 41009
unset object 4011
unset label 41010
unset object 4012
unset label 41011
unset object 4013
unset label 41012
unset object 4014
unset label 41013
unset object 4015
unset label 41014
unset object 4016
unset label 41015
unset object 4017
unset label 41016
unset object 4018
unset label 41017
unset object 4019
unset label 41018
unset object 4020
unset label 41019
unset object 4021
unset label 41020
unset object 4022
unset label 41021
unset object 4023
unset label 41022
unset object 4024
unset label 41023
unset object 4025
unset label 41024
unset object 4026
unset label 41025
unset object 4027
unset label 41026
unset object 4028
unset label 41027
unset object 4029
unset label 41028
unset object 4030
unset label 41029
unset object 4031
unset label 41030
unset object 4032
unset label 41031
unset object 4033
unset label 41032
unset object 4034
unset label 41033
unset object 4035
unset label 41034
unset object 4036
unset label 41035
unset object 4037
unset label 41036
unset object 4038
unset label 41037
unset object 4039
unset label 41038
unset object 4040
unset label 41039
unset object 4041
unset label 41040
unset object 4042
unset label 41041
unset object 4043
unset label 41042
unset object 4044
unset label 41043
unset object 4045
unset label 41044
unset object 4046
unset label 41045
unset object 4047
unset label 41046
unset object 4048
unset label 41047
unset object 4049
unset label 41048
unset object 4050
unset label 41049
unset object 4051
unset label 41050
unset object 4052
unset label 41051
unset object 4053
unset label 41052
unset object 4054
unset label 41053
unset object 4055
unset label 41054
unset object 4056
unset label 41055
unset object 4057
unset label 41056
unset object 4058
unset label 41057
unset object 4059
unset label 41058
unset object 4060
unset label 41059
unset ytics
set label 999 "{/Helvetica-Bold Oxylabs ISP (ISP)}" at 1.5,7.1 center font "Helvetica-Bold, 7"
unset key; unset colorbox; unset grid; unset xlabel
set arrow 102 from -0.5,1.38 to 3.5,1.38 nohead lw 0.5 lc rgb "#bbbbbb" front
set arrow 106 from -0.5,3.22 to 3.5,3.22 nohead lw 0.5 lc rgb "#bbbbbb" front
set arrow 107 from -0.5,3.68 to 3.5,3.68 nohead lw 0.5 lc rgb "#bbbbbb" front
set arrow 113 from -0.5,6.44 to 3.5,6.44 nohead lw 0.5 lc rgb "#bbbbbb" front
set object 5001 rect from -0.48,0.00 to 0.48,0.45 fc rgb "#aac4df" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 51000 "155" at 0,0.23 center font "Helvetica, 6" tc rgb "#333333" front
set object 5002 rect from 0.52,0.00 to 1.48,0.45 fc rgb "#bacfe5" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 51001 "173" at 1,0.23 center font "Helvetica, 6" tc rgb "#333333" front
set object 5003 rect from 1.52,0.00 to 2.48,0.45 fc rgb "#d4e1ee" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 51002 "202" at 2,0.23 center font "Helvetica, 6" tc rgb "#333333" front
set object 5004 rect from 2.52,0.00 to 3.48,0.45 fc rgb "#ceddec" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 51003 "195" at 3,0.23 center font "Helvetica, 6" tc rgb "#333333" front
set object 5005 rect from -0.48,0.46 to 0.48,0.91 fc rgb "#c9d9ea" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 51004 "189" at 0,0.69 center font "Helvetica, 6" tc rgb "#333333" front
set object 5006 rect from 0.52,0.46 to 1.48,0.91 fc rgb "#cbdbeb" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 51005 "192" at 1,0.69 center font "Helvetica, 6" tc rgb "#333333" front
set object 5007 rect from 1.52,0.46 to 2.48,0.91 fc rgb "#d1dfed" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 51006 "198" at 2,0.69 center font "Helvetica, 6" tc rgb "#333333" front
set object 5008 rect from 2.52,0.46 to 3.48,0.91 fc rgb "#b3cae2" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 51007 "165" at 3,0.69 center font "Helvetica, 6" tc rgb "#333333" front
set object 5009 rect from -0.48,0.92 to 0.48,1.37 fc rgb "#ceddec" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 51008 "195" at 0,1.15 center font "Helvetica, 6" tc rgb "#333333" front
set object 5010 rect from 0.52,0.92 to 1.48,1.37 fc rgb "#d8e4f0" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 51009 "207" at 1,1.15 center font "Helvetica, 6" tc rgb "#333333" front
set object 5011 rect from 1.52,0.92 to 2.48,1.37 fc rgb "#d4e1ef" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 51010 "203" at 2,1.15 center font "Helvetica, 6" tc rgb "#333333" front
set object 5012 rect from 2.52,0.92 to 3.48,1.37 fc rgb "#d3e1ee" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 51011 "201" at 3,1.15 center font "Helvetica, 6" tc rgb "#333333" front
set object 5013 rect from -0.48,1.38 to 0.48,1.83 fc rgb "#cadaeb" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 51012 "191" at 0,1.61 center font "Helvetica, 6" tc rgb "#333333" front
set object 5014 rect from 0.52,1.38 to 1.48,1.83 fc rgb "#cadaeb" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 51013 "191" at 1,1.61 center font "Helvetica, 6" tc rgb "#333333" front
set object 5015 rect from 1.52,1.38 to 2.48,1.83 fc rgb "#dbe6f1" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 51014 "210" at 2,1.61 center font "Helvetica, 6" tc rgb "#333333" front
set object 5016 rect from 2.52,1.38 to 3.48,1.83 fc rgb "#d1dfed" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 51015 "198" at 3,1.61 center font "Helvetica, 6" tc rgb "#333333" front
set object 5017 rect from -0.48,1.84 to 0.48,2.29 fc rgb "#bbd0e5" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 51016 "175" at 0,2.06 center font "Helvetica, 6" tc rgb "#333333" front
set object 5018 rect from 0.52,1.84 to 1.48,2.29 fc rgb "#ceddec" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 51017 "195" at 1,2.06 center font "Helvetica, 6" tc rgb "#333333" front
set object 5019 rect from 1.52,1.84 to 2.48,2.29 fc rgb "#d3e1ee" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 51018 "201" at 2,2.06 center font "Helvetica, 6" tc rgb "#333333" front
set object 5020 rect from 2.52,1.84 to 3.48,2.29 fc rgb "#d7e3f0" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 51019 "205" at 3,2.06 center font "Helvetica, 6" tc rgb "#333333" front
set object 5021 rect from -0.48,2.30 to 0.48,2.75 fc rgb "#c9daea" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 51020 "190" at 0,2.53 center font "Helvetica, 6" tc rgb "#333333" front
set object 5022 rect from 0.52,2.30 to 1.48,2.75 fc rgb "#c6d7e9" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 51021 "186" at 1,2.53 center font "Helvetica, 6" tc rgb "#333333" front
set object 5023 rect from 1.52,2.30 to 2.48,2.75 fc rgb "#d2e0ee" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 51022 "200" at 2,2.53 center font "Helvetica, 6" tc rgb "#333333" front
set object 5024 rect from 2.52,2.30 to 3.48,2.75 fc rgb "#ccdcec" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 51023 "193" at 3,2.53 center font "Helvetica, 6" tc rgb "#333333" front
set object 5025 rect from -0.48,2.76 to 0.48,3.21 fc rgb "#d1dfee" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 51024 "199" at 0,2.99 center font "Helvetica, 6" tc rgb "#333333" front
set object 5026 rect from 0.52,2.76 to 1.48,3.21 fc rgb "#c6d8e9" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 51025 "187" at 1,2.99 center font "Helvetica, 6" tc rgb "#333333" front
set object 5027 rect from 1.52,2.76 to 2.48,3.21 fc rgb "#d3e0ee" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 51026 "201" at 2,2.99 center font "Helvetica, 6" tc rgb "#333333" front
set object 5028 rect from 2.52,2.76 to 3.48,3.21 fc rgb "#c9daeb" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 51027 "190" at 3,2.99 center font "Helvetica, 6" tc rgb "#333333" front
set object 5029 rect from -0.48,3.22 to 0.48,3.67 fc rgb "#cedded" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 51028 "196" at 0,3.45 center font "Helvetica, 6" tc rgb "#333333" front
set object 5030 rect from 0.52,3.22 to 1.48,3.67 fc rgb "#c6d8ea" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 51029 "187" at 1,3.45 center font "Helvetica, 6" tc rgb "#333333" front
set object 5031 rect from 1.52,3.22 to 2.48,3.67 fc rgb "#dfe9f3" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 51030 "215" at 2,3.45 center font "Helvetica, 6" tc rgb "#333333" front
set object 5032 rect from 2.52,3.22 to 3.48,3.67 fc rgb "#c0d3e7" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 51031 "179" at 3,3.45 center font "Helvetica, 6" tc rgb "#333333" front
set object 5033 rect from -0.48,3.68 to 0.48,4.13 fc rgb "#d1dfee" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 51032 "199" at 0,3.91 center font "Helvetica, 6" tc rgb "#333333" front
set object 5034 rect from 0.52,3.68 to 1.48,4.13 fc rgb "#cfdeed" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 51033 "197" at 1,3.91 center font "Helvetica, 6" tc rgb "#333333" front
set object 5035 rect from 1.52,3.68 to 2.48,4.13 fc rgb "#d1dfed" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 51034 "198" at 2,3.91 center font "Helvetica, 6" tc rgb "#333333" front
set object 5036 rect from 2.52,3.68 to 3.48,4.13 fc rgb "#c1d4e7" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 51035 "180" at 3,3.91 center font "Helvetica, 6" tc rgb "#333333" front
set object 5037 rect from -0.48,4.14 to 0.48,4.59 fc rgb "#c4d6e9" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 51036 "184" at 0,4.37 center font "Helvetica, 6" tc rgb "#333333" front
set object 5038 rect from 0.52,4.14 to 1.48,4.59 fc rgb "#c6d8e9" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 51037 "186" at 1,4.37 center font "Helvetica, 6" tc rgb "#333333" front
set object 5039 rect from 1.52,4.14 to 2.48,4.59 fc rgb "#c4d6e9" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 51038 "184" at 2,4.37 center font "Helvetica, 6" tc rgb "#333333" front
set object 5040 rect from 2.52,4.14 to 3.48,4.59 fc rgb "#cbdbeb" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 51039 "192" at 3,4.37 center font "Helvetica, 6" tc rgb "#333333" front
set object 5041 rect from -0.48,4.60 to 0.48,5.05 fc rgb "#cedded" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 51040 "196" at 0,4.83 center font "Helvetica, 6" tc rgb "#333333" front
set object 5042 rect from 0.52,4.60 to 1.48,5.05 fc rgb "#bcd1e6" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 51041 "175" at 1,4.83 center font "Helvetica, 6" tc rgb "#333333" front
set object 5043 rect from 1.52,4.60 to 2.48,5.05 fc rgb "#d0dfed" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 51042 "198" at 2,4.83 center font "Helvetica, 6" tc rgb "#333333" front
set object 5044 rect from 2.52,4.60 to 3.48,5.05 fc rgb "#c3d5e8" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 51043 "183" at 3,4.83 center font "Helvetica, 6" tc rgb "#333333" front
set object 5045 rect from -0.48,5.06 to 0.48,5.51 fc rgb "#d1dfee" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 51044 "199" at 0,5.29 center font "Helvetica, 6" tc rgb "#333333" front
set object 5046 rect from 0.52,5.06 to 1.48,5.51 fc rgb "#ccdcec" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 51045 "193" at 1,5.29 center font "Helvetica, 6" tc rgb "#333333" front
set object 5047 rect from 1.52,5.06 to 2.48,5.51 fc rgb "#d1dfed" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 51046 "199" at 2,5.29 center font "Helvetica, 6" tc rgb "#333333" front
set object 5048 rect from 2.52,5.06 to 3.48,5.51 fc rgb "#ccdcec" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 51047 "193" at 3,5.29 center font "Helvetica, 6" tc rgb "#333333" front
set object 5049 rect from -0.48,5.52 to 0.48,5.97 fc rgb "#c3d5e8" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 51048 "183" at 0,5.75 center font "Helvetica, 6" tc rgb "#333333" front
set object 5050 rect from 0.52,5.52 to 1.48,5.97 fc rgb "#d6e2ef" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 51049 "204" at 1,5.75 center font "Helvetica, 6" tc rgb "#333333" front
set object 5051 rect from 1.52,5.52 to 2.48,5.97 fc rgb "#d3e0ee" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 51050 "201" at 2,5.75 center font "Helvetica, 6" tc rgb "#333333" front
set object 5052 rect from 2.52,5.52 to 3.48,5.97 fc rgb "#c5d7e9" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 51051 "185" at 3,5.75 center font "Helvetica, 6" tc rgb "#333333" front
set object 5053 rect from -0.48,5.98 to 0.48,6.43 fc rgb "#d0dfed" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 51052 "198" at 0,6.21 center font "Helvetica, 6" tc rgb "#333333" front
set object 5054 rect from 0.52,5.98 to 1.48,6.43 fc rgb "#c8d9ea" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 51053 "189" at 1,6.21 center font "Helvetica, 6" tc rgb "#333333" front
set object 5055 rect from 1.52,5.98 to 2.48,6.43 fc rgb "#d8e4f0" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 51054 "206" at 2,6.21 center font "Helvetica, 6" tc rgb "#333333" front
set object 5056 rect from 2.52,5.98 to 3.48,6.43 fc rgb "#c6d8e9" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 51055 "186" at 3,6.21 center font "Helvetica, 6" tc rgb "#333333" front
set object 5057 rect from -0.48,6.44 to 0.48,6.89 fc rgb "#cadaeb" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 51056 "191" at 0,6.67 center font "Helvetica, 6" tc rgb "#333333" front
set object 5058 rect from 0.52,6.44 to 1.48,6.89 fc rgb "#cadbeb" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 51057 "191" at 1,6.67 center font "Helvetica, 6" tc rgb "#333333" front
set object 5059 rect from 1.52,6.44 to 2.48,6.89 fc rgb "#d5e2ef" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 51058 "203" at 2,6.67 center font "Helvetica, 6" tc rgb "#333333" front
set object 5060 rect from 2.52,6.44 to 3.48,6.89 fc rgb "#d0deed" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 51059 "197" at 3,6.67 center font "Helvetica, 6" tc rgb "#333333" front
set lmargin at screen 0.695
set rmargin at screen 0.814
set bmargin at screen 0.08
set tmargin at screen 0.88
plot NaN notitle

# --- Panel 7: Oxylabs Mob. ---
unset label 999
unset object 5001
unset label 51000
unset object 5002
unset label 51001
unset object 5003
unset label 51002
unset object 5004
unset label 51003
unset object 5005
unset label 51004
unset object 5006
unset label 51005
unset object 5007
unset label 51006
unset object 5008
unset label 51007
unset object 5009
unset label 51008
unset object 5010
unset label 51009
unset object 5011
unset label 51010
unset object 5012
unset label 51011
unset object 5013
unset label 51012
unset object 5014
unset label 51013
unset object 5015
unset label 51014
unset object 5016
unset label 51015
unset object 5017
unset label 51016
unset object 5018
unset label 51017
unset object 5019
unset label 51018
unset object 5020
unset label 51019
unset object 5021
unset label 51020
unset object 5022
unset label 51021
unset object 5023
unset label 51022
unset object 5024
unset label 51023
unset object 5025
unset label 51024
unset object 5026
unset label 51025
unset object 5027
unset label 51026
unset object 5028
unset label 51027
unset object 5029
unset label 51028
unset object 5030
unset label 51029
unset object 5031
unset label 51030
unset object 5032
unset label 51031
unset object 5033
unset label 51032
unset object 5034
unset label 51033
unset object 5035
unset label 51034
unset object 5036
unset label 51035
unset object 5037
unset label 51036
unset object 5038
unset label 51037
unset object 5039
unset label 51038
unset object 5040
unset label 51039
unset object 5041
unset label 51040
unset object 5042
unset label 51041
unset object 5043
unset label 51042
unset object 5044
unset label 51043
unset object 5045
unset label 51044
unset object 5046
unset label 51045
unset object 5047
unset label 51046
unset object 5048
unset label 51047
unset object 5049
unset label 51048
unset object 5050
unset label 51049
unset object 5051
unset label 51050
unset object 5052
unset label 51051
unset object 5053
unset label 51052
unset object 5054
unset label 51053
unset object 5055
unset label 51054
unset object 5056
unset label 51055
unset object 5057
unset label 51056
unset object 5058
unset label 51057
unset object 5059
unset label 51058
unset object 5060
unset label 51059
unset ytics
set label 999 "{/Helvetica-Bold Oxylabs Mob. (Mobile)}" at 1.5,7.1 center font "Helvetica-Bold, 7"
unset key; unset colorbox; unset grid; unset xlabel
set arrow 102 from -0.5,1.38 to 3.5,1.38 nohead lw 0.5 lc rgb "#bbbbbb" front
set arrow 106 from -0.5,3.22 to 3.5,3.22 nohead lw 0.5 lc rgb "#bbbbbb" front
set arrow 107 from -0.5,3.68 to 3.5,3.68 nohead lw 0.5 lc rgb "#bbbbbb" front
set arrow 113 from -0.5,6.44 to 3.5,6.44 nohead lw 0.5 lc rgb "#bbbbbb" front
set object 6001 rect from -0.48,0.00 to 0.48,0.45 fc rgb "#d2e0ee" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 61000 "200" at 0,0.23 center font "Helvetica, 6" tc rgb "#333333" front
set object 6002 rect from 0.52,0.00 to 1.48,0.45 fc rgb "#cbdbeb" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 61001 "192" at 1,0.23 center font "Helvetica, 6" tc rgb "#333333" front
set object 6003 rect from 1.52,0.00 to 2.48,0.45 fc rgb "#d3e1ee" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 61002 "201" at 2,0.23 center font "Helvetica, 6" tc rgb "#333333" front
set object 6004 rect from 2.52,0.00 to 3.48,0.45 fc rgb "#d7e3f0" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 61003 "205" at 3,0.23 center font "Helvetica, 6" tc rgb "#333333" front
set object 6005 rect from -0.48,0.46 to 0.48,0.91 fc rgb "#bdd1e6" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 61004 "176" at 0,0.69 center font "Helvetica, 6" tc rgb "#333333" front
set object 6006 rect from 0.52,0.46 to 1.48,0.91 fc rgb "#ccdcec" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 61005 "193" at 1,0.69 center font "Helvetica, 6" tc rgb "#333333" front
set object 6007 rect from 1.52,0.46 to 2.48,0.91 fc rgb "#c8d9ea" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 61006 "189" at 2,0.69 center font "Helvetica, 6" tc rgb "#333333" front
set object 6008 rect from 2.52,0.46 to 3.48,0.91 fc rgb "#c4d6e9" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 61007 "184" at 3,0.69 center font "Helvetica, 6" tc rgb "#333333" front
set object 6009 rect from -0.48,0.92 to 0.48,1.37 fc rgb "#d0dfed" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 61008 "198" at 0,1.15 center font "Helvetica, 6" tc rgb "#333333" front
set object 6010 rect from 0.52,0.92 to 1.48,1.37 fc rgb "#ccdbeb" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 61009 "193" at 1,1.15 center font "Helvetica, 6" tc rgb "#333333" front
set object 6011 rect from 1.52,0.92 to 2.48,1.37 fc rgb "#d1dfed" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 61010 "198" at 2,1.15 center font "Helvetica, 6" tc rgb "#333333" front
set object 6012 rect from 2.52,0.92 to 3.48,1.37 fc rgb "#cbdbeb" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 61011 "192" at 3,1.15 center font "Helvetica, 6" tc rgb "#333333" front
set object 6013 rect from -0.48,1.38 to 0.48,1.83 fc rgb "#c5d7e9" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 61012 "186" at 0,1.61 center font "Helvetica, 6" tc rgb "#333333" front
set object 6014 rect from 0.52,1.38 to 1.48,1.83 fc rgb "#d0dfed" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 61013 "198" at 1,1.61 center font "Helvetica, 6" tc rgb "#333333" front
set object 6015 rect from 1.52,1.38 to 2.48,1.83 fc rgb "#c5d7e9" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 61014 "185" at 2,1.61 center font "Helvetica, 6" tc rgb "#333333" front
set object 6016 rect from 2.52,1.38 to 3.48,1.83 fc rgb "#cfdded" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 61015 "196" at 3,1.61 center font "Helvetica, 6" tc rgb "#333333" front
set object 6017 rect from -0.48,1.84 to 0.48,2.29 fc rgb "#ceddec" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 61016 "195" at 0,2.06 center font "Helvetica, 6" tc rgb "#333333" front
set object 6018 rect from 0.52,1.84 to 1.48,2.29 fc rgb "#cfdeed" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 61017 "197" at 1,2.06 center font "Helvetica, 6" tc rgb "#333333" front
set object 6019 rect from 1.52,1.84 to 2.48,2.29 fc rgb "#d3e1ee" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 61018 "202" at 2,2.06 center font "Helvetica, 6" tc rgb "#333333" front
set object 6020 rect from 2.52,1.84 to 3.48,2.29 fc rgb "#cddcec" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 61019 "194" at 3,2.06 center font "Helvetica, 6" tc rgb "#333333" front
set object 6021 rect from -0.48,2.30 to 0.48,2.75 fc rgb "#c8d9ea" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 61020 "189" at 0,2.53 center font "Helvetica, 6" tc rgb "#333333" front
set object 6022 rect from 0.52,2.30 to 1.48,2.75 fc rgb "#bfd3e7" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 61021 "179" at 1,2.53 center font "Helvetica, 6" tc rgb "#333333" front
set object 6023 rect from 1.52,2.30 to 2.48,2.75 fc rgb "#cddcec" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 61022 "194" at 2,2.53 center font "Helvetica, 6" tc rgb "#333333" front
set object 6024 rect from 2.52,2.30 to 3.48,2.75 fc rgb "#cadaeb" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 61023 "191" at 3,2.53 center font "Helvetica, 6" tc rgb "#333333" front
set object 6025 rect from -0.48,2.76 to 0.48,3.21 fc rgb "#b0c9e1" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 61024 "162" at 0,2.99 center font "Helvetica, 6" tc rgb "#333333" front
set object 6026 rect from 0.52,2.76 to 1.48,3.21 fc rgb "#c9d9ea" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 61025 "189" at 1,2.99 center font "Helvetica, 6" tc rgb "#333333" front
set object 6027 rect from 1.52,2.76 to 2.48,3.21 fc rgb "#ceddec" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 61026 "195" at 2,2.99 center font "Helvetica, 6" tc rgb "#333333" front
set object 6028 rect from 2.52,2.76 to 3.48,3.21 fc rgb "#dbe6f1" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 61027 "210" at 3,2.99 center font "Helvetica, 6" tc rgb "#333333" front
set object 6029 rect from -0.48,3.22 to 0.48,3.67 fc rgb "#d5e2ef" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 61028 "203" at 0,3.45 center font "Helvetica, 6" tc rgb "#333333" front
set object 6030 rect from 0.52,3.22 to 1.48,3.67 fc rgb "#d5e2ef" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 61029 "204" at 1,3.45 center font "Helvetica, 6" tc rgb "#333333" front
set object 6031 rect from 1.52,3.22 to 2.48,3.67 fc rgb "#d0dfed" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 61030 "198" at 2,3.45 center font "Helvetica, 6" tc rgb "#333333" front
set object 6032 rect from 2.52,3.22 to 3.48,3.67 fc rgb "#c4d6e9" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 61031 "184" at 3,3.45 center font "Helvetica, 6" tc rgb "#333333" front
set object 6033 rect from -0.48,3.68 to 0.48,4.13 fc rgb "#cddcec" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 61032 "194" at 0,3.91 center font "Helvetica, 6" tc rgb "#333333" front
set object 6034 rect from 0.52,3.68 to 1.48,4.13 fc rgb "#cddcec" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 61033 "194" at 1,3.91 center font "Helvetica, 6" tc rgb "#333333" front
set object 6035 rect from 1.52,3.68 to 2.48,4.13 fc rgb "#d4e1ef" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 61034 "202" at 2,3.91 center font "Helvetica, 6" tc rgb "#333333" front
set object 6036 rect from 2.52,3.68 to 3.48,4.13 fc rgb "#c6d7e9" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 61035 "186" at 3,3.91 center font "Helvetica, 6" tc rgb "#333333" front
set object 6037 rect from -0.48,4.14 to 0.48,4.59 fc rgb "#d0deed" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 61036 "197" at 0,4.37 center font "Helvetica, 6" tc rgb "#333333" front
set object 6038 rect from 0.52,4.14 to 1.48,4.59 fc rgb "#ccdcec" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 61037 "193" at 1,4.37 center font "Helvetica, 6" tc rgb "#333333" front
set object 6039 rect from 1.52,4.14 to 2.48,4.59 fc rgb "#d4e1ef" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 61038 "203" at 2,4.37 center font "Helvetica, 6" tc rgb "#333333" front
set object 6040 rect from 2.52,4.14 to 3.48,4.59 fc rgb "#c5d7e9" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 61039 "185" at 3,4.37 center font "Helvetica, 6" tc rgb "#333333" front
set object 6041 rect from -0.48,4.60 to 0.48,5.05 fc rgb "#d0dfed" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 61040 "198" at 0,4.83 center font "Helvetica, 6" tc rgb "#333333" front
set object 6042 rect from 0.52,4.60 to 1.48,5.05 fc rgb "#d1dfed" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 61041 "199" at 1,4.83 center font "Helvetica, 6" tc rgb "#333333" front
set object 6043 rect from 1.52,4.60 to 2.48,5.05 fc rgb "#cdddec" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 61042 "195" at 2,4.83 center font "Helvetica, 6" tc rgb "#333333" front
set object 6044 rect from 2.52,4.60 to 3.48,5.05 fc rgb "#b8cee4" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 61043 "171" at 3,4.83 center font "Helvetica, 6" tc rgb "#333333" front
set object 6045 rect from -0.48,5.06 to 0.48,5.51 fc rgb "#c5d7e9" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 61044 "185" at 0,5.29 center font "Helvetica, 6" tc rgb "#333333" front
set object 6046 rect from 0.52,5.06 to 1.48,5.51 fc rgb "#c6d8ea" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 61045 "187" at 1,5.29 center font "Helvetica, 6" tc rgb "#333333" front
set object 6047 rect from 1.52,5.06 to 2.48,5.51 fc rgb "#dae6f1" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 61046 "209" at 2,5.29 center font "Helvetica, 6" tc rgb "#333333" front
set object 6048 rect from 2.52,5.06 to 3.48,5.51 fc rgb "#d2e0ee" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 61047 "200" at 3,5.29 center font "Helvetica, 6" tc rgb "#333333" front
set object 6049 rect from -0.48,5.52 to 0.48,5.97 fc rgb "#cbdbeb" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 61048 "192" at 0,5.75 center font "Helvetica, 6" tc rgb "#333333" front
set object 6050 rect from 0.52,5.52 to 1.48,5.97 fc rgb "#cadaeb" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 61049 "191" at 1,5.75 center font "Helvetica, 6" tc rgb "#333333" front
set object 6051 rect from 1.52,5.52 to 2.48,5.97 fc rgb "#d2e0ee" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 61050 "200" at 2,5.75 center font "Helvetica, 6" tc rgb "#333333" front
set object 6052 rect from 2.52,5.52 to 3.48,5.97 fc rgb "#c9daeb" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 61051 "190" at 3,5.75 center font "Helvetica, 6" tc rgb "#333333" front
set object 6053 rect from -0.48,5.98 to 0.48,6.43 fc rgb "#ceddec" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 61052 "195" at 0,6.21 center font "Helvetica, 6" tc rgb "#333333" front
set object 6054 rect from 0.52,5.98 to 1.48,6.43 fc rgb "#cddcec" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 61053 "194" at 1,6.21 center font "Helvetica, 6" tc rgb "#333333" front
set object 6055 rect from 1.52,5.98 to 2.48,6.43 fc rgb "#c9daeb" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 61054 "190" at 2,6.21 center font "Helvetica, 6" tc rgb "#333333" front
set object 6056 rect from 2.52,5.98 to 3.48,6.43 fc rgb "#c7d8ea" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 61055 "188" at 3,6.21 center font "Helvetica, 6" tc rgb "#333333" front
set object 6057 rect from -0.48,6.44 to 0.48,6.89 fc rgb "#c6d8ea" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 61056 "187" at 0,6.67 center font "Helvetica, 6" tc rgb "#333333" front
set object 6058 rect from 0.52,6.44 to 1.48,6.89 fc rgb "#c7d8ea" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 61057 "187" at 1,6.67 center font "Helvetica, 6" tc rgb "#333333" front
set object 6059 rect from 1.52,6.44 to 2.48,6.89 fc rgb "#d7e3f0" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 61058 "205" at 2,6.67 center font "Helvetica, 6" tc rgb "#333333" front
set object 6060 rect from 2.52,6.44 to 3.48,6.89 fc rgb "#c7d8ea" fs solid 1.0 border lc rgb "#e0e0e0" lw 0.15 behind
set label 61059 "187" at 3,6.67 center font "Helvetica, 6" tc rgb "#333333" front
set colorbox user origin 0.955,0.08 size 0.012,0.80
set palette defined (0 "#2166ac", 125 "#67a9cf", 250 "#ffffff", 375 "#ef8a62", 500 "#b2182b")
set cbrange [0:500]
set cbtics 0,100,500 font "Helvetica, 7"
set cblabel "Median gap (ms)" font "Helvetica, 8" offset 1,0
set lmargin at screen 0.820
set rmargin at screen 0.939
set bmargin at screen 0.08
set tmargin at screen 0.88
plot NaN notitle

unset multiplot