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

    def get_data(self, uuid, collection):
        res = []
        for item in self.db[collection].find({'name': uuid}).sort('time'):
            del item['_id']
            res.append(item)
        return res

    def get_hosts(self):
        res = []
        hosts = self.db['one_min_load'].distinct('name')
        for host in hosts:
            attributes = dict()
            attributes['hostIP'] = host

            cpu_data = self.db['one_min_cpu'].find({'name': host}).sort(
                'time').limit(1).next()['data']
            cpu_sum = 0.0
            for val in cpu_data.values():
                cpu_sum += val
            cpu_sum -= cpu_data['idle']
            attributes['hostCPU'] = cpu_sum

            attributes['hostLoad'] = self.db['one_min_load'].find(
                {'name': host}).sort('time').limit(1).next()['data']['w1_avg']

            memory_data = self.db['one_min_memory'].find({'name': host}).limit(
                1).next()['data']
            memory_usage = float(memory_data['abs_used']) / float(
                memory_data['total'])
            attributes['hostMemory'] = memory_usage

            res.append(attributes)
        return res