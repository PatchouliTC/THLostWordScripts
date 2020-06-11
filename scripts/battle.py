# -*- coding: utf-8 -*-

import os
from core.script_base import ScriptBase
from . import load_img as li,RESAULTPATH

from core.general import util
from core.script_helper import *
from airtest.core.api import *

#image save at scripts/template
#use li to load scriptimage--> image=li(r"t112521512.png")
class Battle(ScriptBase):
    ScriptName='battle'
    Description='战斗脚本基类'
    ENABLERECORD=False
    #关卡
    LEVEL_NAME = "L236"
    #当前战斗信息
    #最大失败重试次数
    max_enter_fail = 10
    max_end_fail = 5
    #每波次等待时间
    wave_resttime = 15
    #队伍
    group = Template(image=li(os.path.join("group", r"ran.png")), threshold=0.85, record_pos=(-0.044, 0.22), resolution=(1280, 720))

    level = Template(image=li(os.path.join("level", r"L236.png")), record_pos=(0.197, -0.137), resolution=(1280, 720))
    #章节,如果不使用图片选择章节,则需要重载InitSelectLevel方法
    event = Template(image=li(os.path.join("event", r"L23.png")), threshold=0.85, record_pos=(0.145, -0.027), resolution=(1280, 720))
    
    def __init__(self):
        super().__init__(RESAULTPATH,__name__)
        self.first_time = True
        self.change_group = True
        self.in_battle = False
        self.end_battle = False
        self.enter_fail = 0
        self.end_fail = 0

    def start(self):
        self.Logger.info(f'关卡 {self.LEVEL_NAME}')
        #raise NotImplementedError('BaseScript-start error-No Function Defined')

        self.first_time = True
        self.in_battle = False
        if util.GoHome():
            util.GoExplore()
            sleep(2)
            self.InitSelectLevel()
            self.first_time = False
        else:
            self.Logger.error(f'{self.ScriptName} 返回主页面失败')

    def run(self):
        #print(f'{self.ScriptName} 脚本真实循环执行的逻辑...')
        #self.Logger.info('sample1 run')
        self.start_record()
        self.fail = False

        while not self.BattleStart():
            pass

        self.Battle()

        while not self.BattleEnd():
            pass


    def finish(self):
        print(f'{self.ScriptName} 脚本循环结束，返回主界面,方便其他脚本运行')
        #raise NotImplementedError('BaseScript-finish error-No Function Defined')

        util.GoHome()

    def SelectGroup(self):
        '''选择队伍方法'''
        return select_group(target=self.group)
    
    def InitSelectLevel(self):
        '''初始化选择章节方法'''
        try:
            util.SelectExplore(1)
            sleep(1)
            util.SelectExplore(0)
            sleep(1)
            util.SelectEvent(3)
            util.SelectDifficulty(Difficulty.lunatic)
            sleep(1)
            touch(self.event)
            sleep(1)
        except TargetNotFoundError as e:
            self.Logger.error(f'{self.ScriptName} InitSelectLevel fail({str(e)})')
            return False
        else:
            return True

    def SelectLevel(self):
        '''选择关卡'''
        return util.select_level(Level.M3)
        #touch(self.level)

    def BattleStart(self):
        '''进入战斗逻辑,包含切换队伍'''

        #再次挑战的情况
        if exists(T[TM.rebattle]):
            touch(P[PM.rebattle])
            self.in_battle = True
            return self.in_battle
        #情况一,未进入战斗
        if not self.in_battle:
            sleep(2)
            util.auto_timeout()
            if not exists(T[TM.startbattle]):
                if not self.SelectLevel():
                    self.enter_fail += 1
                else:
                    sleep(5)
            else:
                if not self.SelectGroup():
                    self.enter_fail += 1
                else:
                    touch(T[TM.startbattle])
                    self.in_battle = True
                    #已进入战斗,等待加载或超时
                    sleep(self.wave_resttime)
                    if util.auto_timeout():
                        self.in_battle = False
            
            if self.enter_fail >= self.max_enter_fail:
                self.enter_fail = 0
                util.auto_timeout()
                util.auto_retry()
                util.GoHome()
                util.GoExplore()
                sleep(3)
                self.InitSelectLevel()
        return self.in_battle

    def Battle(self):
        '''战斗逻辑'''
        util.WaitStatic()
        #选定小恶魔
        #touch(PointSet([235, 358], src_resolution, 10))
        util.graze()
        util.graze()
        util.graze()
        util.boost()
        util.use_skill(0, 1, 2)
        util.use_spell(0)
        sleep(self.wave_resttime)
        #进入2面
        util.WaitStatic()
        util.graze()
        util.use_spell(1)
        sleep(self.wave_resttime)
        #进入3面
        util.WaitStatic(max_time=3, timeout=3)
        util.graze()
        util.boost()
        util.use_spell(2)
        sleep(self.wave_resttime)

    def BattleEnd(self):
        '''
        战斗结束判断
        :return: 战斗结束True
        '''
        #判断结算图
        if not self.end_battle and not exists(T[TM.battle_success]):
            if self.end_fail >= self.max_end_fail:
                self.end_fail = 0
                if util.auto_timeout():
                    return False
                if exists(T[TM.battle_fail]):
                    self.fail = True
                    self.end_battle = True
                else:
                    util.auto_retry()
                    self.end_battle = True
            if not util.WaitStatic(max_time=1, timeout=3):
                self.end_fail += 1
            else:
                self.end_fail = 0
                self.BattleEndAtk()
            
            return False
        #结算
        else:
            if self.fail:
                touch(T[TM.battle_fail])
                self.end_record(False)
            else:
                self.write_result()
                touch(P[PM.battle_success])
                self.end_record(True)

            return True

    def BattleEndAtk(self):
        '''结束战斗用的战斗方式,默认使用集中弹幕'''
        util.graze()
        util.boost()
        util.focus_shoot()