import argparse

"""
author: hty / zby
create: 2015.11.30
agent.py -- catch avg_load cpu and memory usage
"""

parser = argparse.ArgumentParser(prog='agent.py', usage='python %(prog)s [Options]', add_help=False)
group = parser.add_argument_group('Options')
group.add_argument('-v', '--version', action='version', help='show program version number and exit')
group.add_argument('-h', '--help', action='help', help='show this help message and exit')
group.add_argument('-t', '--ttl', action='store', type=int, default=60, dest='ttl', metavar='',
                   help='set agent period, default is 60s')
group.add_argument('-m', '--module=', dest='MODULE', required=True, action='store',
                   help='use module %(dest)s')

groupmodules = parser.add_argument_group('Modules')
groupmodules.add_argument('all, cpu, memory', action='store_const', const=0)

args = parser.parse_args()

ttl = args.ttl
print ttl

module = args.MODULE
if module == 'all':
    print module
elif module == 'cpu':
    print module
elif module == 'memory':
    print module
