#!/usr/bin/env python

from matplotlib.pyplot import *
from scipy import *

plot(genfromtxt(sys.argv[1], delimiter = ",", skip_header = 1))
show()
