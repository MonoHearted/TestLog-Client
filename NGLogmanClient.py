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

def parse_arguments():
    parser = argparse.ArgumentParser(description='Establish NGLM gRPC Client-side')
    parser.add_argument("-c", "--config", dest="configFile", type=str,
                        default=None,
                        required=False, help='provide a configuration file')
    parser.add_argument("-ip", "--address", type=str, dest='address', required=False,
                        help='specify address and port (x.x.x.x:port) of NGLM gRPC Server-side')

    args = parser.parse_args()
    return args

def registerClient(address):
    channel = grpc.insecure_channel(address)

    stub = nglm_pb2_grpc.ServerStub(channel)
    hostName = socket.gethostname()
    hostIPv4 = socket.gethostbyname(hostName)

    clientInfo = nglm_pb2.clientInfo(hostname=hostName, ipv4=hostIPv4)
    response = stub.register(clientInfo)

    if not response.success:
        raise RuntimeError('Failed to register client.')


@contextmanager
def createServer(port):
    server = grpc.server(singletonThreadPool(max_workers=10))

    addToServer(server)
    server.add_insecure_port('[::]:' + port)
    server.start()
    yield
    server.stop(0)


if __name__ == '__main__':
    args = parse_arguments()
    logger, config = cfgParser(args, parseGRPCOnly=True)

    serverAddress = config.get('grpc', 'server_ip') + ':' + config.get('grpc', 'server_port')
    registerClient(serverAddress)

    hostPort = config.get('grpc', 'host_port')
    with createServer(hostPort):
        print('gRPC Server now listening on port ' + hostPort)
        try:
            while True:
                time.sleep(86400)
        except KeyboardInterrupt:
            pass
