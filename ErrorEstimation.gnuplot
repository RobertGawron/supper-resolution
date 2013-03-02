# a script for printing a chart with changes of the error estimation in each iteration

# usage:
#
# in SRRestorer.py replace:
#        print '%2d: estimation error: %3f' % (i, error)
# to:
#        print error
# 
# bash-3.2$ python SRRestorer.py input > error.log
# bash-3.2$ gnuplot ErrorEstimation.gnuplot 

# output:
# estimation_error.png in the directory where the script is

set terminal png
set output "estimation_error.png"

set title "Estimation error"
set xlabel "iteration"
set ylabel "error"
unset key 

# it's 12, because the script prints also other things, we need to skip them 
plot "error.log" every ::12
