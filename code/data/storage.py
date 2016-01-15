#!/usr/bin/env python
# -*- encoding=utf8 -*-

'''
FileName:   storage
Author:     Hao Tingyi
@contact:   lokikiller@126.com
@version:   $

Description:

Changelog:

'''

import os
from pymongo import MongoClient


class Storage(object):
    def __init__(self):
        self.host = os.environ.get('MONGO_HOST')
        if not self.host:
            self.host = 'localhost'

        self.port = os.environ.get('MONGO_PORT')
        if not self.port:
            self.port = '27017'

    def conn(self):
        return MongoClient('mongodb://' + self.host + ':' + self.port + '/')[
            'performance']
