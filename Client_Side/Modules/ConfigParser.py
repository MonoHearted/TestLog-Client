import configparser
import logging
from configparser import NoOptionError

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
    # Load the configuration file
    config = configparser.RawConfigParser(allow_no_value=True)
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
    # get local logger
    logger = logging.getLogger(__name__)

    # setup config for other arguments
    logger.info("Parsing configuration")

    """
    Validate other options in config file
    Including Mandatory and Optional Opts   
    """
    # validate mandatory options
    mandatoryOpts = [('cassandra', 'hosts'), ('elasticsearch', 'hosts'),
                     ('metadata', 'template_cr'), ('metadata', 'template_sr')
                     ]

    def validateMandatoryOpts(sectionOpt):
        retOpt = config.get(sectionOpt[0], sectionOpt[1], fallback=None)
        if (retOpt is None or ''):
            raise NoOptionError(sectionOpt[1], sectionOpt[0])

    for opt in mandatoryOpts:
        validateMandatoryOpts(opt)

    """
    Endtime is not mandatory in cmdline argument
    thus, check cmdline and config file, setting it in either way is fine
    """
    if (argParser.endTime is not None):
        # if set in cmdline
        config.set('metadata', 'endtime', argParser.endTime)
    else:
        """
        if not set in cmdline
        if not set in config file or set in config file, but it's empty
        """
        if (config.get('metadata', 'endtime', fallback=None) is None or
                config.get('metadata', 'endtime', fallback=None) is ''):
            raise Exception("Neither in cmdline nor config file, "
                            "[metadata][endtime] is set")
        # check whether it is a int
        try:
            int(config.get('metadata', 'endtime'))
        except ValueError:
            raise ValueError("endtime must be "
                             "an epoch timestamp in millisecond")

    """
    Same situation for keys
    Check both cmdline and config file
    """
    if (argParser.keys is not None):
        config.set('metadata', 'keys', argParser.endTime)
    else:
        if (config.get('metadata', 'keys', fallback=None) is None or
                config.get('metadata', 'keys', fallback=None) is ''):
            raise Exception("Neither in cmdline nor config file, "
                            "[metadata][keys] is set")
        # check whether it is a int
        try:
            int(config.get('metadata', 'keys'))
        except ValueError:
            raise ValueError("keys must be an integer")

    """
    Version has default value, set it to elasticsearch section
    Datatype has default value, set it to metadata section
    """
    config.set('elasticsearch', 'version', argParser.version)
    config.set('metadata', 'datatype', argParser.dataType)

    # setting up config for optional options but with default value

    # default set to 1000ms, 1s
    defaultInterval = "1000"
    defaultWorkerPoolSize = "4"
    if (config.get('metadata', 'interval', fallback=defaultInterval) is ''):
        config.set('metadata', 'interval', defaultInterval)

    if (config.get('workers', 'pool', fallback=defaultWorkerPoolSize) is ''):
        config.set('workers', 'pool', defaultWorkerPoolSize)

    # Printout all the sections and properties red from config file
    for section in config.sections():
        logger.debug("%s:" % section)
        for key in config[section].keys():
            logger.debug("\t%s = %s" % (key, config[section][key]))
    return rootlogger, config
