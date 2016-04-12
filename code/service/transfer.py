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
import sys

sys.path.append('..')
from utils.mongo_util import DB


class Transfer(object):
    def __init__(self):
        self.db = DB().conn()

    def get_data(self, uuid, collection):
        res = []
        for item in self.db[collection].find({'name': uuid}).sort('time'):
            del item['_id']
            res.append(item)
        return res

    def collection_exist(self, collection):
        if collection in self.db.collection_names():
            return True
        else:
            return False

    def uuid_count(self, uuid, collection):
        if self.db[collection].find({'name': uuid}).count() != 0:
            return True
        else:
            return False

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
