import socket
import grpc
import time
import datetime
import argparse
import sys
from contextlib import contextmanager

import nglm_grpc.nglm_pb2 as nglm_pb2
import nglm_grpc.nglm_pb2_grpc as nglm_pb2_grpc
from nglm_grpc.gRPCMethods import addToServer
from grpc._channel import _Rendezvous

from Modules.Utility import singletonThreadPool
from Modules.ConfigParser import cfgParser


def parse_arguments():
    parser = argparse.ArgumentParser(description='Capture Resource Usage')

    parser.add_argument("-c", "--config", dest="configFile", type=str,
                        default=None,
                        required=False, help='provide a configuration file')

    parser.add_argument("-s", "--server", action='store_true',
                        help='run NGLogman in gRPC mode, may specify address')

    parser.add_argument('-ip', '--address', type=str, dest='address',
                        required=False, default=None,
                        help='specify server address&port (x.x.x.x:port)')

    if '-s' not in sys.argv and '--server' not in sys.argv:
        parser.add_argument("interval", type=int, help='specify interval')

        parser.add_argument("duration", type=int,
                            help='specify duration for capturing')

        parser.add_argument("-pn", "--process-name", dest="procName", type=str,
                            default=None,
                            required=False, help="provide process name")

        parser.add_argument("-pid", "--process-id", dest="pid", type=int,
                            default=None,
                            required=False, help='specify a end time')

    args = parser.parse_args()
    return args


def logMain(params=None):
    args = parse_arguments()

    if params is not None:
        # grpc parameter overwrites
        (args.pid, args.procName) = (params.pid, params.pname)
        (args.interval, args.duration) = (params.interval, params.duration)

    logger, config = cfgParser(args)

    logger.info("Beginning execution of %s" % sys.argv)

    import math
    numItr = int(math.ceil(args.duration / args.interval))
    from Modules.TaskManager import createTask
    executor = singletonThreadPool(max_workers=config
                                   .getint('workers', 'pool'))
    logger.info(time.time())
    return createTask(numItr, args.interval, config, datetime.datetime.now()
                      .isoformat(), executor=executor)


def checkConnection(address, hostingPort):
    try:
        channel = grpc.insecure_channel(address)
        nglm_pb2_grpc.ServerStub(channel).isAlive(nglm_pb2.query(query=''))
        channel.close()
    except _Rendezvous:
        logger.error('Server connection dropped.')
        registerClient(address, hostingPort)


def registerClient(address, hostingPort):
    channel = grpc.insecure_channel(address)
    stub = nglm_pb2_grpc.ServerStub(channel)

    import netifaces as ni
    hostName = socket.gethostname()
    hostIPv4 = socket.gethostbyname(hostName) # ni.ifaddresses('eth0')[ni.AF_INET][0]['addr']

    clientInfo = nglm_pb2.clientInfo(hostname=hostName, ipv4=hostIPv4,
                                     port=hostingPort)
    try:
        response = stub.register(clientInfo)

        if not response.success:
            # server side register raised exception
            raise RuntimeError('Failed to register client.')
        logger.info('Connected to ' + address)
    except _Rendezvous:
        logger.error('Failed to connect. Retrying in 5s...')
        channel.close()
        time.sleep(5)
        registerClient(address, hostingPort)

    channel.close()


@contextmanager
def createServer(port):
    from concurrent import futures
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    addToServer(server)
    server.add_insecure_port('[::]:' + port)
    server.start()
    yield
    server.stop(0)


if __name__ == '__main__':
    if '-s' in sys.argv or '--server' in sys.argv:
        args = parse_arguments()
        logger, grpcConfig = cfgParser(args)

        serverAddress = grpcConfig.get('grpc', 'server_ip') + ':' + \
            grpcConfig.get('grpc', 'server_port')
        hostPort = grpcConfig.get('grpc', 'host_port')

        registerClient(serverAddress, int(hostPort))
        with createServer(hostPort):
            logger.info('gRPC Server now listening on port ' + hostPort)
            try:
                while True:
                    time.sleep(5)
                    checkConnection(serverAddress, int(hostPort))
            except KeyboardInterrupt:
                pass
    else:
        logMain()
