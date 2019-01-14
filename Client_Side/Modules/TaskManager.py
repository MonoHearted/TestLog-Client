import logging
import time
import pandas as pd
from pandas import DataFrame as df
from concurrent.futures import as_completed
import os, sys
from Modules.Utility import convertBytesTo

logger = logging.getLogger(__name__)


def createTask(Itr, Unit, Interval, procName=None, pid=None, executor=None):
    logger.info("Starting Task @ {}".format(time.time()))
    from Modules.CaptureSysResource import CaptureSysResource
    CSR = CaptureSysResource(Interval)

    from Modules.CaptureProcResource import CaptureProcResource
    CPR = CaptureProcResource(pid, procName)

    # todo
    # to capture java process enable this
    # read the config from config file
    from Modules.CaptureJVMResource import CaptureJVMResource
    # todo
    # read the JAVA_HOME from config file and pass it to CaptureJVMResource
    # constructor
    if (len(CPR.processes) == 1):
        javaPid = CPR.processes[0].info['pid']
        CJR = CaptureJVMResource("/usr/java/latest/", Interval, javaPid)
    else:
        logger.error("More than one Java process found")
        sys.exit(1)
    futures = []

    # TODO
    # Read from config file and set the unit here
    @convertBytesTo(unit=Unit)
    def runPerItr():
        result = dict()
        result['Time'] = pd.datetime.now().time()
        try:
            # these two metric can be captured in real time
            futures.append(executor.submit(CSR.getSysResourceUsage))
            futures.append(executor.submit(CPR.getProcessesStats))
            # run jvmtop
            # jvmResult=CJR.startJob(Itr)
            # result.update(jvmResult)
            for task in as_completed(futures):
                logger.info(task.result())
                result.update(task.result())
        except Exception as e:
            raise e
        logger.debug(result)
        return result

    summaryDF = None
    for jvmResult in CJR.startJob(Itr):
        if (summaryDF is None):
            firstRow = runPerItr()
            firstRow.update(jvmResult)
            firstRowData = tuple(firstRow.values())
            summaryDF = df([firstRowData],
                           columns=list(firstRow.keys())
                           )
            logger.info("Summary is:\n{}".format(summaryDF))
            continue
        retRow = runPerItr()
        retRow.update(jvmResult)
        logger.debug(retRow)
        summaryDF = summaryDF.append(retRow, ignore_index=True)

    logger.debug(summaryDF.dtypes)
    logger.debug("Summary is:\n{}".format(summaryDF))

    logger.debug("Calculating percentle...")

    percentle = 0.95
    percentleDict = summaryDF.quantile(percentle, numeric_only=True).to_dict()
    percentleDict['Time'] = '%dth Percentle' % (percentle * 100)
    logger.debug("Percentle is: \n{}".format(percentleDict))

    # Adding this row back to summaryDF
    summaryDF = summaryDF.append(percentleDict, ignore_index=True)
    logger.debug("Summary is:\n{}".format(summaryDF))
    summaryDF.to_excel(os.path.join(
        os.path.dirname(sys.modules['__main__'].__file__),
        "Output",
        "result.xls"
    ), index=False)
