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

from subprocess import Popen, PIPE
from cli.cli import CollectorCLI

class Test_cli(object):
    def test_cli(self):
        popen = Popen("python code/agent.py -t 1 -m load -s show",
                         shell = True, stdout = PIPE)
        next_line = ""
        while True:
            next_line = next_line + popen.stdout.readline()
            if 'w5_avg' in next_line:
                break
        popen.terminate()
        assert "w1_avg" in next_line
        assert "w5_avg" in next_line

    def test_version(self):
        p = Popen("python code/agent.py -v", shell=True, stdout=PIPE, stderr=PIPE)
        p.wait()
        version_info = p.stderr.read()
        assert p.returncode == 0
        assert version_info == "0.1.0\n"

    def test_help(self):
        p = Popen("python code/agent.py -h", shell=True, stdout=PIPE, stderr=PIPE)
        p.wait()
        help_info = p.stdout.read()
        assert p.returncode == 0
        assert "usage: python agent.py [Options]" in help_info 
