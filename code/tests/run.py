#!/usr/bin/env python
# -*- encoding=utf8 -*-

'''
FileName:   run
Author:     Hao Tingyi
@contact:   lokikiller@126.com
@version:   $

Description:

Changelog:

'''

import argparse
import subprocess
import sys

sys.path.append('..')

class Cli(object):
    def __init__(self):
        self.version = '0.1.0'
        self.report = ' --resultlog=./report.log'

    def run(self):
        parser = argparse.ArgumentParser(prog='run.py', usage='python %('
                                                              'prog)s ['
                                                              'Options]',
                                         add_help=False)
        group = parser.add_argument_group('Options')
        group.add_argument('-v', '--version', action='version',
                           version=self.version, help='show program version '
                                                      'number and exit')
        group.add_argument('-h', '--help', action='help', help='show this '
                                                    'help message and exit')
        group.add_argument('-m', '--module=', dest='MODULE', required=True,
                           action='store', help='test module MODULE')

        groupmodules = parser.add_argument_group('Modules')
        groupmodules.add_argument('all collector producer consumer',
                                  action='store_const', const=0)
        self.__handler(parser)

    def __handler(self, parser):
        args = parser.parse_args()
        module = args.MODULE
        getattr(self, 'test_' + module)()

    def test_all(self):
        cmd = 'py.test' + self.report
        subprocess.Popen(cmd, shell=True)

    def test_collector(self):
        cmd = 'py.test collector_test.py' + self.report
        subprocess.Popen(cmd, shell=True)

    def test_consumer(self):
        cmd = 'py.test kafka_consumer_test.py' + self.report
        subprocess.Popen(cmd, shell=True)

    def test_producer(self):
        cmd = 'py.test kafka_producer_test.py' + self.report
        subprocess.Popen(cmd, shell=True)


if __name__ == '__main__':
    Cli().run()