import logging
import psutil

logger = logging.getLogger(__name__)


class CaptureSysResource(object):

    def __init__(self, interval):
        self._interval = interval

    async def getCPUPercent(self):
        # Blocking
        return psutil.cpu_percent(interval=self._interval)

    async def getPerCPUPercent(self):
        # non-blocking
        return psutil.cpu_percent(
            percpu=True
        )

    async def getIOCounters(self):
        return psutil.disk_io_counters()

    async def getSysResourceUsage(self):
        ioStats = psutil.disk_io_counters()
        (readCountPre, writeCoutPre,
         readBytesPre, writeBytesPre) = (
            ioStats.read_count,
            ioStats.write_count,
            ioStats.read_bytes,
            ioStats.write_bytes
        )
        await self.getPerCPUPercent()
        CPUPercent = await self.getCPUPercent()
        perCPUPercent = await self.getPerCPUPercent()
        ioStats = psutil.disk_io_counters()
        (readCount, writeCout,
         readBytes, writeBytes) = (
            ioStats.read_count,
            ioStats.write_count,
            ioStats.read_bytes,
            ioStats.write_bytes
        )
        (readCount, writeCout, readBytes, writeBytes) = (
            readCount - readCountPre,
            writeCout - writeCoutPre,
            readBytes - readBytesPre,
            writeBytes - writeBytesPre
        )
        retDict = dict()
        retDict['CPUPercent'] = CPUPercent
        for itr, value in enumerate(perCPUPercent):
            retDict['CPU%d' % itr] = perCPUPercent[itr]
        retDict['Disk Read OPs'] = readCount
        retDict['Disk Write OPs'] = writeCout
        retDict['Disk Read Bytes'] = readBytes
        retDict['Disk Write Bytes'] = writeBytes
        return retDict
