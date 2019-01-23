from . import nglm_pb2
from . import nglm_pb2_grpc
import os, sys


class ServerServicer(nglm_pb2_grpc.ServerServicer):
    def isAlive(self, request, context):
        res = nglm_pb2.response()
        res.success = True
        return res


class LoggingServicer(nglm_pb2_grpc.LoggingServicer):
    def start(self, request, context):
        try:
            from NGLogmanClient import logMain
            filePath = os.path.join(
                os.path.dirname(sys.modules['__main__'].__file__),
                "Output", logMain(params=request))
            return getChunks(filePath)
        except:
            raise

    def getConfig(self, request, context):
        try:
            configPath = os.path.join(
                os.path.dirname(sys.modules['__main__'].__file__),
                "config", "logman.ini")
            return getChunks(configPath)
        except:
            raise


def getChunks(path):
    with open(path, 'rb') as f:
        while True:
            chunk = f.read(1024)
            if len(chunk) == 0:
                return
            yield nglm_pb2.chunks(buffer=chunk)


def addToServer(server):
    # Adds services to server, called on server start
    nglm_pb2_grpc.add_ServerServicer_to_server(ServerServicer(), server)
    nglm_pb2_grpc.add_LoggingServicer_to_server(LoggingServicer(), server)

