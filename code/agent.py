#!/usr/bin/env python
# -*- encoding=utf8 -*-

'''
FileName:   agent
Author:     Hao Tingyi / Zhou Boyu
@contact:   lokikiller@126.com
@version:   $

Description:
    usage: python agent.py [Options]

    Options:
      -v, --version         show program version number and exit
      -h, --help            show this help message and exit
      -t , --ttl            set agent period, default is 60s
      -m MODULE, --module= MODULE
                            use module MODULE

    Modules:
      all, load, cpu, memory
Changelog:
    create at 2015.12.14
'''

import curses
from cli.cli import CollectorCLI

if __name__ == '__main__':
    try:
        CollectorCLI().run()
    except KeyboardInterrupt:
        curses.endwin()
        exit()
