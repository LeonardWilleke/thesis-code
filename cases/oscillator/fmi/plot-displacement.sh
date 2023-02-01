#!/bin/sh

if [ "${1:-}" = "" ]; then
    echo "No target directory specified. Please specify the directory watchpoint log, e.g. ./plot-displacement.sh .."
    exit 1
fi

FILE="$1/precice-Mass-Left-watchpoint-displacement.log"

if [ ! -f "$FILE" ]; then
    echo "Unable to locate the watchpoint file (precice-Mass-Left-watchpoint-displacement.log) in the specified directory '${1}'. Make sure the specified directory matches the participant you used for the calculations."
    exit 1
fi
 
gnuplot -p << EOF                                                               
	set grid                                                                        
	set title 'x-displacement of the left mass'                                        
	set xlabel 'time [s]'                                                           
	set ylabel 'x-displacement [m]'                                                 
	plot "$1/precice-Mass-Left-watchpoint-displacement.log" using 1:4 with lines title "$1"
EOF
