#!/usr/bin/python3

###########################################################
# A python script to capture HW resource usage in real time
# This is a client side script running with DUT in the same
# machine.
#
# Maintainer: Ivor
###########################################################
import argparse
import asyncio
import sys
import time

from Modules.Logging import setLogger


def parse_arguments():
    parser = argparse.ArgumentParser(description='Capture Respurce Usage')
    parser.add_argument("-pn", "--process-name", dest="procName", type=str,
                        required=True, help="provide process name")

    parser.add_argument("-pid", "--process-id", dest="pid", type=int,
                        required=False, help='specify a end time')

    parser.add_argument("interval", type=int,
                        help='specify interval')

    parser.add_argument("duration", type=int,
                        help='specify duraton for capturing')

    args = parser.parse_args()
    return args


async def metadata_populate():
    args = parse_arguments()
    _format='%(asctime)s - %(name)s:%(lineno)d - %(levelname)s - %(message)s'
    level='DEBUG'
    logger = setLogger(_format, level, 'logs', 20)
    logger.info("Start to run %s" % sys.argv)
    from Modules.CaptureSysResource import CaptureSysResource
    CSR=CaptureSysResource(args.interval)
    # Task1=asyncio.create_task(CSR.getCPUPercent())
    # Task2=asyncio.create_task(CSR.getPerCPUPercent())
    logger.info(time.time())
    # logger.info(await asyncio.gather(Task1,Task2))
    # # logger.info(time.time())
    # from concurrent import futures
    # with futures.ProcessPoolExecutor(max_workers=4) as executor:
    #     logger.info(time.time())
    #     task1=executor.submit(CSR.getCPUPercent())
    #     task2=executor.submit(CSR.getPerCPUPercent())
    #     futures.as_completed([task1,task2])
    #     logger.info(time.time())
    import math

    numItr=math.ceil(args.duration / args.interval)
    for _ in range(numItr):
        result=await CSR.getSysResourceUsage()
        logger.info(result)
    logger.info(time.time())



if __name__ == '__main__':
    asyncio.run(metadata_populate())
