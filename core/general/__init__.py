# -*- coding: utf-8 -*-

import os

from core.helper import load_img as li

BASEPATH=os.path.dirname(__file__)
TEMPLATEPATH=os.path.join(BASEPATH,'template')

def load_img(fname):
    return li(os.path.join(TEMPLATEPATH,fname))