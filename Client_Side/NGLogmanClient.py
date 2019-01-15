import socket
import grpc
from concurrent import futures

import nglm_grpc.nglm_pb2 as nglm_pb2
import nglm_grpc.nglm_pb2_grpc as nglm_pb2_grpc

channel = grpc.insecure_channel('localhost:50051')

stub = nglm_pb2_grpc.ClientStub(channel)
hostName = socket.gethostname()
hostIPv4 = socket.gethostbyname(hostName)

clientInfo = nglm_pb2.clientInfo(hostname=hostName, ipv4=hostIPv4)
response = stub.register(clientInfo)

if not response.success:
    raise RuntimeError('Failed to register client.')

# TODO: create gRPC server listener here to call main()