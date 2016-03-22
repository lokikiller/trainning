#!/usr/bin/env python
# -*- encoding=utf8 -*-

'''
FileName:   filter
Author:     Hao Tingyi
@contact:   lokikiller@126.com
@version:   $

Description:

Changelog:

'''

import logging
import logging.config
from collector import DataCollection

logging.config.fileConfig('conf/log.conf')
root_logger = logging.getLogger('root')


class Filter(object):
    def __init__(self):
        # init key for dict
        self.load_params = ["w1_avg", "w5_avg", "w15_avg"]
        self.cpu_params = ["user", "nice", "system", "idle", "iowait",
                           "irq", "softirq", "steal", "guest", "guest_nice"]
        self.mem_params = ["total", "used", "abs_used", "free", "buffers",
                           "cached", "active", "inactive", "swap_used"]

        # init data handler
        self.handler = DataHandler()

    # get data(type dict) from collector and extract value from dict
    def pre_producer(self, lists):
        data_set = self.handler.catch_data()
        for index, datas in enumerate(data_set):
            self.handler.push_data(datas, lists[index])
        return lists

    # pack data(type list) to dict(add key)
    def end_producer(self, lists, collection):
        params_list = [self.load_params, self.cpu_params, self.mem_params]
        res = []
        for index, items in enumerate(lists):
            res.append(self.handler.get_data(items, params_list[index]))
        return (res, collection)

    # init data manage queue
    def new_list(self):
        load_list = [0 for i in range(len(self.load_params))]
        cpu_list = [0 for i in range(len(self.cpu_params))]
        mem_list = [0 for i in range(len(self.mem_params))]
        return [load_list, cpu_list, mem_list]

    # merge two list according to which value is lager
    def update_list(self, list_old, list_new):
        for index, items in enumerate(list_old):
            for i, v in enumerate(items):
                if list_new[index][i] > v:
                    list_old[index][i] = list_new[index][i]

    # when cycle nums equals size, take out the data, and clear queue
    def producer(self, size, limit, list_old, list_new, collection):
        if size == limit:
            res, collect = self.end_producer(list_new, collection)
            self.update_list(list_old, list_new)
            for index, items in enumerate(list_new):
                for i, v in enumerate(items):
                    list_new[index][i] = 0
            return (True, res, collect)
        return (False, [], '')


class DataHandler(object):
    def __init__(self):
        self.modules = ['load', 'cpu', 'memory']

    def push_data(self, data, data_list):
        i = 0
        for val in data.values():
            if data_list[i] < val:
                data_list[i] = val
            i += 1

    def get_data(self, data_list, params_list):
        res = dict()
        for i in xrange(len(data_list)):
            res[params_list[i]] = data_list[i]
        return res

    def catch_data(self):
        return (DataCollection('load').catch(), DataCollection(
            'cpu').catch(), DataCollection('memory').catch())
