from __future__ import division
import logging

import psutil
from collections import namedtuple
from time import sleep
import platform

logger = logging.getLogger(__name__)


def sysResourceTuple(fieldsList):
    return namedtuple("SystemResource", fieldsList)


class CaptureSysResource(object):
    """
    A thread based object, constructor requires a param interval
    Periodically captures resource usage and serialize data into a pickle file
    """

    def __init__(self, interval):
        self._interval = interval
        self._OSPlatform = platform.system()

    def getOverallCPUPercentage(self):
        """
        Get overall CPU usage out of 100
        :return: CPU percentage
        """
        # Blocking
        return psutil.cpu_percent()

    def getPerCPUPercentage(self):
        """
        Get each CPU usage out of 100
        :return: A list of all CPU percentage
        """
        # non-blocking
        return psutil.cpu_percent(
            percpu=True
        )

    def getIOCounters(self):
        ioStats = psutil.disk_io_counters()
        (readCount, writeCout,
         readBytes, writeBytes) = (
            ioStats.read_count,
            ioStats.write_count,
            ioStats.read_bytes,
            ioStats.write_bytes
        )
        return (readCount, writeCout, readBytes, writeBytes)

    def getNetIOCounter(self):
        netIOStats = psutil.net_io_counters()
        (bytesSent, bytesRecv,
         dropIn, dropOut) = (
            netIOStats.bytes_sent,
            netIOStats.bytes_recv,
            netIOStats.dropin,
            netIOStats.dropout
        )
        return (bytesSent, bytesRecv, dropIn, dropOut)

    def getMemStats(self):
        memStats = psutil.virtual_memory()
        (memAvail, memUsedPerc) = (
            memStats.available,
            memStats.percent
        )

        if ('Linux' in self._OSPlatform):
            memBuffered = memStats.buffers
            return (memAvail, memUsedPerc, memBuffered)

        return (memAvail, memUsedPerc)

    def getSysResourceUsage(self):
        """
        To return Overall cpu usage, per CPU usage which are out of 100%.

        :return: A dict contains System HW Resource Usage
        """
        (bytesSentPre, bytesRecvPre,
         dropInPre, dropOutPre) = self.getNetIOCounter()

        (readCountPre, writeCoutPre,
         readBytesPre, writeBytesPre) = self.getIOCounters()

        # discard the first set of perCPU usage data
        self.getOverallCPUPercentage()
        self.getPerCPUPercentage()
        # blocking for {interval}
        sleep(self._interval)

        # get overall CPU since last call
        CPUPercent = self.getOverallCPUPercentage()
        # get perCPU since last call
        perCPUPercent = self.getPerCPUPercentage()

        (readCount, writeCout,
         readBytes, writeBytes) = self.getIOCounters()

        # calculate the difference within this interval
        (readCount, writeCout, readBytes, writeBytes) = (
            readCount - readCountPre,
            writeCout - writeCoutPre,
            readBytes - readBytesPre,
            writeBytes - writeBytesPre
        )
        (bytesSent, bytesRecv,
         dropIn, dropOut) = self.getNetIOCounter()

        (bytesSent, bytesRecv,
         dropIn, dropOut) = (
            bytesSent - bytesSentPre,
            bytesRecv - bytesRecvPre,
            dropIn - dropInPre,
            dropOut - dropOutPre
        )
        if ('Linux' in self._OSPlatform):
            (memAvailBytes, memUsedPercentage,
             memBufferedBytes) = self.getMemStats()
        else:
            (memAvailBytes, memUsedPercentage) = self.getMemStats()

        retDict = dict()
        retDict['OVERALL CPU USED PERCENTAGE'] = CPUPercent
        for itr, value in enumerate(perCPUPercent):
            retDict['CPU%d USED PERCENTAGE' % itr] = perCPUPercent[itr]
        retDict['OVERALL DISK READ OPS'] = readCount
        retDict['OVERALL DISK WRITE OPS'] = writeCout
        retDict['OVERALL DISK READ BYTES'] = readBytes
        retDict['OVERALL DISK WRITE BYTES'] = writeBytes
        retDict['OVERALL NETWORK SEND BYTES'] = bytesSent
        retDict['OVERALL NETWORK RECV BYTES'] = bytesRecv
        retDict['OVERALL INCOMING PACKETS DROPPED'] = dropIn
        retDict['OVERALL OUTGOING PACKETS DROPPED'] = dropOut
        retDict['OVERALL MEMORY AVAILABLE BYTES'] = memAvailBytes
        retDict['OVERALL MEMORY USED PERCENTAGE'] = memUsedPercentage
        if ('Linux' in self._OSPlatform):
            retDict['OVERALL MEMORY BUFFERED BYTES'] = memBufferedBytes
        return retDict
