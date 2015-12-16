#!/usr/bin/env python
# -*- encoding=utf8 -*-

'''
FileName:   agent
Author:     Hao Tingyi / Zhou Boyu
@contact:   lokikiller@126.com / zby22013@163.com
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

import argparse
import curses
import sched
import time
from data.collector import DataCollection


class CollectorCLI(object):
    def __init__(self):
        self.VERSION = '0.1.0'
        self.__scheduler = sched.scheduler(time.time, time.sleep)

    def cli(self):
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

        groupmodules = parser.add_argument_group('Modules')
        groupmodules.add_argument('all, load, cpu, memory',
                                  action='store_const',
                                  const=0)

        args = parser.parse_args()
        try:
            screen = curses.initscr()
            screen.clear()

            ttl = args.ttl
            inittime = time.time()
            module = args.MODULE

            self.__scheduler.enterabs(inittime, 1, self.__catchdata,
                                      (module, inittime, ttl, screen,))
            self.__scheduler.run()
        except Exception, e:
            curses.endwin()
            parser.parse_args(['-h'])

    # TODO: Add unit name
    def __catchdata(self, mod, action_time, ttl, screen):
        datas = DataCollection(mod).catch()
        i = 0
        for data in datas:
            i += 1
            str = '{:<15}\t{:<25}'.format(data, datas[data])
            screen.addstr(i, 0, str, curses.A_NORMAL)
            screen.refresh()

        self.__scheduler.enterabs(action_time + ttl, 1, self.__catchdata,
                                  (mod, action_time + ttl, ttl, screen,))


if __name__ == '__main__':
    try:
        CollectorCLI().cli()
    except KeyboardInterrupt:
        curses.endwin()
        exit()
