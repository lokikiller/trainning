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

import argparse
import threading
import time

from pykafka import KafkaClient
from kazoo.client import KazooClient
from storage import Storage


class KafkaConsumer(threading.Thread):
    def __init__(self, kafka_hosts, topic_name):
        threading.Thread.__init__(self)

        self.KAFKA_HOSTS = kafka_hosts
        self.TOPIC_NAME = topic_name

        self.client = KafkaClient(hosts=self.KAFKA_HOSTS)
        self.topic = self.client.topics[self.TOPIC_NAME]

        self.one_min = 30
        self.five_min = 36
        self.thirty_min = 48
        self.one_day = 30

        db = Storage()
        self.db = db.conn()

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
            storages = {"time": time.time(), "name": self.TOPIC_NAME,
                        "data": items}
            tb = self.db[collection + '_' + dbnames[index]]
            tb.insert_one(storages)
            if tb.find({'name': self.TOPIC_NAME}).count() > limit:
                data = tb.find({'name': self.TOPIC_NAME}).sort('time').limit(
                    1).next()
                tb.find_one_and_delete({'_id': data['_id']})

    def run(self):
        self.__consume()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-zk', '--zookeeper', action='store',
                           dest='zookeeper', help='zookeeper address use in '
                                                  'distributed environment')
    args = parser.parse_args()
    zk_host = args.zookeeper

    zk = KazooClient(hosts=zk_host)
    zk.start()
    kafka_host_list = []
    if zk.exists("/kafka/brokers/"):
        children = zk.get_children("/kafka/brokers/")
        for child in children:
            data, _ = zk.get("/kafka/brokers/" + child)
            kafka_host_list.append(data.decode("utf-8"))
    zk.stop()

    kafka_hosts = ','.join(kafka_host_list)

    threads = []

    client = KafkaClient(hosts=kafka_hosts)
    for topic_name in client.topics.keys():
        if topic_name.startswith('node_'):
            consumer = KafkaConsumer(kafka_hosts, topic_name)
            consumer.setDaemon(True)
            consumer.start()
            threads.append(consumer)

    for thread in threads :
        thread.join()


if __name__ == '__main__':
    main()
