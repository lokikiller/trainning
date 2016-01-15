#!/usr/bin/env python
# -*- encoding=utf8 -*-

'''
FileName:   cli_test
Author:     Hao Tingyi
@contact:   lokikiller@126.com
@version:   $

Description:

Changelog:

'''
import subprocess
import sys

sys.path.append("..")

class TestCli(object):

    def test_run_help(self):
        code = subprocess.call(['python', 'agent.py', '-h'])
        assert code == 0

    def test_run_version(self):
        code = subprocess.call(['python', 'agent.py', '-v'])
        assert code == 0

