load 'style.gnu'
set terminal postscript enhanced color eps font "Helvetica, 14"
set size 0.75, 0.7
set output '../figures/heatmap_country_server.eps'

set xrange [-0.5:3.5]
set yrange [-0.5:14.5]
set xlabel "{/Helvetica-Bold Honeypot Server}" offset 0,0.3
set xtics ("Virginia" 0, "Tokyo" 1, "Paris" 2, "S. Paulo" 3) font "Helvetica, 12" offset 0,0.2

set ytics ("United States" 0, "Canada" 1, "Mexico" 2, "United Kingdom" 3, "Germany" 4, "France" 5, "Russia" 6, "Brazil" 7, "Japan" 8, "Singapore" 9, "Indonesia" 10, "South Korea" 11, "India" 12, "Australia" 13, "South Africa" 14) font "Helvetica, 11"

set label "{/Helvetica-Bold N. Am.}" at -2.0,1.0 center font "Helvetica-Bold, 9" tc rgb "#333333"
set label "{/Helvetica-Bold Europe}" at -2.0,4.5 center font "Helvetica-Bold, 9" tc rgb "#333333"
set label "{/Helvetica-Bold S. Am.}" at -2.0,7.0 center font "Helvetica-Bold, 9" tc rgb "#333333"
set label "{/Helvetica-Bold Asia}" at -2.0,10.0 center font "Helvetica-Bold, 9" tc rgb "#333333"
set label "{/Helvetica-Bold OC}" at -2.0,13.0 center font "Helvetica-Bold, 9" tc rgb "#333333"
set label "{/Helvetica-Bold AF}" at -2.0,14.0 center font "Helvetica-Bold, 9" tc rgb "#333333"
set arrow from -0.5,2.5 to 3.5,2.5 nohead lw 1.2 lc rgb "#666666" front
set arrow from -0.5,6.5 to 3.5,6.5 nohead lw 1.2 lc rgb "#666666" front
set arrow from -0.5,7.5 to 3.5,7.5 nohead lw 1.2 lc rgb "#666666" front
set arrow from -0.5,12.5 to 3.5,12.5 nohead lw 1.2 lc rgb "#666666" front
set arrow from -0.5,13.5 to 3.5,13.5 nohead lw 1.2 lc rgb "#666666" front

set lmargin 13
set bmargin 3
set tmargin 1
set rmargin 5
unset key
unset grid
unset colorbox

