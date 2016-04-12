#!/usr/bin/env python
# -*- encoding=utf8 -*-

'''
FileName:   dataqueue
Author:     Hao Tingyi
@contact:   lokikiller@126.com
@version:   $

Description:

Changelog:

'''

from SimpleXMLRPCServer import SimpleXMLRPCServer, SimpleXMLRPCRequestHandler
import SocketServer
from utils.kafka_util import KafkaUtil


class AsyncXMLRPCServer(SocketServer.ThreadingMixIn, SimpleXMLRPCServer):
    pass


class DataQueue(object):
    def __init__(self, ip, port, zk_host):
        self.server = AsyncXMLRPCServer((ip, port), SimpleXMLRPCRequestHandler)
        self.zk_host = zk_host
        self.kafka_client = KafkaUtil(self.zk_host)
        self.server.register_multicall_functions()
        self.server.register_function(self.push, 'push')
        self.server.serve_forever()

    def push(self, lists, collection, topic):
        self.kafka_client.kafka_producer(lists, collection, topic)
