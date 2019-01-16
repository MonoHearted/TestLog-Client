from . import nglm_pb2
from . import nglm_pb2_grpc


class ServerServicer(nglm_pb2_grpc.ServerServicer):
    def register(self, request, context):
        pass

def addToServer(server):
    # Adds services to server, called on server start
    nglm_pb2_grpc.add_ServerServicer_to_server(ServerServicer(), server)

