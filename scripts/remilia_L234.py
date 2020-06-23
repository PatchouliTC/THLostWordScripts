# -*- coding: utf-8 -*-

from core.battle import *
from . import RESAULTPATH, TEMPLATEPATH

class remilia_L234(Battle):
    ScriptName='remilia_L234'
    Description='蕾咪 L234'
    ENABLERECORD=False
    #关卡
    LEVEL_NAME = "L234"
    #队伍
    group = Template(image=li(os.path.join(TEMPLATEPATH, "group", r"remilia.png")), threshold=0.85, resolution=(854, 480))

    def __init__(self):
        super().__init__(base=RESAULTPATH)

    def InitSelectLevel(self):
        '''初始化选择章节方法'''
        try:
            util.SelectExplore(1)
            sleep(1)
            util.SelectExplore(0)
            sleep(1)
            Go_level(Event.Story4, Chapter.C2, Difficulty.lunatic)
            sleep(1)
        except TargetNotFoundError as e:
            self.Logger.error(f'{self.ScriptName} InitSelectLevel fail({str(e)})')
            return False
        else:
            return True

    def SelectLevel(self):
        '''选择关卡'''
        return util.select_level(Level.M1)
        #touch(self.level)

    def Battle(self):
        '''战斗逻辑'''
        util.WaitStatic()
        util.boost()
        util.use_skill(0, 2)
        util.use_spell(0)
        sleep(self.wave_resttime)
        #进入2面
        util.WaitStatic()
        util.graze()
        util.use_skill(1)
        util.use_spell(1)
        sleep(self.wave_resttime)
        util.WaitStatic()
        util.graze()
        util.use_spell(3)
        sleep(self.wave_resttime)
        #进入3面
        util.WaitStatic()
        util.graze()
        util.boost()
        util.boost()
        util.boost()
        util.use_spell(2)
        sleep(self.wave_resttime)

    def BattleEndAtk(self):
        '''结束战斗用的战斗方式,默认使用集中弹幕'''
        util.graze()
        util.boost()
        util.spread_shoot()