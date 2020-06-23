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
def Go_level(event:Event=None, chapter:Chapter=None, difficulty:Difficulty=None, swipe_times = 0):
    '''
        跳转到章,节,关卡,不点击关卡
        :param event:章
        :param chapter:节
        :param difficulty:难度
        :param swipe_times:滑动次数
    '''
    if event:
        SelectEvent(event)
    if difficulty:
        SelectDifficulty(difficulty) 
        sleep(1)
    if chapter:
        SelectChapter(chapter)
    if swipe_times>0:
        for i in range(swipe_times):
            SwipeLevel()
            sleep(2)

    return True
