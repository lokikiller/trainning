#!/usr/bin/env python
# -*- encoding=utf8 -*-

'''
FileName:   cli
Author:     Hao Tingyi
@contact:   lokikiller@126.com
@version:   $

Description:

Changelog:

'''
import argparse
import curses
import sched
import time
import sys

sys.path.append("..")

from data.collector import DataCollection
from data.rpc_sender import RPCSender

class CollectorCLI(object):
    def __init__(self):
        self.VERSION = '0.1.0'
        self.__scheduler = sched.scheduler(time.time, time.sleep)

    def run(self):
        parser = argparse.ArgumentParser(prog='agent.py',
                                         usage='python %(prog)s [Options]',
                                         add_help=False)
        group = parser.add_argument_group('Options')
        group.add_argument('-v', '--version', action='version',
                           version=self.VERSION,
                           help='show program version number and exit')
        group.add_argument('-h', '--help', action='help',
                           help='show this help message and exit')
        group.add_argument('-t', '--ttl', action='store', type=int, default=60,
                           dest='ttl', metavar='',
                           help='set agent period, default is 60s')
        group.add_argument('-m', '--module=', dest='MODULE', required=True,
                           action='store',
                           help='use module %(dest)s')
        group.add_argument('-s', '--show', action='store', dest='show',
                           type=bool,
                           help='show data in terminal and do not store data')
        group.add_argument('-zk', '--zookeeper', action='store',
                           dest='zookeeper', help='zookeeper address use in '
                                                  'distributed environment')
        group.add_argument('-ip', '--address', action='store', dest='ip',
                           help='data queue address')
        group.add_argument('-port', '--port', action='store', dest='port',
                           help='data queue port')

        groupmodules = parser.add_argument_group('Modules')
        groupmodules.add_argument('all, load, cpu, memory',
                                  action='store_const',
                                  const=0)

        self.__handler(parser)

    def __handler(self, parser):
        args = parser.parse_args()
        if args.show:
            ttl = args.ttl
            module = args.MODULE
            self.show_data_terminal(ttl, module, parser)
        else:
            zk_host = args.zookeeper
            ip = args.ip
            port = args.port
            producer = RPCSender(zk_host, ip, port)
            producer.setDaemon(True)
            producer.run()

    def show_data_terminal(self, ttl, module, parser):
        try:
            screen = curses.initscr()
            screen.clear()
            init_time = time.time()

            self.__scheduler.enterabs(init_time, 1, self.__catch_data,
                                      (module, init_time, ttl, screen,))
            self.__scheduler.run()
        except Exception:
            curses.endwin()
            parser.parse_args(['-h'])

    def __catch_data(self, mod, action_time, ttl, screen):
        datas = DataCollection(mod).catch()
        i = 0
        for data in datas:
            i += 1
            format_str = '{:<15}\t{:<25}'.format(data, datas[data])
            screen.addstr(i, 0, format_str, curses.A_NORMAL)
            screen.refresh()

        self.__scheduler.enterabs(action_time + ttl, 1, self.__catch_data,
                                  (mod, action_time + ttl, ttl, screen,))
