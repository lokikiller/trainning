#!/usr/bin/env python
# -*- encoding=utf8 -*-

'''
FileName:   kafka_producer_test
Author:     Hao Tingyi / Zhou Boyu
@contact:   lokikiller@126.com / zby22013@163.com
@version:   $

Description:

Changelog:

'''

import collections
import sys

import mock
import pytest

sys.path.append("..")

from data.filter import DataHandler,Filter
from kazoo.client import KazooClient
from pykafka.cluster import Cluster, TopicDict


class TestDataHandler(object):
    def test_push_data(self):
        data_dict = collections.OrderedDict()
        data_dict['data1'] = 2
        data_dict['data2'] = 3
        data_dict['data3'] = 4
        data_list = [1, 2, 3]
        DataHandler().push_data(data_dict, data_list)
        assert data_list == [2, 3, 4]

    def test_get_data(self):
        data_list = [1, 2, 3]
        param_list = ['data1', 'data2', 'data3']
        assert DataHandler().get_data(data_list, param_list) == {'data1': 1,
                                                                 'data2': 2,
                                                                 "data3": 3}


class TestKafkaProducer(object):
    @mock.patch.object(KazooClient, 'start')
    @mock.patch.object(KazooClient, 'exists')
    @mock.patch.object(KazooClient, 'get_children')
    @mock.patch.object(KazooClient, 'get')
    @mock.patch.object(KazooClient, 'stop')
    @mock.patch('socket.gethostbyname')
    @mock.patch('pykafka.client.KafkaClient')
    @mock.patch.object(Cluster, 'update')
    @mock.patch.object(TopicDict, '_create_topic')
    @mock.patch.object(Cluster, 'topics')
    @mock.patch('time.sleep')
    def test_run(self, mock_sleep, mock_cluster, mock_topic, mock_update,
                 mock_kafka,
                 mock_host,
                 mock_zk_stop,
                 mock_zk_get, mock_zk_child,
                 mock_zk_exists, mock_zk_start):
        mock_zk_start.return_value = None
        mock_zk_exists.return_value = True
        mock_zk_child.return_value = ['node']
        mock_zk_get.return_value = 'localhost', None
        mock_zk_stop.return_value = None

        mock_host.return_value = '0.0.0.0'

        mock_kafka.topics = ['node_0']

        mock_cluster.return_value = ['node_0']

        mock_update.return_value = None

        mock_topic.return_value = None

        mock_sleep.side_effect = Exception('Boom')

        with pytest.raises(Exception) as excinfo:
            Filter('localhost','0.0.0.0','80').run()

        assert excinfo.value.message == 'Boom'
