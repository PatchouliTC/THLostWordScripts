# -*- coding: utf-8 -*-

from core.battle import *
from . import RESAULTPATH, TEMPLATEPATH

class remilia_L234(Battle):
    ScriptName='event_dd'
    Description='摸你傻揍帝帝组'
    ENABLERECORD=False
    #关卡
    LEVEL_NAME = "EL234"
    #队伍
    group = None

    def __init__(self):
        super().__init__(base=RESAULTPATH,module=__name__)

    def InitSelectLevel(self):
        '''初始化选择章节方法'''
        try:
            Go_level(difficulty=Difficulty.lunatic,event=Event.Story4)
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

    def Battle(self):
        '''战斗逻辑'''
        util.WaitStatic()
        util.boost()
        util.use_skill(Skill.A)
        util.use_spell(Spell.LW)
        sleep(self.wave_resttime)

    def BattleEndAtk(self):
        '''结束战斗用的战斗方式,默认使用集中弹幕'''
        util.graze()
        util.boost()
        util.spread_shoot()
        sleep(self.wave_resttime)