set object 1 rect from -0.48,-0.45 to 0.48,0.45 fc rgb "#4b83bb" fillstyle solid 1.0 border lc rgb "#cccccc" lw 0.3 behind
set label 100 "109" at 0,0 center font "Helvetica, 10" tc rgb "#333333" front
set object 2 rect from 0.52,-0.45 to 1.48,0.45 fc rgb "#4b83bb" fillstyle solid 1.0 border lc rgb "#cccccc" lw 0.3 behind
set label 101 "109" at 1,0 center font "Helvetica, 10" tc rgb "#333333" front
set object 3 rect from 1.52,-0.45 to 2.48,0.45 fc rgb "#4b83bc" fillstyle solid 1.0 border lc rgb "#cccccc" lw 0.3 behind
set label 102 "109" at 2,0 center font "Helvetica, 10" tc rgb "#333333" front
set object 4 rect from 2.52,-0.45 to 3.48,0.45 fc rgb "#457fb9" fillstyle solid 1.0 border lc rgb "#cccccc" lw 0.3 behind
set label 103 "105" at 3,0 center font "Helvetica, 10" tc rgb "#333333" front
set object 5 rect from -0.48,0.55 to 0.48,1.45 fc rgb "#6e9bc9" fillstyle solid 1.0 border lc rgb "#cccccc" lw 0.3 behind
set label 104 "133" at 0,1 center font "Helvetica, 10" tc rgb "#333333" front
set object 6 rect from 0.52,0.55 to 1.48,1.45 fc rgb "#6f9bc9" fillstyle solid 1.0 border lc rgb "#cccccc" lw 0.3 behind
set label 105 "133" at 1,1 center font "Helvetica, 10" tc rgb "#333333" front
set object 7 rect from 1.52,0.55 to 2.48,1.45 fc rgb "#6e9bc8" fillstyle solid 1.0 border lc rgb "#cccccc" lw 0.3 behind
set label 106 "132" at 2,1 center font "Helvetica, 10" tc rgb "#333333" front
set object 8 rect from 2.52,0.55 to 3.48,1.45 fc rgb "#6f9cc9" fillstyle solid 1.0 border lc rgb "#cccccc" lw 0.3 behind
set label 107 "133" at 3,1 center font "Helvetica, 10" tc rgb "#333333" front
set object 9 rect from -0.48,1.55 to 0.48,2.45 fc rgb "#7ba4cd" fillstyle solid 1.0 border lc rgb "#cccccc" lw 0.3 behind
set label 108 "141" at 0,2 center font "Helvetica, 10" tc rgb "#333333" front
set object 10 rect from 0.52,1.55 to 1.48,2.45 fc rgb "#78a2cc" fillstyle solid 1.0 border lc rgb "#cccccc" lw 0.3 behind
set label 109 "139" at 1,2 center font "Helvetica, 10" tc rgb "#333333" front
set object 11 rect from 1.52,1.55 to 2.48,2.45 fc rgb "#77a1cc" fillstyle solid 1.0 border lc rgb "#cccccc" lw 0.3 behind
set label 110 "139" at 2,2 center font "Helvetica, 10" tc rgb "#333333" front
set object 12 rect from 2.52,1.55 to 3.48,2.45 fc rgb "#7aa3cd" fillstyle solid 1.0 border lc rgb "#cccccc" lw 0.3 behind
set label 111 "141" at 3,2 center font "Helvetica, 10" tc rgb "#333333" front
set object 13 rect from -0.48,2.55 to 0.48,3.45 fc rgb "#7aa3cd" fillstyle solid 1.0 border lc rgb "#cccccc" lw 0.3 behind
set label 112 "141" at 0,3 center font "Helvetica, 10" tc rgb "#333333" front
set object 14 rect from 0.52,2.55 to 1.48,3.45 fc rgb "#78a2cc" fillstyle solid 1.0 border lc rgb "#cccccc" lw 0.3 behind
set label 113 "139" at 1,3 center font "Helvetica, 10" tc rgb "#333333" front
set object 15 rect from 1.52,2.55 to 2.48,3.45 fc rgb "#7aa3cd" fillstyle solid 1.0 border lc rgb "#cccccc" lw 0.3 behind
set label 114 "140" at 2,3 center font "Helvetica, 10" tc rgb "#333333" front
set object 16 rect from 2.52,2.55 to 3.48,3.45 fc rgb "#749fcb" fillstyle solid 1.0 border lc rgb "#cccccc" lw 0.3 behind
set label 115 "137" at 3,3 center font "Helvetica, 10" tc rgb "#333333" front
set object 17 rect from -0.48,3.55 to 0.48,4.45 fc rgb "#76a0cb" fillstyle solid 1.0 border lc rgb "#cccccc" lw 0.3 behind
set label 116 "138" at 0,4 center font "Helvetica, 10" tc rgb "#333333" front
set object 18 rect from 0.52,3.55 to 1.48,4.45 fc rgb "#8db1d4" fillstyle solid 1.0 border lc rgb "#cccccc" lw 0.3 behind
set label 117 "154" at 1,4 center font "Helvetica, 10" tc rgb "#333333" front
set object 19 rect from 1.52,3.55 to 2.48,4.45 fc rgb "#8bafd3" fillstyle solid 1.0 border lc rgb "#cccccc" lw 0.3 behind
set label 118 "152" at 2,4 center font "Helvetica, 10" tc rgb "#333333" front
set object 20 rect from 2.52,3.55 to 3.48,4.45 fc rgb "#80a7cf" fillstyle solid 1.0 border lc rgb "#cccccc" lw 0.3 behind
set label 119 "145" at 3,4 center font "Helvetica, 10" tc rgb "#333333" front
set object 21 rect from -0.48,4.55 to 0.48,5.45 fc rgb "#ceddec" fillstyle solid 1.0 border lc rgb "#cccccc" lw 0.3 behind
set label 120 "197" at 0,5 center font "Helvetica, 10" tc rgb "#333333" front
set object 22 rect from 0.52,4.55 to 1.48,5.45 fc rgb "#dae5f1" fillstyle solid 1.0 border lc rgb "#cccccc" lw 0.3 behind
set label 121 "205" at 1,5 center font "Helvetica, 10" tc rgb "#333333" front
set object 23 rect from 1.52,4.55 to 2.48,5.45 fc rgb "#d8e4f0" fillstyle solid 1.0 border lc rgb "#cccccc" lw 0.3 behind
set label 122 "204" at 2,5 center font "Helvetica, 10" tc rgb "#333333" front
set object 24 rect from 2.52,4.55 to 3.48,5.45 fc rgb "#abc5df" fillstyle solid 1.0 border lc rgb "#cccccc" lw 0.3 behind
set label 123 "174" at 3,5 center font "Helvetica, 10" tc rgb "#333333" front
set object 25 rect from -0.48,5.55 to 0.48,6.45 fc rgb "#edb3b5" fillstyle solid 1.0 border lc rgb "#cccccc" lw 0.3 behind
set label 124 "279" at 0,6 center font "Helvetica, 10" tc rgb "#ffffff" front
set object 26 rect from 0.52,5.55 to 1.48,6.45 fc rgb "#a8c3de" fillstyle solid 1.0 border lc rgb "#cccccc" lw 0.3 behind
set label 125 "171" at 1,6 center font "Helvetica, 10" tc rgb "#333333" front
set object 27 rect from 1.52,5.55 to 2.48,6.45 fc rgb "#fcfdfe" fillstyle solid 1.0 border lc rgb "#cccccc" lw 0.3 behind
set label 126 "228" at 2,6 center font "Helvetica, 10" tc rgb "#333333" front
set object 28 rect from 2.52,5.55 to 3.48,6.45 fc rgb "#f9e5e5" fillstyle solid 1.0 border lc rgb "#cccccc" lw 0.3 behind
set label 127 "247" at 3,6 center font "Helvetica, 10" tc rgb "#333333" front
set object 29 rect from -0.48,6.55 to 0.48,7.45 fc rgb "#e2ebf4" fillstyle solid 1.0 border lc rgb "#cccccc" lw 0.3 behind
set label 128 "211" at 0,7 center font "Helvetica, 10" tc rgb "#333333" front
set object 30 rect from 0.52,6.55 to 1.48,7.45 fc rgb "#d3e0ee" fillstyle solid 1.0 border lc rgb "#cccccc" lw 0.3 behind
set label 129 "200" at 1,7 center font "Helvetica, 10" tc rgb "#333333" front
set object 31 rect from 1.52,6.55 to 2.48,7.45 fc rgb "#cddcec" fillstyle solid 1.0 border lc rgb "#cccccc" lw 0.3 behind
set label 130 "197" at 2,7 center font "Helvetica, 10" tc rgb "#333333" front
set object 32 rect from 2.52,6.55 to 3.48,7.45 fc rgb "#e1eaf4" fillstyle solid 1.0 border lc rgb "#cccccc" lw 0.3 behind
set label 131 "210" at 3,7 center font "Helvetica, 10" tc rgb "#333333" front
set object 33 rect from -0.48,7.55 to 0.48,8.45 fc rgb "#f9e5e6" fillstyle solid 1.0 border lc rgb "#cccccc" lw 0.3 behind
set label 132 "247" at 0,8 center font "Helvetica, 10" tc rgb "#333333" front
set object 34 rect from 0.52,7.55 to 1.48,8.45 fc rgb "#f3cccd" fillstyle solid 1.0 border lc rgb "#cccccc" lw 0.3 behind
set label 133 "263" at 1,8 center font "Helvetica, 10" tc rgb "#333333" front
set object 35 rect from 1.52,7.55 to 2.48,8.45 fc rgb "#f2c7c8" fillstyle solid 1.0 border lc rgb "#cccccc" lw 0.3 behind
set label 134 "266" at 2,8 center font "Helvetica, 10" tc rgb "#333333" front
set object 36 rect from 2.52,7.55 to 3.48,8.45 fc rgb "#eeb4b6" fillstyle solid 1.0 border lc rgb "#cccccc" lw 0.3 behind
set label 135 "278" at 3,8 center font "Helvetica, 10" tc rgb "#ffffff" front
set object 37 rect from -0.48,8.55 to 0.48,9.45 fc rgb "#f4d1d2" fillstyle solid 1.0 border lc rgb "#cccccc" lw 0.3 behind
set label 136 "260" at 0,9 center font "Helvetica, 10" tc rgb "#333333" front
set object 38 rect from 0.52,8.55 to 1.48,9.45 fc rgb "#e4878a" fillstyle solid 1.0 border lc rgb "#cccccc" lw 0.3 behind
set label 137 "307" at 1,9 center font "Helvetica, 10" tc rgb "#ffffff" front
set object 39 rect from 1.52,8.55 to 2.48,9.45 fc rgb "#f0bfc1" fillstyle solid 1.0 border lc rgb "#cccccc" lw 0.3 behind
set label 138 "271" at 2,9 center font "Helvetica, 10" tc rgb "#ffffff" front
set object 40 rect from 2.52,8.55 to 3.48,9.45 fc rgb "#f4d0d1" fillstyle solid 1.0 border lc rgb "#cccccc" lw 0.3 behind
set label 139 "260" at 3,9 center font "Helvetica, 10" tc rgb "#333333" front
set object 41 rect from -0.48,9.55 to 0.48,10.45 fc rgb "#eeb7b9" fillstyle solid 1.0 border lc rgb "#cccccc" lw 0.3 behind
set label 140 "276" at 0,10 center font "Helvetica, 10" tc rgb "#ffffff" front
set object 42 rect from 0.52,9.55 to 1.48,10.45 fc rgb "#efb9bb" fillstyle solid 1.0 border lc rgb "#cccccc" lw 0.3 behind
set label 141 "275" at 1,10 center font "Helvetica, 10" tc rgb "#ffffff" front
set object 43 rect from 1.52,9.55 to 2.48,10.45 fc rgb "#edb3b5" fillstyle solid 1.0 border lc rgb "#cccccc" lw 0.3 behind
set label 142 "279" at 2,10 center font "Helvetica, 10" tc rgb "#ffffff" front
set object 44 rect from 2.52,9.55 to 3.48,10.45 fc rgb "#eeb6b8" fillstyle solid 1.0 border lc rgb "#cccccc" lw 0.3 behind
set label 143 "277" at 3,10 center font "Helvetica, 10" tc rgb "#ffffff" front
set object 45 rect from -0.48,10.55 to 0.48,11.45 fc rgb "#eeb7b8" fillstyle solid 1.0 border lc rgb "#cccccc" lw 0.3 behind
set label 144 "277" at 0,11 center font "Helvetica, 10" tc rgb "#ffffff" front
set object 46 rect from 0.52,10.55 to 1.48,11.45 fc rgb "#e0777a" fillstyle solid 1.0 border lc rgb "#cccccc" lw 0.3 behind
set label 145 "318" at 1,11 center font "Helvetica, 10" tc rgb "#ffffff" front
set object 47 rect from 1.52,10.55 to 2.48,11.45 fc rgb "#eaa4a6" fillstyle solid 1.0 border lc rgb "#cccccc" lw 0.3 behind
set label 146 "289" at 2,11 center font "Helvetica, 10" tc rgb "#ffffff" front
set object 48 rect from 2.52,10.55 to 3.48,11.45 fc rgb "#de6e71" fillstyle solid 1.0 border lc rgb "#cccccc" lw 0.3 behind
set label 147 "324" at 3,11 center font "Helvetica, 10" tc rgb "#ffffff" front
set object 49 rect from -0.48,11.55 to 0.48,12.45 fc rgb "#de6d70" fillstyle solid 1.0 border lc rgb "#cccccc" lw 0.3 behind
set label 148 "325" at 0,12 center font "Helvetica, 10" tc rgb "#ffffff" front
set object 50 rect from 0.52,11.55 to 1.48,12.45 fc rgb "#e17a7d" fillstyle solid 1.0 border lc rgb "#cccccc" lw 0.3 behind
set label 149 "316" at 1,12 center font "Helvetica, 10" tc rgb "#ffffff" front
set object 51 rect from 1.52,11.55 to 2.48,12.45 fc rgb "#e4898c" fillstyle solid 1.0 border lc rgb "#cccccc" lw 0.3 behind
set label 150 "306" at 2,12 center font "Helvetica, 10" tc rgb "#ffffff" front
set object 52 rect from 2.52,11.55 to 3.48,12.45 fc rgb "#e1797c" fillstyle solid 1.0 border lc rgb "#cccccc" lw 0.3 behind
set label 151 "317" at 3,12 center font "Helvetica, 10" tc rgb "#ffffff" front
set object 53 rect from -0.48,12.55 to 0.48,13.45 fc rgb "#ebaaac" fillstyle solid 1.0 border lc rgb "#cccccc" lw 0.3 behind
set label 152 "285" at 0,13 center font "Helvetica, 10" tc rgb "#ffffff" front
set object 54 rect from 0.52,12.55 to 1.48,13.45 fc rgb "#eeb6b8" fillstyle solid 1.0 border lc rgb "#cccccc" lw 0.3 behind
set label 153 "277" at 1,13 center font "Helvetica, 10" tc rgb "#ffffff" front
set object 55 rect from 1.52,12.55 to 2.48,13.45 fc rgb "#f0bcbe" fillstyle solid 1.0 border lc rgb "#cccccc" lw 0.3 behind
set label 154 "273" at 2,13 center font "Helvetica, 10" tc rgb "#ffffff" front
set object 56 rect from 2.52,12.55 to 3.48,13.45 fc rgb "#f0c0c1" fillstyle solid 1.0 border lc rgb "#cccccc" lw 0.3 behind
set label 155 "271" at 3,13 center font "Helvetica, 10" tc rgb "#ffffff" front
set object 57 rect from -0.48,13.55 to 0.48,14.45 fc rgb "#da5d60" fillstyle solid 1.0 border lc rgb "#cccccc" lw 0.3 behind
set label 156 "335" at 0,14 center font "Helvetica, 10" tc rgb "#ffffff" front
set object 58 rect from 0.52,13.55 to 1.48,14.45 fc rgb "#e0777a" fillstyle solid 1.0 border lc rgb "#cccccc" lw 0.3 behind
set label 157 "318" at 1,14 center font "Helvetica, 10" tc rgb "#ffffff" front
set object 59 rect from 1.52,13.55 to 2.48,14.45 fc rgb "#dc6568" fillstyle solid 1.0 border lc rgb "#cccccc" lw 0.3 behind
set label 158 "330" at 2,14 center font "Helvetica, 10" tc rgb "#ffffff" front
set object 60 rect from 2.52,13.55 to 3.48,14.45 fc rgb "#d85558" fillstyle solid 1.0 border lc rgb "#cccccc" lw 0.3 behind
set label 159 "340" at 3,14 center font "Helvetica, 10" tc rgb "#ffffff" front

