# -*- coding: utf-8 -*-

from .logger import init_logging
from .setting import Settings as ST

# init_logging(__name__,logging.INFO)

def setup_log():
    init_logging(__name__)
    return init_logging()