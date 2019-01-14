import configparser
import logging
from pathlib import Path

from .Logging import setLogger


def setSectionForConfigParser(section, configSection, config):
    """
    Setup config for logging section
    :param section: section name
    :param configSection: a dictionary for default config value
    :param config: configparser object
    :return: NA
    """
    # logger is not ready yet, use assertion instead
    assert section in config, "Can't find %s in config file" % (section)
    for key in configSection:
        retOpt = config[section].get(key, configSection[key])
        if (retOpt is ''):
            config.set(section, key, configSection[key])
        else:
            config.set(section, key,
                       config[section].get(key, configSection[key]))


def cfgParser(argParser):
    """
    load config file passed by cmdline arguments
    argument from cmdline will override
    config red from config file
    :param argParser: the argument parser object
    :return: the final cfgparser object including all configs
                red from cmdline and config file
             the root logger
    """
    # get local logger
    logger = logging.getLogger(__name__)

    # Load the configuration file
    config = configparser.RawConfigParser(allow_no_value=True)
    if argParser.configFile is None:
        logger.info('No config provided, generating default')
        defaultPath = Path('config/logman.ini')
        argParser.configFile = defaultPath
    config.read(argParser.configFile)

    # Setup root logger
    # default value
    defaultFormat = '%(asctime)s - %(name)s:%(lineno)d - ' \
                    '%(levelname)s - %(message)s'
    defaultLogLevel = "INFO"
    defaultLogFileDir = "logs"
    defaultRotateSize = "20"
    defaultConfigValue = {
        'max_log_file_size_mb': defaultRotateSize,
        'logfile_path': defaultLogFileDir,
        'level': defaultLogLevel,
        'format': defaultFormat
    }
    setSectionForConfigParser('logging', defaultConfigValue, config)
    rootlogger = setLogger(config['logging']['format'],
                           config['logging']['level'],
                           config['logging']['logfile_path'],
                           int(config['logging']['max_log_file_size_mb']))

    # setup config for other arguments
    logger.info("Parsing configuration")

    # commandline argument overwrites
    if argParser.pid is not None or argParser.procName is not None:
        if argParser.pid is not None:
            config.set('proc_info', 'pid', argParser.pid)
        if argParser.procName is not None:
            config.set('proc_info', 'process_name', argParser.procName)
    else:
        # if neither are provided in command line
        # check validity and if exists in config
        if config.get('proc_info', 'pid', fallback='') is not '':
            try:
                int(config.get('proc_info', 'pid'))
            except ValueError:
                raise ValueError('PID must be an integer')
        elif config.get('proc_info', 'process_name', fallback=None) is None:
            raise Exception('pid&process name are not defined in neither arguments nor config.')

    # set default values for optionals in config
    defaultOptionalValues = {
        "proc_info": {
            "aggregate_data": 'False',
            "is_java_process": 'True'
        },
        "system_info": {
            "per_disk": 'False',
            "per_nic": 'False'
        },
        "data": {
            "unit": "BYTES",
            "average": 'False'
        },
        "workers": {
            "pool": '4'
        }
    }
    for section, opts in defaultOptionalValues.items():
        for option, value in opts.items():
            configValue = config.get(section, option, fallback=None)
            if configValue is None or configValue is '':
                config.set(section, option, value)

    # Printout all the sections and properties read from config file
    for section in config.sections():
        logger.debug("%s:" % section)
        for key in config[section].keys():
            logger.debug("\t%s = %s" % (key, config[section][key]))

    return rootlogger, config

