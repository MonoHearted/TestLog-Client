import logging
import time
import pandas as pd
from pandas import DataFrame as df
from concurrent.futures import as_completed
import os,sys
from Client_Side.Modules.Utility import convertBytesTo

logger = logging.getLogger(__name__)


def createTask(Itr, Interval, config, startTime, executor=None):
    procName = config['proc_info'].get('process_name')
    pid = config['proc_info'].get('pid')

    logger.info("Starting Task @ {}".format(time.time()))
    from Client_Side.Modules.CaptureSysResource import CaptureSysResource
    CSR = CaptureSysResource(Interval)

    from Client_Side.Modules.CaptureProcResource import CaptureProcResource
    CPR = CaptureProcResource(pid, procName)

    CJR = None
    if config.getboolean('proc_info', 'is_java_process'):
        from Client_Side.Modules.CaptureJVMResource import CaptureJVMResource
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

    @convertBytesTo(unit=config.get('data', 'unit'))
    def runPerItr():
        res = dict()
        res['Time'] = pd.datetime.now().time()
        try:
            # these two metric can be captured in real time
            is_per_disk = config.getboolean('system_info', 'per_disk')
            is_per_nic = config.getboolean('system_info', 'per_nic')
            futures.append(executor.submit(CSR.getSysResourceUsage, is_per_disk, is_per_nic))

            is_aggregate = config.getboolean('proc_info', 'aggregate_data')
            futures.append(executor.submit(CPR.getProcessesStats, is_aggregate))

            # run jvmtop
            # jvmResult=CJR.startJob(Itr)
            # result.update(jvmResult)
            for task in as_completed(futures):
                logger.info(task.result())
                res.update(task.result())
        except Exception as e:
            raise e
        logger.debug(res)
        return res

    summaryDF = None
    if(CJR is not None):
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
    else:
        for _ in range(Itr):
            if (summaryDF is None):
                firstRow = runPerItr()
                firstRowData = tuple(firstRow.values())
                summaryDF = df([firstRowData],
                               columns=list(firstRow.keys())
                               )
                logger.info("Summary is:\n{}".format(summaryDF))
                continue
            retRow = runPerItr()
            logger.debug(retRow)
            summaryDF = summaryDF.append(retRow, ignore_index=True)

    logger.debug(summaryDF.dtypes)
    logger.debug("Summary is:\n{}".format(summaryDF))

    percentiles = config['data'].get('percentile')
    if bool(percentiles):
        percentiles = percentiles.split(',')
        logger.debug("Calculating percentile...")

        for percentile in percentiles:
            percentile = float(percentile)
            percentileDict = summaryDF.quantile(percentile, numeric_only=True).to_dict()
            percentileDict['Time'] = '%dth Percentile' % (percentile * 100)
            logger.debug("Percentile is: \n{}".format(percentileDict))

            # Adding this row back to summaryDF
            summaryDF = summaryDF.append(percentileDict, ignore_index=True)
        logger.debug("Summary is:\n{}".format(summaryDF))

    if config.getboolean('data', 'average') is True:
        # same as above, but for mean
        logger.debug("Calculating average...")

        averageDict = summaryDF.iloc[:-1].mean(numeric_only=True).to_dict()
        averageDict['Time'] = 'Mean'
        logger.debug('Averages are: \n{}'.format(averageDict))

        summaryDF = summaryDF.append(averageDict, ignore_index=True)
        logger.debug("Summary is:\n{}".format(summaryDF))

    if config.getboolean('data', 'max') is True:
        # same as above, but for mean
        logger.debug("Calculating maxima...")

        averageDict = summaryDF.iloc[:-2].max(numeric_only=True).to_dict()
        averageDict['Time'] = 'Max'
        logger.debug('Maxima are: \n{}'.format(averageDict))

        summaryDF = summaryDF.append(averageDict, ignore_index=True)
        logger.debug("Summary is:\n{}".format(summaryDF))

    if config.getboolean('data', 'min') is True:
        # same as above, but for mean
        logger.debug("Calculating minima...")

        averageDict = summaryDF.iloc[:-3].min(numeric_only=True).to_dict()
        averageDict['Time'] = 'Min'
        logger.debug('Minima are: \n{}'.format(averageDict))

        summaryDF = summaryDF.append(averageDict, ignore_index=True)
        logger.debug("Summary is:\n{}".format(summaryDF))

    summaryDF.to_excel(os.path.join(
        os.path.dirname(sys.modules['__main__'].__file__),
        "Output",
        CPR._pName + '_' + startTime.replace(':', '-').replace('.', '_') + '_result.xls'
    ), index=False)
