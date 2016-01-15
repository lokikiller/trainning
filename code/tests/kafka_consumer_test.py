#!/usr/bin/env python
# -*- encoding=utf8 -*-

'''
FileName:   kafka_consumer_test
Author:     Hao Tingyi
@contact:   lokikiller@126.com
@version:   $

Description:

Changelog:

'''
import sys

import mock

sys.path.append("..")

from data.storage import Storage
from data.kafka_consumer import KafkaConsumer
from pykafka.cluster import Cluster, TopicDict


class TestKafkaConsumer(object):
    @mock.patch.object(Storage, 'conn')
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

        KafkaConsumer('localhost', 'node_0').run()
