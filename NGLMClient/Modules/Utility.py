from __future__ import division
import logging
from concurrent.futures.thread import ThreadPoolExecutor
from functools import wraps
from Modules.ConfigParser import cfgParser

logger = logging.getLogger(__name__)

Units = ['BYTES', 'KB', 'MB', 'GB', 'TB']
MUL = [1, 1 << 10, 1 << 20, 1 << 30, 1 << 40]


def convertBytesTo(unit):
    if (not unit in Units):
        raise ValueError("Invalid unit <%s>" % unit)
    index = Units.index(unit)
    multiple = MUL[index]

    def setUnitDecorator(f):
        @wraps(f)
        def funcWrapper(*args, **kwargs):
            logger.debug("Ready to set unit to <%s>" % unit)
            result =f(*args, **kwargs)
            retDict = dict()
            if (not isinstance(result, dict)):
                raise ValueError("Invalid type for returned result")
            for key, value in result.items():
                if (not isinstance(key, str)):
                    raise ValueError("Invalid type for key name, str expected")
                if ('BYTES' in key.upper()):
                    try:
                        if(isinstance(value, list)):
                            value[:]=[int(x) / multiple for x in value]
                        else:
                            value = int(value) / multiple
                    except:
                        raise ValueError("Invalid type for value, "
                                         "str formatted integer is expected")
                    key = key.upper().replace('BYTES', unit)
                    retDict[key] = value
                else:
                    retDict[key] = value
            return retDict

        return funcWrapper

    return setUnitDecorator


class Singleton(type):
    def __init__(self, *args, **kwargs):
        self.__instance = None
        super().__init__(*args, **kwargs)

    def __call__(self, *args, reset=False, **kwargs):
        if reset:
            self.__instance = None
        if self.__instance is None:
            self.__instance = super().__call__(*args, **kwargs)
            return self.__instance
        else:
            return self.__instance

# class Config(metaclass=Singleton):
#     def __init__(self, argParser):
#         tup = cfgParser(argParser)
#         self.__logger = tup[0]
#         self.__cfg = tup[1]
#
#     def getLogger(self):
#         return self.__logger
#
#     def __getattr__(self, attr):
#         return getattr(self.__cfg, attr)

class singletonThreadPool(ThreadPoolExecutor,metaclass=Singleton):
    """
    Create a singleton class which wrap a threadpool object
    """
    pass