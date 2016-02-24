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

from pykafka import KafkaClient
from kazoo.client import KazooClient
import logging
import logging.config

logging.config.fileConfig('../../conf/log.conf')
root_logger = logging.getLogger('root')

class KafkaProducer(object):
    def __init__(self, zk_host, topic):
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
        self.topic = self.client.topics[topic]

        root_logger.info('kafka-host-producer:' + self.KAFKA_HOSTS)
        root_logger.info('kafka-topic-producer:' + topic)

    def kafka_producer(self, lists, collection):
        with self.topic.get_sync_producer() as producer:
            res = [lists, collection]
            message = repr(res)
            producer.produce(message)