#!/usr/bin/env python
# -*- encoding=utf8 -*-

'''
FileName:   kafkaProducer
Author:     Hao Tingyi / Zhou Boyu
@contact:   lokikiller@126.com / zby22013@163.com
@version:   $

Description:
    filt data from data-set, using queue to filt the max data in each set,
every 30 seconds and push data to kafka.

Changelog:
    create at 2015.12.15 by Haotingyi
    modify at 2015.1.6 by Zhou boyu
'''

import socket
import threading
import time
from collector import DataCollection
from kafka_producer import KafkaProducer

import logging
import logging.config

logging.config.fileConfig('../../conf/log.conf')
root_logger = logging.getLogger('root')

class Filter(threading.Thread):
    def __init__(self, zk_host):
        threading.Thread.__init__(self)


        hostname = socket.getfqdn(socket.gethostname())
        ip = socket.gethostbyname(hostname)
        self.TOPIC_NAME = "node_" + ip.split(".")[3]
        self.zk_host = zk_host

        # init list size
        self.ONE_MIN_LIST_SIZE = 2
        self.FIVE_MIN_LIST_SIZE = 5
        self.THIRTY_MIN_LIST_SIZE = 6
        self.ONE_DAY_LIST_SIZE = 48

        # init key for dict
        self.load_params = ["w1_avg", "w5_avg", "w15_avg"]
        self.cpu_params = ["user", "nice", "system", "idle", "iowait",
                           "irq", "softirq", "steal", "guest", "guest_nice"]
        self.mem_params = ["total", "used", "abs_used", "free", "buffers",
                           "cached", "active", "inactive", "swap_used"]

        # init data handler
        self.handler = DataHandler()

        # init data length for a host  
        self.one_min = 30
        self.five_min = 36
        self.thirty_min = 48
        self.one_day = 30

    # get data(type dict) from collector and extract value from dict
    def __pre_producer(self, lists):
        data_set = self.handler.catch_data()
        for index, datas in enumerate(data_set):
            self.handler.push_data(datas, lists[index])
        return lists

    # pack data(type list) to dict(add key)
    def __end_producer(self, lists, collection):
        params_list = [self.load_params, self.cpu_params, self.mem_params]
        res = []
        for index, items in enumerate(lists):
            res.append(self.handler.get_data(items, params_list[index]))
        self.__kafka_producer(res, collection)

    # kafka producer
    def __kafka_producer(self, lists, collection):
        producer = KafkaProducer(self.zk_host, self.TOPIC_NAME)
        producer.kafka_producer(lists, collection)

    # init data manage queue
    def __new_list(self):
        load_list = [0 for i in range(len(self.load_params))]
        cpu_list = [0 for i in range(len(self.cpu_params))]
        mem_list = [0 for i in range(len(self.mem_params))]
        return [load_list, cpu_list, mem_list]

    # merge two list according to which value is lager
    def __update_list(self, list_old, list_new):
        for index, items in enumerate(list_old):
            for i, v in enumerate(items):
                if list_new[index][i] > v:
                    list_old[index][i] = list_new[index][i]

    # when cycle nums equals size, take out the data, and clear queue
    def __producer(self, size, limit, list_old, list_new, collection):
        if size == limit:
            self.__end_producer(list_new, collection)
            self.__update_list(list_old, list_new)
            for index, items in enumerate(list_new):
                for i, v in enumerate(items):
                    list_new[index][i] = 0
            return True
        return False

    def run(self):
        one_min_size = 0
        one_min_list = self.__new_list()

        five_min_size = 0
        five_min_list = self.__new_list()

        thirty_min_size = 0
        thirty_min_list = self.__new_list()

        one_day_size = 0
        one_day_list = self.__new_list()

        while True:
            self.__pre_producer(one_min_list)

            one_min_size += 1
            if self.__producer(one_min_size, self.ONE_MIN_LIST_SIZE,
                               five_min_list, one_min_list, "one_min"):
                one_min_size = 0

                five_min_size += 1
                if self.__producer(five_min_size, self.FIVE_MIN_LIST_SIZE,
                                   thirty_min_list, five_min_list, "five_min"):
                    five_min_size = 0

                    thirty_min_size += 1
                    if self.__producer(thirty_min_size,
                                       self.THIRTY_MIN_LIST_SIZE,
                                       one_day_list, thirty_min_list,
                                       "thirty_min"):
                        thirty_min_size = 0

                        one_day_size += 1
                        if self.__producer(one_day_size,
                                           self.ONE_DAY_LIST_SIZE,
                                           self.__new_list(), one_day_list,
                                           "one_day"):
                            one_day_size = 0

            time.sleep(30)


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
