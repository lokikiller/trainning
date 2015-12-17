#!/usr/bin/env python
# -*- encoding=utf8 -*-

'''
FileName:   transmission
Author:     Hao Tingyi
@contact:   lokikiller@126.com
@version:   $

Description:

Changelog:

'''
import os
from pymongo import MongoClient


class DB(object):
    def __init__(self):
        host = os.environ.get('MONGO_HOST')
        if not host:
            host = 'localhost'

        port = os.environ.get('MONGO_PORT')
        if not port:
            port = '27017'

        self.client = MongoClient('mongodb://' + host + ':' + port + '/')

    def conn(self):
        return self.client['performance']


class Transfer(object):
    def __init__(self):
        self.db = DB().conn()

    def get_data(self, collection):
        res = []
        for item in self.db[collection].find():
            del item['_id']
            res.append(item)
        return res
