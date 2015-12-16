#!/usr/bin/env python
# -*- encoding=utf8 -*-

'''
FileName:   filter
Author:     Hao Tingyi / Zhou Boyu
@contact:   lokikiller@126.com
@version:   $

Description:
    filt data from data-set, using queue to filt the max data in each set,
every 30 seconds.

Changelog:
    create at 2015.12.15
'''

from collector import DataCollection
import time
import threading


class DataFilter(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.ONE_MIN_LIST_SIZE = 2
        self.FIVE_MIN_LIST_SIZE = 5
        self.THIRTY_MIN_LIST_SIZE = 6
        self.ONE_DAY_LIST_SIZE = 48

        self.LOAD_PARAMS = ["w1_avg", "w5_avg", "w15_avg"]
        self.CPU_PARAMS = ["user", "nice", "system", "idle", "iowait",
                           "irq", "softirq", "steal", "guest", "guest_nice"]
        self.MEM_PARAMS = ["total", "used", "abs_used", "free", "buffers",
                           "cached", "active", "inactive", "swap_used"]

        self.handler = DataHandler()

    def __pre_filter(self, lists):
        dataSet = self.handler.catch_data()
        for index, datas in enumerate(dataSet):
            self.handler.push_data(datas, lists[index])
        return lists

    def __end_filter(self, lists, collection):
        params_list = [self.LOAD_PARAMS, self.CPU_PARAMS, self.MEM_PARAMS]
        res = []
        for index, items in enumerate(lists):
            res.append(self.handler.get_data(items, params_list[index]))
        self.handler.store_data(res, collection)

    def __new_list(self):
        load_list = [0 for i in range(len(self.LOAD_PARAMS))]
        cpu_list = [0 for i in range(len(self.CPU_PARAMS))]
        mem_list = [0 for i in range(len(self.MEM_PARAMS))]
        return [load_list, cpu_list, mem_list]

    def __update_list(self, list_old, list_new):
        for index, items in enumerate(list_old):
            for i, v in enumerate(items):
                if list_new[index][i] > v:
                    list_old[index][i] = list_new[index][i]

    def __filter(self, size, limit, list_old, list_new, collection):
        if size == limit:
            self.__end_filter(list_new, collection)
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
            self.__pre_filter(one_min_list)

            one_min_size += 1
            if self.__filter(one_min_size, self.ONE_MIN_LIST_SIZE,
                             five_min_list, one_min_list, "one_min"):
                one_min_size = 0

                five_min_size += 1
                if self.__filter(five_min_size, self.FIVE_MIN_LIST_SIZE,
                                 thirty_min_list, five_min_list, "five_min"):
                    five_min_size = 0

                    thirty_min_size += 1
                    if self.__filter(thirty_min_size,
                                     self.THIRTY_MIN_LIST_SIZE,
                                     one_day_list, thirty_min_list,
                                     "thirty_min"):
                        thirty_min_size = 0

                        one_day_size += 1
                        if self.__filter(one_day_size, self.ONE_DAY_LIST_SIZE,
                                         self.__new_list(), one_day_list,
                                         "one_day"):
                            one_day_size = 0

            time.sleep(30)


class DataHandler(object):
    def push_data(self, data, list):
        i = 0
        for val in data.values():
            if list[i] < val:
                list[i] = val
            i += 1

    def get_data(self, list, params_list):
        res = dict()
        for i in xrange(len(list)):
            res[params_list[i]] = list[i]
        return res

    def store_data(self, lists, collection):
        # TODO: store data into DataBase Mongo
        print collection + ":"
        print lists

    def catch_data(self):
        return (DataCollection('load').catch(), DataCollection(
            'cpu').catch(), DataCollection('memory').catch())


def main():
    filter = DataFilter()
    filter.setDaemon(True)
    filter.run()

if __name__ == '__main__':
    main()
