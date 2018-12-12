# ------------------------------------------------------
# A module to setup logging
# Set logging format and handler
# Set log rotation
# ------------------------------------------------------
import logging, logging.handlers, logging.config
import time
from logging.handlers import RotatingFileHandler


def setLogger(format, level, path, rotateSize):
    """
    read from config and setup root logger
    :param format: logging format
    :param level: default log level
    :param path: path to save log file
    :param rotateSize: max size for log rotation
    :return: root logger, used by main module
    """
    # check whether format string is valid
    try:
        formatter = logging.Formatter(format)
    except Exception as ex:
        assert type(format) is str, "Provided log format is not a string"
        assert True, "Fail to use logging format %s" % format
        raise ex

    # set log level and logging messages format
    numeric_level = getattr(logging, level.upper(), None)
    LOGFILE_PATH = "%s/NGLM_%s.log" % \
                   (path,
                    time.strftime("%m%d%y_%H%M%S",
                                  time.localtime(time.time())))


    # set log rotation handler
    # set rotate size to 10 MB and keep up
    # to 30 log files to avoid out of space issue

    rotateSize = 1000000 * rotateSize
    logRotateHandler = RotatingFileHandler(
        LOGFILE_PATH, maxBytes=rotateSize, backupCount=30)

    # # set console handler
    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(formatter)

    logging.basicConfig(format=format,
                        level=numeric_level,
                        handlers=[logRotateHandler,
                                  consoleHandler])

    # get root logger
    rootlogger = logging.getLogger("Main")

    return rootlogger
