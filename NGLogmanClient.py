import socket
import grpc
import time
import argparse
from contextlib import contextmanager

import nglm_grpc.nglm_pb2 as nglm_pb2
import nglm_grpc.nglm_pb2_grpc as nglm_pb2_grpc
from nglm_grpc.gRPCMethods import addToServer

from Modules.Utility import singletonThreadPool
from Modules.ConfigParser import cfgParser

from grpc._channel import _Rendezvous

def parse_arguments():
    parser = argparse.ArgumentParser(description='Establish NGLM gRPC Client-side')
    parser.add_argument("-c", "--config", dest="configFile", type=str,
                        default=None,
                        required=False, help='provide a configuration file')
    parser.add_argument("-ip", "--address", type=str, dest='address', required=False,
                        help='specify address and port (x.x.x.x:port) of NGLM gRPC Server-side')

    args = parser.parse_args()
    return args

def registerClient(address, hostingPort):
    channel = grpc.insecure_channel(address)

    stub = nglm_pb2_grpc.ServerStub(channel)
    hostName = socket.gethostname()
    hostIPv4 = socket.gethostbyname(hostName)

    clientInfo = nglm_pb2.clientInfo(hostname=hostName, ipv4=hostIPv4, port=hostingPort)
    try:
        response = stub.register(clientInfo)

        if not response.success:
            # server side register raised exception
            raise RuntimeError('Failed to register client.')
        logger.info('Connected to ' + address)
    except _Rendezvous:
        logger.error('Failed to connect. Retrying in 5s...')
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
    args = parse_arguments()
    logger, config = cfgParser(args, parseGRPCOnly=True)

    serverAddress = config.get('grpc', 'server_ip') + ':' + config.get('grpc', 'server_port')
    hostPort = config.get('grpc', 'host_port')

    registerClient(serverAddress, int(hostPort))
    with createServer(hostPort):
        logger.info('gRPC Server now listening on port ' + hostPort)
        try:
            while True:
                time.sleep(86400)
        except KeyboardInterrupt:
            pass
