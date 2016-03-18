#!/usr/bin/env python
# -*- encoding=utf8 -*-

'''
FileName:   kafka_consumer_test
Author:     Hao Tingyi / Zhou Boyu
@contact:   lokikiller@126.com / zby22013@163.com
@version:   $

Description:

Changelog:

'''
import sys

import mock

sys.path.append("..")

from utils.mongo_util import DB
from storage.storage import Storage
from utils.kafka_util import KafkaUtil
from pykafka.cluster import Cluster, TopicDict


class TestKafkaConsumer(object):
    @mock.patch.object(DB, 'conn')
    @mock.patch('pykafka.client.KafkaClient')
    @mock.patch.object(Cluster, 'update')
    @mock.patch.object(TopicDict, '_create_topic')
    @mock.patch.object(Cluster, 'topics')
    def test_run(self, mock_topics, mock_create_topic, mock_update,
                 mock_kafka, mock_storage):
        mock_kafka.topics = ['node_0']

        mock_topics.return_value = ['node_0']

        mock_update.return_value = None

        mock_create_topic.return_value = None

        mock_storage.return_value = None

        kafka_client = KafkaUtil('localhost')

        Storage(kafka_client, 'node_0').run()
