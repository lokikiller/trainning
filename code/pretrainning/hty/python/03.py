#!/usr/bin/env python

'03.py --- string template'

from string import Template

s = Template('There are ${howmany} ${lang} Quotation Symbols.')

print s.substitute(howmany=3, lang='python')

print s.safe_substitute(lang='python')

str = "kila"

print str.capitalize()
print str.center(40)
print str.count('ki')
print str.endswith('a')
print str.find('k')
print str.index('i')
print ':'.join(['a', 'b', 'c'])

