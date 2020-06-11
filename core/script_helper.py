# -*- coding: utf-8 -*-

from .general.util import *
from airtest.core.cv import Template,PointSet


#切换队伍
def select_group(target:Template,maxtime:int=5,waittime:int=2):
    for i in range(maxtime):
        if not exists(target):
            ChangeGroup(True)
            sleep(waittime)
        else:
            return True
    return False

#前往关卡页面
def Go_level():
    pass


