import argparse
import curses
import sched
import time
from os.path import dirname, join

from data.getdata import GetData

"""
author: hty / zby
create: 2015.11.30
agent.py -- catch avg_load cpu and memory usage

usage: python agent.py [Options]

Options:
  -v, --version         show program version number and exit
  -h, --help            show this help message and exit
  -t , --ttl            set agent period, default is 60s
  -m MODULE, --module= MODULE
                        use module MODULE

Modules:
  load, cpu, memory
"""


def main():
    with open(join(dirname(__file__), 'version/VERSION'), 'rb') as f:
        version = f.read().decode('ascii').strip()

    parser = argparse.ArgumentParser(prog='agent.py', usage='python %(prog)s [Options]', add_help=False)
    group = parser.add_argument_group('Options')
    group.add_argument('-v', '--version', action='version', version=version,
                       help='show program version number and exit')
    group.add_argument('-h', '--help', action='help', help='show this help message and exit')
    group.add_argument('-t', '--ttl', action='store', type=int, default=60, dest='ttl', metavar='',
                       help='set agent period, default is 60s')
    group.add_argument('-m', '--module=', dest='MODULE', required=True, action='store',
                       help='use module %(dest)s')

    groupmodules = parser.add_argument_group('Modules')
    groupmodules.add_argument('load, cpu, memory', action='store_const', const=0)

    args = parser.parse_args()
    try:
        screen = curses.initscr()
        screen.clear()

        ttl = args.ttl
        inittime = time.time()
        module = args.MODULE

        scheduler.enterabs(inittime, 1, catchdata, (module, inittime, ttl, screen,))
        scheduler.run()
    except Exception:
        curses.endwin()
        parser.parse_args(['-h'])


# TODO: Add unit name
def catchdata(mod, action_time, ttl, screen):
    datas = GetData(mod).catch()
    i = 0
    for data in datas:
        i += 1
        str = '{:<15}\t{:<15}'.format(data, datas[data])
        screen.addstr(i, 0, str, curses.A_NORMAL)
        screen.refresh()

    scheduler.enterabs(action_time + ttl, 1, catchdata, (mod, action_time + ttl, ttl, screen,))


if __name__ == '__main__':
    try:
        scheduler = sched.scheduler(time.time, time.sleep)
        main()
    except KeyboardInterrupt:
        curses.endwin()
        exit()
