#!/usr/bin/env python
# -*- encoding=utf8 -*-

'''
FileName:   cli_test
Author:     Zhou Boyu
@contact:   zby22013@163.com
@version:   $

Description:

    Changelog:

        '''

import os

from cli.cli import CollectorCLI

class Test_cli(object):
    def test_cli(self):
        os.system('python code/agent.py -t 1 -m cpu')
