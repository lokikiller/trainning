import json
import subprocess
from exception.module import ModuleException
from collections import OrderedDict

"""
author: hty / zby
create: 2015.12.07
getdata.py -- catch avg_load cpu and memory usage from scripts

usage:
    new instance with GetData('MODULE') MODULE means cpu/memory/load
    get data with catch() function, data type depend on MODULE, and return jsonType

MODULE:
    load: w1_avg/ w5_avg/ w15_avg
    cpu: user/ nice/ system/ idle/ iowait/ irq/ softirq/ steal/ guest/ guest_nice
    memory: total/ used/ abs_used/ free/ buffers/ cached/ active/ inactive/ swap_used
"""


class GetData(object):
    def __init__(self, mod):
        self.__scriptPath = '../scripts/'
        self.mod = mod

    def __get_cpu(self):
        return subprocess.check_output(self.__scriptPath + 'cpu.sh')

    def __get_memory(self):
        return subprocess.check_output(self.__scriptPath + 'mem.sh')

    def __get_load(self):
        return subprocess.check_output(self.__scriptPath + 'loadavg.sh')

    def catch(self):
        '''
        catching data form different module, if module is not in [cpu, memory, load], raise exception
        :return: data format dict
        '''
        data = ''
        if self.mod == 'cpu':
            data = self.__get_cpu()
        elif self.mod == 'memory':
            data = self.__get_memory()
        elif self.mod == 'load':
            data = self.__get_load()
        else:
            raise ModuleException('no such module ' + self.mod)
        return json.loads(data, object_pairs_hook=OrderedDict)
