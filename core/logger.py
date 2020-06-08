import os
import logging

ROOT='TH_LW'

def init_logging(logname:str=ROOT,level:int=logging.DEBUG,filepath:str=None):
    # logger = logging.root
    # use 'airtest' as root logger name to prevent changing other modules' logger
    logger = logging.getLogger(logname)
    logger.setLevel(level)
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        fmt='[%(asctime)s][%(levelname)s]<%(name)s> %(message)s',
        datefmt='%I:%M:%S'
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    if filepath is not None:
        fhandler=logging.FileHandler(filename=filepath,encoding='utf-8')
        fhandler.setFormatter(formatter)
        logger.addHandler(fhandler)
    return logger

def set_logger_level(logname:str=ROOT,level:int=logging.DEBUG):
    logging.getLogger(logname).setLevel(level)


def get_logger(name:str=ROOT):
    logger = logging.getLogger(name)
    return logger


def get_script_logger(name:str=None,filepath:str=None,level:int=logging.INFO):
    if name is None:
        log=logging.getLogger(ROOT)
    else:
        log=logging.getLogger(name)

    if filepath is not None and len(log.handlers) == 0:
        formatter = logging.Formatter(
            fmt='[%(asctime)s][%(levelname)s]<%(name)s> %(message)s',
            datefmt='%I:%M:%S'
        )
        log.setLevel(level)
        fhandler=logging.FileHandler(filename=filepath,encoding='utf-8')
        fhandler.setFormatter(formatter)
        log.addHandler(fhandler)
    return log