#!/usr/bin/python3
import argparse
import os
import sys

import gs
from servers import *

# get servers
servers = {}
for s in gs.servers:
    servers[s.id] = s

# setup data dir
dataDir = os.path.dirname(os.path.realpath(__file__)) + '/data'
if not os.path.isdir(dataDir):
    os.mkdir(dataDir)

# Parse command-line arguments
parser = argparse.ArgumentParser(description='GameServer Manager')
parser.add_argument('server')
parser.add_argument('command', nargs='*')

args = parser.parse_args()

if args.server in servers:
    server = servers[args.server]

    # load server data
    dataFile = dataDir + '/' + server.id
    if os.path.isfile(dataFile):
        with open(dataFile) as f:
            server.pid = int(f.read())

    try:
        # handle command
        server.handle(args.command)

        # write server data
        with open(dataFile, 'w') as f:
            f.write(str(server.pid))

    except gs.GameServerError as err:
        print('ERROR handling \'' + args.command[0]
            + '\' for \'' + server.id + '\':\n' + str(err))
else:
    print('Unknown server \'' + args.server + '\'')

sys.exit(0)
