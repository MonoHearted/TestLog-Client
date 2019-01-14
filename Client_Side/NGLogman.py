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
import time

from Modules.Logging import setLogger


def parse_arguments():
    parser = argparse.ArgumentParser(description='Capture Respurce Usage')
    parser.add_argument("-pn", "--process-name", dest="procName", type=str,
                        default=None,
                        required=False, help="provide process name")

    parser.add_argument("-pid", "--process-id", dest="pid", type=int,
                        default=None,
                        required=False, help='specify a end time')

    parser.add_argument("interval", type=int,
                        help='specify interval')

    parser.add_argument("duration", type=int,
                        help='specify duraton for capturing')

    args = parser.parse_args()
    return args


def main():
    args = parse_arguments()
    _format = '%(asctime)s - %(name)s:%(lineno)d - %(levelname)s - %(message)s'
    level = 'DEBUG'
    logger = setLogger(_format, level, 'logs', 20)
    logger.info("Start to run %s" % sys.argv)

    import math
    numItr = int(math.ceil(args.duration / args.interval))
    from Modules.TaskManager import createTask
    from concurrent.futures import ThreadPoolExecutor
    executor = ThreadPoolExecutor(max_workers=3)
    createTask(numItr, 'KB', args.interval, procName=args.procName,
               pid=args.pid,
               executor=executor)

    logger.info(time.time())


if __name__ == '__main__':
    main()
