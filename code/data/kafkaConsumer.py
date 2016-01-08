#! /usr/bin/env python
# -*- encoding=utf8 -*-

'''
FileName:   kafkaConsumer
Author:     Hao Tingyi / Zhou Boyu
@contact:   lokikiller@126.com / zby22013@163.com
@version:   $

Description:
        consume data from kafka, and storage into database
Changelog:
        create at 2015.1.6
'''

from pykafka import KafkaClient
import time
import threading
from storage import Storage
import socket


class KafkaConsumer(threading.Thread):
    def __init__(self, kafka_hosts, topic_name):
        threading.Thread.__init__(self)

        self.KAFKA_HOSTS = kafka_hosts
        self.TOPIC_NAME = topic_name

        self.client = KafkaClient(hosts=self.KAFKA_HOSTS)
        self.topic = self.client.topics[self.TOPIC_NAME]

        db = Storage()
        self.db = db.conn()

        hostname = socket.getfqdn(socket.gethostname())
        ip = socket.gethostbyname(hostname)
        self.unique = hostname + '/' + ip

    def __consume(self):
        consumer = self.topic.get_simple_consumer()
        for message in consumer:
            if message is not None:
                lists = eval(message.value)
                data_lists = lists[0]
                collection = lists[1]
                self.__store_data(data_lists, collection)

    def __store_data(self, lists, collection):
        dbnames = ['load', 'cpu', 'memory']
        limit = getattr(self, collection)
        for index, items in enumerate(lists):
            storages = {"time": time.time(), "name": self.unique,
                        "data": items}
            tb = self.db[collection + '_' + dbnames[index]]
            tb.insert_one(storages)
            if tb.find({'name': self.unique}).count() > limit:
                data = tb.find({'name': self.unique}).sort('time').limit(
                    1).next()
                tb.find_one_and_delete({'_id': data['_id']})

    def run(self):
        self.__consume()


def main():
    TOPICS = ['node_135', 'node_138']
    for topic_name in TOPICS:
        consumer = KafkaConsumer("123.58.165.135:9092,123.58.165.138:9092",
                                 topic_name)
        consumer.run()


if __name__ == '__main__':
    main()
