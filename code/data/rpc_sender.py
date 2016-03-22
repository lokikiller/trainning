#!/usr/bin/env python
# -*- encoding=utf8 -*-

'''
FileName:   rpc_sender
Author:     Hao Tingyi
@contact:   lokikiller@126.com
@version:   $

Description:

Changelog:

'''

import socket
import xmlrpclib
import threading
import time
from filter import Filter


class RPCSender(threading.Thread):
    def __init__(self, zk_host, ip, port):
        threading.Thread.__init__(self)

        hostname = socket.getfqdn(socket.gethostname())
        node = socket.gethostbyname(hostname)
        self.TOPIC_NAME = "node_" + node.split(".")[3]
        self.zk_host = zk_host
        self.ip = ip
        self.port = port

        # init list size
        self.ONE_MIN_LIST_SIZE = 2
        self.FIVE_MIN_LIST_SIZE = 5
        self.THIRTY_MIN_LIST_SIZE = 6
        self.ONE_DAY_LIST_SIZE = 48

        self.filter = Filter()

    # data_queue
    def __push_queue(self, lists, collection):
        proxy = xmlrpclib.ServerProxy("http://" + self.ip + ":" + self.port +
                                      "/")
        multicall = xmlrpclib.MultiCall(proxy)
        multicall.push(lists, collection, self.TOPIC_NAME)

    def run(self):
        one_min_size = 0
        one_min_list = self.filter.new_list()

        five_min_size = 0
        five_min_list = self.filter.new_list()

        thirty_min_size = 0
        thirty_min_list = self.filter.new_list()

        one_day_size = 0
        one_day_list = self.filter.new_list()

        while True:
            self.filter.pre_producer(one_min_list)

            one_min_size += 1
            res_one, lis_one, collect_one = self.filter.producer(one_min_size,
                self.ONE_MIN_LIST_SIZE, five_min_list, one_min_list, "one_min")
            if res_one:
                self.__push_queue(lis_one, collect_one)
                one_min_size = 0

                five_min_size += 1
                res_five, lis_five, collect_five = self.filter.producer(
                    five_min_size, self.FIVE_MIN_LIST_SIZE, thirty_min_list,
                    five_min_list, "five_min")
                if res_five:
                    self.__push_queue(lis_five, collect_five)
                    five_min_size = 0

                    thirty_min_size += 1
                    res_thirty, lis_thirty, collect_thirty = \
                        self.filter.producer(thirty_min_size,
                        self.THIRTY_MIN_LIST_SIZE, one_day_list,
                        thirty_min_list, "thirty_min")
                    if res_thirty:
                        self.__push_queue(lis_thirty, collect_thirty)
                        thirty_min_size = 0

                        one_day_size += 1
                        res, lis, collect = self.filter.producer(
                            one_day_size, self.ONE_DAY_LIST_SIZE,
                            self.filter.new_list(),  one_day_list, "one_day")
                        if res:
                            self.__push_queue(lis, collect)
                            one_day_size = 0

            time.sleep(30)
