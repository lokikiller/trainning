#!/usr/bin/env python
# -*- encoding=utf8 -*-

'''
FileName:   test
Author:     Hao Tingyi
@contact:   lokikiller@126.com
@version:   $

Description:

Changelog:

'''

from data.collector import DataCollection
import json

data = DataCollection('memory').catch()
print json.dumps(data)