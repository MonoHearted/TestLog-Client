from __future__ import division
import logging

import psutil
import numpy
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

    def getSysResourceUsage(self, per_disk, per_nic):
        """
        To return Overall cpu usage, per CPU usage which are out of 100%.

        :param per_disk: Display usage per disk
        :param per_nic: Return usage per network interface card

        :return: A dict contains System HW Resource Usage
        """

        netIOPre = psutil.net_io_counters(per_nic)

        diskIOPre = psutil.disk_io_counters(per_disk)

        # discard the first set of perCPU usage data
        self.getOverallCPUPercentage()
        self.getPerCPUPercentage()
        # blocking for {interval}
        sleep(self._interval)

        # get overall CPU since last call
        CPUPercent = self.getOverallCPUPercentage()
        # get perCPU since last call
        perCPUPercent = self.getPerCPUPercentage()

        # define namedtuples
        ntDisk = namedtuple('ntDisk', 'read_count, write_count, read_bytes, write_bytes, read_time, '
                                      'write_time, busy_time, read_merged_count, write_merged_count')
        ntNIC = namedtuple('ntNIC', 'bytes_sent, bytes_recv, packets_sent, packets_recv, errin, errout, dropin, dropout')

        # calculate the difference within this interval
        netIO = psutil.net_io_counters(per_nic)
        if type(netIO) == dict and type(netIOPre) == dict:
            assert(netIO.keys() == netIOPre.keys()), "NICs differ during interval"
            for name, tup in netIO.items():
                if name.upper() == "LO":
                    continue
                tup = ntNIC(*tuple(numpy.subtract(tup, netIOPre[name])))
        else:
            netIO = ntNIC(*tuple(numpy.subtract(netIO, netIOPre)))

        diskIO = psutil.disk_io_counters(per_disk)
        if type(diskIO) == dict and type(diskIOPre) == dict:
            assert (diskIO.keys() == diskIOPre.keys()), "disks differ during interval"
            for name, tup in diskIO.items():
                tup = ntDisk(*tuple(numpy.subtract(tup, diskIOPre[name])))
        else:
            diskIO = ntDisk(*tuple(numpy.subtract(diskIO, diskIOPre)))

        if ('Linux' in self._OSPlatform):
            (memAvailBytes, memUsedPercentage,
             memBufferedBytes) = self.getMemStats()
        else:
            (memAvailBytes, memUsedPercentage) = self.getMemStats()

        retDict = dict()
        retDict['OVERALL CPU USED PERCENTAGE'] = CPUPercent
        for itr, value in enumerate(perCPUPercent):
            retDict['CPU%d USED PERCENTAGE' % itr] = perCPUPercent[itr]

        retDict['OVERALL MEMORY AVAILABLE BYTES'] = memAvailBytes
        retDict['OVERALL MEMORY USED PERCENTAGE'] = memUsedPercentage
        if ('Linux' in self._OSPlatform):
            retDict['OVERALL MEMORY BUFFERED BYTES'] = memBufferedBytes

        if per_disk:
            for name, tup in diskIO.items():
                retDict[name.upper() + ' READ OPS'] = tup.read_count
                retDict[name.upper() + ' WRITE OPS'] = tup.write_count
                retDict[name.upper() + ' READ BYTES'] = tup.read_bytes
                retDict[name.upper() + ' WRITE BYTES'] = tup.write_bytes
        else:
            retDict['OVERALL DISK READ OPS'] = diskIO.read_count
            retDict['OVERALL DISK WRITE OPS'] = diskIO.write_count
            retDict['OVERALL DISK READ BYTES'] = diskIO.read_bytes
            retDict['OVERALL DISK WRITE BYTES'] = diskIO.write_bytes

        if per_nic:
            for name, tup in netIO.items():
                retDict[name.upper() + ' SEND BYTES'] = tup.bytes_sent
                retDict[name.upper() + ' RECV BYTES'] = tup.bytes_recv
                retDict[name.upper() + ' INCOMING PACKETS DROPPED'] = tup.dropin
                retDict[name.upper() + ' OUTGOING PACKETS DROPPED'] = tup.dropout
        else:
            retDict['OVERALL NETWORK SEND BYTES'] = netIO.bytes_sent
            retDict['OVERALL NETWORK RECV BYTES'] = netIO.bytes_recv
            retDict['OVERALL INCOMING PACKETS DROPPED'] = netIO.dropin
            retDict['OVERALL OUTGOING PACKETS DROPPED'] = netIO.dropout

        return retDict
