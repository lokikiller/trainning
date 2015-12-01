import argparse

"""
author: hty / zby
create: 2015.11.30
agent.py -- catch avg_load cpu and memory usage
"""

parser = argparse.ArgumentParser(prog='agent.py', usage='python %(prog)s [Options]', add_help=False)
group = parser.add_argument_group('Options')
group.add_argument('-v', '--version', action='version')
group.add_argument('-h', '--help', action='help', help='show this help message and exit')
group.add_argument('-t', '--ttl',action='store_true', help='set agent period, default is 60s')
group.add_argument('-m', '--module=', dest='module', action='store', help='use modele MODULE')

groupmodules = parser.add_argument_group('Modules')
groupmodules.add_argument('all, cpu, memory')

args = parser.parse_args(['-h'])