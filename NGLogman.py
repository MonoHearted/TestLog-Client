#!/usr/bin/python3

###########################################################
# A python script to capture HW resource usage in real time
# This is a client side script running with DUT in the same
# machine.
#
# Todo:
# Run it in a sever mode, restful web server
# or a gRPC server(Preferred),
# Create thread pool for CaptureSysResource and
# CaptureProcResource
#
# instantiate a CaptureSysResource obj and
# a CaptureProcResource obj for each request
#
# instantiate a Retention manager obj to purge data older
# than a specific age
#
# Maintainer: Ivor
###########################################################

import argparse
import sys
import datetime
import time

from Modules.ConfigParser import cfgParser


def parse_arguments():
    parser = argparse.ArgumentParser(description='Capture Resource Usage')
    parser.add_argument("-pn", "--process-name", dest="procName", type=str,
                        default=None,
                        required=False, help="provide process name")

    parser.add_argument("-pid", "--process-id", dest="pid", type=int,
                        default=None,
                        required=False, help='specify a end time')

    parser.add_argument("-c", "--config", dest="configFile", type=str,
                        default=None,
                        required=False, help='provide a configuration file')

    parser.add_argument("interval", type=int,
                        help='specify interval')

    parser.add_argument("duration", type=int,
                        help='specify duration for capturing')

    args = parser.parse_args()
    return args


def main():
    args = parse_arguments()
    logger, config = cfgParser(args)

    logger.info("Beginning execution of %s" % sys.argv)

    import math
    numItr = int(math.ceil(args.duration / args.interval))
    from Modules.TaskManager import createTask
    from Modules.Utility import singletonThreadPool
    executor = singletonThreadPool(max_workers=config.getint('workers','pool'))
    createTask(numItr, args.interval, config, datetime.datetime.now().isoformat(), executor=executor)

    logger.info(time.time())

if __name__ == '__main__':
    main()
