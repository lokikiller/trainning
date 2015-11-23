#!/usr/bin/env python

'''
mdict.py --- using dict func
'''

dict1 = {'name': 'earth', 'port': 80}

for eachKey in sorted(dict1):
    print 'dict key', eachKey, 'has value', dict1[eachKey]

dict2 = {'name': 'hty', 'port': 80, 'server': 'http'}
dict1.update(dict2)

print dict1

dict2.clear()
print dict2

dict3 = dict1.copy()
print dict3

print dict3.get('name')
print dict3.get('who')
print dict3.get('who', 'server')

print dict1.keys()
print dict1.items()
print dict1.values()

{}.fromkeys(('honey', 'lover'), 1)
