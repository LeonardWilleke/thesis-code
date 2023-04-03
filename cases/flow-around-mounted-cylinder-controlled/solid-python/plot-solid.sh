#!/bin/sh

if [ "${1:-}" = "" ]; then
    echo "No target directory specified. Please specify the directory of the participant solid containing the watchpoint, e.g. ./plot-displacement.sh solid-python."
    exit 1
fi

FILE="$1/precice-Solid-watchpoint-Spring.log"

if [ ! -f "$FILE" ]; then
	echo "Unable to locate the watchpoint file (*.log) in the specified directory '${1}'. Make sure the specified directory matches the fluid or solid participant you used for the calculations."
	exit 1
fi
 
gnuplot -p <<EOF                                                         
	set grid                                                                        
	set title 'Displacement spring'                                        
	set xlabel 'time [s]'                                                           
	set ylabel 'delta y [m]'                                                 
	plot "$1/precice-Solid-watchpoint-Spring.log" using 1:5 with lines title "$1"
EOF

gnuplot -p <<EOF                                             
	set grid                                                                        
	set title 'Displacement cylinder'                                        
	set xlabel 'time [s]'                                                           
	set ylabel 'delta y [m]'                                                 
	plot "$1/precice-Solid-watchpoint-Spring.log" using 1:7 with lines title "$1"
EOF

gnuplot -p <<EOF                                                             
	set grid                                                                        
	set title 'Force from Spring acting on cylinder'                                        
	set xlabel 'time [s]'                                                           
	set ylabel 'force y [N]'                                                 
	plot "$1/precice-Solid-watchpoint-Spring.log" using 1:9 with lines title "$1"
EOF
