#!/usr/bin/env python

'02.py -- test int() floor() round()'

import math

for num in (.2, .7, 1.2, 1.7, -.2, -.7, -1.2, -1.7):
    print "int(%.1f)\t%+.1f" % (num, float(int(num)))
    print "floor(%.1f)\t%+.1f" % (num, math.floor(num))
    print "round(%.1f)\t%+.1f" % (num, round(num))
    print "-" * 20
