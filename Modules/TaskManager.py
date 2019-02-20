import logging
import time
import pandas as pd
from pandas import DataFrame as df
from concurrent.futures import as_completed
import os
import sys
from Modules.Utility import convertBytesTo

logger = logging.getLogger(__name__)


def createTask(Itr, Config, Interval, startTime, executor=None):
    """
    :param Itr:
    :param Interval:
    :param config:
    :param startTime:
    :param executor:
    :return: filePath
    """

    procName = Config.get('proc_info', 'process_name')
    pid = Config.get('proc_info', 'pid') or None

    logger.info("Starting Task @ {}".format(time.time()))
    from Modules.CaptureSysResource import CaptureSysResource
    CSR = CaptureSysResource(Interval)

    from Modules.CaptureProcResource import CaptureProcResource
    CPR = CaptureProcResource(pid, procName)

    CJR = None
    if Config.getboolean('proc_info', 'is_java_process'):
        from Modules.CaptureJVMResource import CaptureJVMResource
        if(Config.get('proc_info', 'java_home', fallback=None) is None or
                Config.get('proc_info', 'java_home', fallback=None) is ''):
            raise ValueError("Invalid value for java_home")

        if (len(CPR.processes) == 1):
            javaPid = CPR.processes[0].info['pid']
            CJR = CaptureJVMResource(Config.get('proc_info', 'java_home'),
                                     Interval, javaPid)
        else:
            logger.error("More than one Java process found")
            sys.exit(1)
    futures = []

    @convertBytesTo(unit=Config.get('data', 'unit'))
    def runPerItr():
        res = dict()
        res['Time'] = pd.datetime.now().time()
        try:
            # these two metric can be captured in real time
            is_per_disk = Config.getboolean('system_info', 'per_disk')
            is_per_nic = Config.getboolean('system_info', 'per_nic')
            futures.append(executor.submit(CSR.getSysResourceUsage,
                                           is_per_disk, is_per_nic))

            is_aggregate = Config.getboolean('proc_info', 'aggregate_data')
            futures.append(executor.submit(CPR.getProcessesStats,
                                           is_aggregate))

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
    if CJR is not None:
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

    percentiles = Config['data'].get('percentile')
    excl = 0
    row_count = len(summaryDF.index)

    if Config.getfloat('data', 'leading_trim_percent') > 0:
        trim_frac = Config.getfloat('data', 'leading_trim_percent') / 100
        to_trim = round(trim_frac * row_count)
        summaryDF = summaryDF[to_trim:]
        logger.debug('Trimmed %d leading rows.' % to_trim)

    if Config.getfloat('data', 'trailing_trim_percent') > 0:
        trim_frac = Config.getfloat('data', 'trailing_trim_percent') / 100
        to_trim = round(trim_frac * row_count)
        end_index = row_count - to_trim
        summaryDF = summaryDF[:end_index]
        logger.debug('Trimmed %d trailing rows.' % to_trim)

    if bool(percentiles):
        percentiles = percentiles.split(',')
        logger.debug("Calculating percentile...")

        for percentile in percentiles:
            percentile = float(percentile)
            percentileDict = summaryDF.quantile(percentile, numeric_only=True)\
                .to_dict()
            percentileDict['Time'] = '%dth Percentile' % (percentile * 100)
            logger.debug("Percentile is: \n{}".format(percentileDict))

            # Adding this row back to summaryDF
            summaryDF = summaryDF.append(percentileDict, ignore_index=True)
        logger.debug("Summary is:\n{}".format(summaryDF))
        excl += len(percentiles)

    if Config.getboolean('data', 'average') is True:
        # same as above, but for mean
        logger.debug("Calculating average...")

        averageDict = summaryDF.iloc[:-excl].mean(numeric_only=True).to_dict()
        averageDict['Time'] = 'Mean'
        logger.debug('Averages are: \n{}'.format(averageDict))

        summaryDF = summaryDF.append(averageDict, ignore_index=True)
        logger.debug("Summary is:\n{}".format(summaryDF))
        excl += 1

    if Config.getboolean('data', 'max') is True:
        # same as above, but for mean
        logger.debug("Calculating maxima...")

        averageDict = summaryDF.iloc[:-excl].max(numeric_only=True).to_dict()
        averageDict['Time'] = 'Max'
        logger.debug('Maxima are: \n{}'.format(averageDict))

        summaryDF = summaryDF.append(averageDict, ignore_index=True)
        logger.debug("Summary is:\n{}".format(summaryDF))
        excl += 1

    if Config.getboolean('data', 'min') is True:
        # same as above, but for mean
        logger.debug("Calculating minima...")

        averageDict = summaryDF.iloc[:-excl].min(numeric_only=True).to_dict()
        averageDict['Time'] = 'Min'
        logger.debug('Minima are: \n{}'.format(averageDict))

        summaryDF = summaryDF.append(averageDict, ignore_index=True)
        logger.debug("Summary is:\n{}".format(summaryDF))
        excl += 1

    filePath = CPR._pName + '_' + startTime.replace(':', '-')\
        .replace('.', '_') + '_result.xlsx'
    summaryDF.to_excel(os.path.join(
        os.path.dirname(sys.modules['__main__'].__file__),
        "Output", filePath
    ), index=False, engine="openpyxl")

    return filePath
