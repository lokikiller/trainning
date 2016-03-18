#!/usr/bin/env python
# -*- encoding=utf8 -*-

'''
FileName:   storage
Author:     Hao Tingyi
@contact:   lokikiller@126.com
@version:   $

Description:

Changelog:

'''
import argparse
import threading
import time
from utils.kafka_util import KafkaUtil
from utils.mongo_util import DB


class Storage(threading.Thread):
    def __init__(self, kafka_client, topic):
        threading.Thread.__init__(self)

        self.kafka_client = kafka_client
        self.topic = topic

        self.one_min = 30
        self.five_min = 36
        self.thirty_min = 48
        self.one_day = 30

        db = DB()
        self.db = db.conn()

    def __storage_data(self):
        con = self.kafka_client.kafka_consumer(self.topic)
        if con is not None:
            lists, collection = con
            dbnames = ['load', 'cpu', 'memory']
            limit = getattr(self, collection)
            for index, items in enumerate(lists):
                storages = {"time": time.time(), "name": self.topic,
                            "data": items}
                tb = self.db[collection + '_' + dbnames[index]]
                tb.insert_one(storages)
                if tb.find({'name': self.topic}).count() > limit:
                    data = tb.find({'name': self.topic}).sort('time').limit(
                        1).next()
                    tb.find_one_and_delete({'_id': data['_id']})

    def run(self):
        self.__storage_data()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-zk', '--zookeeper', action='store',
                        dest='zookeeper', help='zookeeper address use in '
                                               'distributed environment')
    args = parser.parse_args()
    zk_host = args.zookeeper
    kafka_client = KafkaUtil(zk_host)

    threads = []
    for topic_name in kafka_client.get_topics():
        if topic_name.startswith('node_'):
            consumer = Storage(kafka_client, topic_name)
            consumer.setDaemon(True)
            consumer.start()
            threads.append(consumer)

    for thread in threads :
        thread.join()


if __name__ == '__main__':
    main()