# Colorbar
set object 61 rect from 3.7,-0.50 to 4.1,0.00 fc rgb "#2166ac" fillstyle solid 1.0 noborder behind
set object 62 rect from 3.7,0.00 to 4.1,0.50 fc rgb "#2f70b1" fillstyle solid 1.0 noborder behind
set object 63 rect from 3.7,0.50 to 4.1,1.00 fc rgb "#3e7ab7" fillstyle solid 1.0 noborder behind
set object 64 rect from 3.7,1.00 to 4.1,1.50 fc rgb "#4d84bc" fillstyle solid 1.0 noborder behind
set object 65 rect from 3.7,1.50 to 4.1,2.00 fc rgb "#5c8ec2" fillstyle solid 1.0 noborder behind
set object 66 rect from 3.7,2.00 to 4.1,2.50 fc rgb "#6b99c7" fillstyle solid 1.0 noborder behind
set object 67 rect from 3.7,2.50 to 4.1,3.00 fc rgb "#79a3cd" fillstyle solid 1.0 noborder behind
set object 68 rect from 3.7,3.00 to 4.1,3.50 fc rgb "#88add2" fillstyle solid 1.0 noborder behind
set object 69 rect from 3.7,3.50 to 4.1,4.00 fc rgb "#97b7d8" fillstyle solid 1.0 noborder behind
set object 70 rect from 3.7,4.00 to 4.1,4.50 fc rgb "#a6c1dd" fillstyle solid 1.0 noborder behind
set object 71 rect from 3.7,4.50 to 4.1,5.00 fc rgb "#b5cce3" fillstyle solid 1.0 noborder behind
set object 72 rect from 3.7,5.00 to 4.1,5.50 fc rgb "#c3d6e8" fillstyle solid 1.0 noborder behind
set object 73 rect from 3.7,5.50 to 4.1,6.00 fc rgb "#d2e0ee" fillstyle solid 1.0 noborder behind
set object 74 rect from 3.7,6.00 to 4.1,6.50 fc rgb "#e1eaf3" fillstyle solid 1.0 noborder behind
set object 75 rect from 3.7,6.50 to 4.1,7.00 fc rgb "#f0f4f9" fillstyle solid 1.0 noborder behind
set object 76 rect from 3.7,7.00 to 4.1,7.50 fc rgb "#ffffff" fillstyle solid 1.0 noborder behind
set object 77 rect from 3.7,7.50 to 4.1,8.00 fc rgb "#fbefef" fillstyle solid 1.0 noborder behind
set object 78 rect from 3.7,8.00 to 4.1,8.50 fc rgb "#f8e0e0" fillstyle solid 1.0 noborder behind
set object 79 rect from 3.7,8.50 to 4.1,9.00 fc rgb "#f4d0d1" fillstyle solid 1.0 noborder behind
set object 80 rect from 3.7,9.00 to 4.1,9.50 fc rgb "#f1c1c2" fillstyle solid 1.0 noborder behind
set object 81 rect from 3.7,9.50 to 4.1,10.00 fc rgb "#edb2b3" fillstyle solid 1.0 noborder behind
set object 82 rect from 3.7,10.00 to 4.1,10.50 fc rgb "#eaa2a4" fillstyle solid 1.0 noborder behind
set object 83 rect from 3.7,10.50 to 4.1,11.00 fc rgb "#e69395" fillstyle solid 1.0 noborder behind
set object 84 rect from 3.7,11.00 to 4.1,11.50 fc rgb "#e38386" fillstyle solid 1.0 noborder behind
set object 85 rect from 3.7,11.50 to 4.1,12.00 fc rgb "#df7477" fillstyle solid 1.0 noborder behind
set object 86 rect from 3.7,12.00 to 4.1,12.50 fc rgb "#dc6468" fillstyle solid 1.0 noborder behind
set object 87 rect from 3.7,12.50 to 4.1,13.00 fc rgb "#d85559" fillstyle solid 1.0 noborder behind
set object 88 rect from 3.7,13.00 to 4.1,13.50 fc rgb "#d5464a" fillstyle solid 1.0 noborder behind
set object 89 rect from 3.7,13.50 to 4.1,14.00 fc rgb "#d1363b" fillstyle solid 1.0 noborder behind
set object 90 rect from 3.7,14.00 to 4.1,14.50 fc rgb "#ce272c" fillstyle solid 1.0 noborder behind
set label 160 "100" at 4.25,0.50 left font "Helvetica, 10" tc rgb "#333333"
set label 161 "150" at 4.25,3.00 left font "Helvetica, 10" tc rgb "#333333"
set label 162 "200" at 4.25,5.50 left font "Helvetica, 10" tc rgb "#333333"
set label 163 "250" at 4.25,8.00 left font "Helvetica, 10" tc rgb "#333333"
set label 164 "300" at 4.25,10.50 left font "Helvetica, 10" tc rgb "#333333"
set label 165 "350" at 4.25,13.00 left font "Helvetica, 10" tc rgb "#333333"
set label 166 "{/Helvetica-Bold ms}" at 4.25,15.3 left font "Helvetica-Bold, 9" tc rgb "#333333"

plot NaN notitle
