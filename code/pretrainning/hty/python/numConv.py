#!/usr/bin/env python

def convert(func, seq):
    'conv. sequence of numbers to same type'
    return [func(eachNum) for eachNum in seq]


myseq = (123, 45.67, -6.2e8, 9999999L)
print convert(int, myseq)
print convert(float, myseq)
print convert(long, myseq)
