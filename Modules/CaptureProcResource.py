import logging
from psutil import process_iter, NoSuchProcess
from psutil import _exceptions as PSExceptions
import platform, os

logger = logging.getLogger(__name__)


class CaptureProcResource(object):

    def __init__(self, pid, pName):
        self._pid = pid
        self._pName = pName
        self._processes = list()
        self._OSPlatform = platform.system()
        self._currentProcPid=os.getpid()
        logger.info("This process's pid is %d\n\n\n" % self._currentProcPid)
        if (pid is not None):
            self.initProcessObjectWithPid()
        else:
            self.initProcessObjectWithPname(self._pName)

    @property
    def processes(self):
        return self._processes

    def __str__(self):
        for proc in self._processes:
            logger.info(proc.info)

    def initProcessObjectWithPid(self):
        """
        Pid is provided. Two cases need to handle
        1. Pname provide, attach one process or throw NoSuchProcess
        2. Pname not provide, attach one process
        :return:
        """
        attrList = ['pid', 'name']
        for proc in process_iter(attrs=attrList):
            # logger.debug(proc.info)
            if (proc.info['pid'] == self._pid):
                if (self._pName and self._pName in ' '.join(
                        proc.cmdline()).lower()):
                    # Pid and Pname are both provided
                    #  only one process should be attached
                    self._processes.append(proc)
                elif (not self._pName):
                    # Pname not provide
                    self._pName = proc.info['name']
                    logger.debug('Adding this process')
                    logger.debug(proc.info)
                    self._processes.append(proc)
                else:
                    raise NoSuchProcess(pid=self._pid,
                                        name=self._pName)
                # if pid is provided, find the proc and break immediately
                break

    def initProcessObjectWithPname(self, pName):
        attrList = ['pid', 'name']
        for proc in process_iter(attrs=attrList):
            try:
                if (pName.lower() in ' '.join(proc.cmdline()).lower() and
                    proc.pid != self._currentProcPid):
                        logger.debug('Adding this process')
                        logger.debug(proc.info)
                        self._processes.append(proc)
            except PSExceptions.AccessDenied:
                pass
        if (len(self._processes) < 1):
            raise NoSuchProcess(pid=self._pid, name=self._pName)

    def getProcessesStats(self, aggregate):
        logger.debug("enter")
        retDict = dict()

        if aggregate:
            for proc in self._processes:
                try:
                    with proc.oneshot():
                        key = "%s CPU USED PERCENTAGE" % self._pName
                        if key not in retDict:
                            retDict[key] = 0
                        retDict[key] += proc.cpu_percent()

                        if ('Linux' in self._OSPlatform):
                            key = "%s FILE DESCRIPTORS OPENED" % self._pName
                            if key not in retDict:
                                retDict[key] = 0
                            retDict[key] = proc.num_fds()
                        else:
                            key = "%s HANDLES USED" % self._pName
                            if key not in retDict:
                                retDict[key] = 0
                            retDict[key] += proc.num_handles()

                        key = "%s THREADS USED" % self._pName
                        if key not in retDict:
                            retDict[key] = 0
                        retDict[key] += proc.num_threads()
                except NoSuchProcess:
                    pass
        else:
            for proc in self._processes:
                try:
                    with proc.oneshot():
                        key = "%s %d CPU USED PERCENTAGE" % (self._pName,
                                                             proc.info['pid'])
                        retDict[key] = proc.cpu_percent()

                        if ('Linux' in self._OSPlatform):
                            key = "%s %d FILE DESCRIPTORS OPENED" % (
                                self._pName,
                                proc.info['pid'])
                            retDict[key] = proc.num_fds()
                        else:
                            key = "%s %d HANDLES USED" % (self._pName,
                                                          proc.info['pid'])
                            retDict[key] = proc.num_handles()

                        key = "%s %d THREADS USED" % (self._pName,
                                                      proc.info['pid'])
                        retDict[key] = proc.num_threads()
                except NoSuchProcess:
                    pass
        return retDict
