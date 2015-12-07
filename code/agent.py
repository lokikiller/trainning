import sched
import sys, time
import argparse
from data.getdata import GetData

"""
author: hty / zby
create: 2015.11.30
agent.py -- catch avg_load cpu and memory usage
"""

scheduler = sched.scheduler(time.time, time.sleep)


def main():
    parser = argparse.ArgumentParser(prog='agent.py', usage='python %(prog)s [Options]', add_help=False)
    group = parser.add_argument_group('Options')
    group.add_argument('-v', '--version', action='version', help='show program version number and exit')
    group.add_argument('-h', '--help', action='help', help='show this help message and exit')
    group.add_argument('-t', '--ttl', action='store', type=int, default=60, dest='ttl', metavar='',
                       help='set agent period, default is 60s')
    group.add_argument('-m', '--module=', dest='MODULE', required=True, action='store',
                       help='use module %(dest)s')

    groupmodules = parser.add_argument_group('Modules')
    groupmodules.add_argument('load, cpu, memory', action='store_const', const=0)

    args = parser.parse_args()

    ttl = args.ttl
    inittime = time.time()
    module = args.MODULE

    scheduler.enterabs(inittime, 1, catchdata, (module, inittime, ttl,))
    scheduler.run()


def catchdata(mod, action_time, ttl):
    datas = GetData(mod).catch()
    for data in datas:
        print '%-15s\t%-15s' % (data, datas[data])
    scheduler.enterabs(action_time + ttl, 1, catchdata, (mod, action_time + ttl, ttl,))


if __name__ == '__main__':
    main()
