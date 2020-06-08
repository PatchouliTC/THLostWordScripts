###
###
###  Store All Script in here
###
###

import os

from core.helper import load_img as li

BASEPATH=os.path.dirname(__file__)
TEMPLATEPATH=os.path.join(BASEPATH,'template')
RESAULTPATH=os.path.join(BASEPATH,'script_resault')

def load_img(fname):
    return li(os.path.join(TEMPLATEPATH,fname))

from core.logger import init_logging,logging


if not os.path.exists(RESAULTPATH):
    os.makedirs(RESAULTPATH)

init_logging(__name__,level=logging.INFO)
#,filepath=os.path.join(BASEPATH,'script_resault','result.log')

