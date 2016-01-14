#!/usr/bin/env python
# -*- encoding=utf8 -*-

'''
FileName:   collector_test
Author:     Hao Tingyi
@contact:   lokikiller@126.com
@version:   $

Description:

Changelog:

'''
import sys

import mock
import pytest

sys.path.append("..")

from data.collector import DataCollection

from data.exception.module import ModuleException
from subprocess import Popen


class TestCollector(object):
    def test_raise(self):
        with  pytest.raises(ModuleException) as excinfo:
            DataCollection('abc').catch()

    @mock.patch.object(Popen, 'communicate')
    def test_load(self, communicate_mock):
        communicate_mock.return_value = ['1 2 3']
        assert DataCollection('load').catch() == {'w1_avg': '1', 'w5_avg': '2',
                                                  'w15_avg': '3'}

    @mock.patch.object(Popen, 'communicate')
    def test_cpu(self, communicat_mock):
        list1 = ['1 2 3 4 5 6 7 8 9 10']
        list2 = ['11 12 13 14 15 16 17 18 19 20']
        communicat_mock.side_effect = [list1, list2]
        assert DataCollection('cpu').catch() == {'user': 0.1, 'nice': 0.1,
                                                 'system': 0.1, 'idle': 0.1,
                                                 'iowait': 0.1, 'irq': 0.1,
                                                 'softirq': 0.1, 'steal': 0.1,
                                                 'guest': 0.1,
                                                 'guest_nice': 0.1}

    @mock.patch.object(Popen, 'communicate')
    def test_memory(self, communicat_mock):
        data = ['4 k\n1 k\n1 k\n1 k\n1 k\n1 k\n2 k\n1 k\n']
        communicat_mock.side_effect = [data]
        assert DataCollection('memory').catch() == {'total': 4096,
                                                    'free': 1024,
                                                    'buffers': 1024,
                                                    'cached': 1024,
                                                    'active': 1024,
                                                    'inactive': 1024,
                                                    'used': 3072,
                                                    'abs_used': 1024,
                                                    'swap_used': 1024}
