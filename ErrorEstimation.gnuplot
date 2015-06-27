# print a chart with estimation errors for each iteration

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

# plot and skip some data (TODO why I added 12 here?) 
plot "error.log" every ::12
