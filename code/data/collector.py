#!/usr/bin/env python
# -*- encoding=utf8 -*-

'''
FileName:   collector
Author:     Hao Tingyi / Zhou Boyu
@contact:   lokikiller@126.com
@version:   $

Description:
    collect cpu/memory/load data from /proc file
Changelog:
    create at 2015.12.15
'''

import subprocess
import time
import collections
from exception.module import ModuleException


class DataCollection(object):
    def __init__(self, mod):
        self.mod = mod
        method_name = 'get_%s' % (self.mod,)
        self.get_data = getattr(self, method_name, self.__raise_no_module)

    def get_cpu(self):
        cmd = "sed -n 's/^cpu\s//p' /proc/stat"
        process1 = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        cpu_array1 = process1.communicate()[0].strip().split(' ')
        total1 = 0
        for val in cpu_array1:
            total1 += int(val)

        time.sleep(5)

        process2 = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        cpu_array2 = process2.communicate()[0].strip().split(' ')
        total2 = 0
        for val in cpu_array2:
            total2 += int(val)

        diff = total2 - total1
        result = collections.OrderedDict()
        key_list = (
            'user', 'nice', 'system', 'idle', 'iowait', 'irq', 'softirq',
            'steal',
            'guest', 'guest_nice')

        for i in range(10):
            result[key_list[i]] = (float(cpu_array2[i]) - float(
                cpu_array1[i])) / diff

        return result

    def get_memory(self):
        cmd = "cat /proc/meminfo | grep -w 'MemTotal:\|MemFree:\|Buffers:" \
              "\|Cached:\|Active:\|Inactive:\|SwapTotal:\|SwapFree:'"
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        list = []
        for val in process.communicate()[0].strip().split('\n'):
            list.append(int(val.split(' ')[-2]) * 1024)

        result = collections.OrderedDict()
        result['total'] = list[0]
        result['used'] = list[0] - list[1]
        result['abs_used'] = list[0] - (list[1] + list[2] + list[3])
        result['free'] = list[1]
        result['buffers'] = list[2]
        result['cached'] = list[3]
        result['active'] = list[4]
        result['inactive'] = list[5]
        result['swap_used'] = list[6] - list[7]

        return result

    def get_load(self):
        cmd = "cat /proc/loadavg"
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        data = process.communicate()[0].strip().split(' ')
        result = collections.OrderedDict()
        key_list = ('w1_avg', 'w5_avg', 'w15_avg')

        for i in range(3):
            result[key_list[i]] = data[i]

        return result

    def get_all(self):
        cpu_result = self.get_cpu()
        memory_result = self.get_memory()
        load_result = self.get_load()
        result = collections.OrderedDict(
            cpu_result.items() + memory_result.items() + load_result.items())
        return result

    def __raise_no_module(self):
        raise ModuleException('no such module ' + self.mod)

    def catch(self):
        return self.get_data()