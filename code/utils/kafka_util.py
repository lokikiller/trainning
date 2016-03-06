#!/usr/bin/env python
# -*- encoding=utf8 -*-

'''
FileName:   kafka_util
Author:     Hao Tingyi
@contact:   lokikiller@126.com
@version:   $

Description:

Changelog:

'''

from pykafka import KafkaClient
from kazoo.client import KazooClient


class KafkaUtil(object):
    def __init__(self, zk_host):
        # init zk
        self.zkHost = zk_host
        zk = KazooClient(hosts=self.zkHost)
        zk.start()
        kafka_host_list = []
        if zk.exists("/kafka/brokers/"):
            children = zk.get_children("/kafka/brokers/")
            for child in children:
                data, _ = zk.get("/kafka/brokers/" + child)
                kafka_host_list.append(data.decode("utf-8"))
        zk.stop()

        # init kafka
        self.KAFKA_HOSTS = ','.join(kafka_host_list)
        self.client = KafkaClient(hosts=self.KAFKA_HOSTS)

    def kafka_producer(self, lists, collection, topic):
        with self.self.client.topics[topic].get_sync_producer() as producer:
            res = [lists, collection]
            message = repr(res)
            producer.produce(message)

    def kafka_consumer(self, topic):
        consumer = self.self.client.topics[topic].get_simple_consumer()
        for message in consumer:
            if message is not None:
                lists = eval(message.value)
                data_lists = lists[0]
                collection = lists[1]
                return {'lists': data_lists, 'collection': collection}

    def get_topics(self):
        return self.client.topics.keys()
