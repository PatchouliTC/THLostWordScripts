# -*- encoding=utf8 -*-
from .cache import templates as T,points as P,TemplateMode as TM,PointMode as PM

from .cache import Skill,Spell,Level,Event,Group,Explore,Difficulty

from airtest.core.api import touch,wait,exists,sleep,wait_until_stable,swipe
from airtest.core.cv import TargetNotFoundError

from core.logger import get_logger
logger=get_logger(__name__)

""" 底层单元函数 """

def spread_shoot():
    """尝试使用扩散普通攻击"""
    try:
        touch(wait(T[TM.spread_shoot],3))
        return True
    except TargetNotFoundError:
        logger.error("spread_shoot fail")
        return False

def focus_shoot():
    """尝试使用集中普通攻击"""
    try:
        touch(wait(T[TM.focus_shoot], 3))
        return True
    except TargetNotFoundError:
        logger.error("focus_shoot fail")
        return False

def graze():
    """使用护盾"""
    touch(P[PM.graze])
    sleep(0.5)

def auto_timeout():
    """是否链接超时并尝试重连一次"""
    if exists(T[TM.msg_box_title]):
        touch(T[TM.msg_box_confirm])
        return True
    return False

def use_skill(*args:Skill):
    """
        使用技能，可以多个
        example-> use_skill(Skill.A，Skill.B)
    """
    try:
        touch(P[PM.skill_open])
        sleep(1)
        for i in args:
            touch(P[PM.skill][i])
            sleep(0.75)
            touch(P[PM.confirm])
            sleep(0.75)
    except TargetNotFoundError:
        logger.error("use_skill fail, skill: " + str(args))       
    finally:
        touch(P[PM.skill_expanded])
        sleep(0.5)


def use_spell(s:Spell):
    """
        使用符卡
        example-> use_spell(Spell.A)
    """
    try:
        #wait(Template(r"tpl1588523129888.png", record_pos=(-0.448, 0.089), resolution=(1280, 720)))
        #touch(Template(r"tpl1588523129888.png", record_pos=(-0.448, 0.089), resolution=(1280, 720)))
        touch(P[PM.spell_open])
        #wait(Template(r"tpl1588559730239.png", record_pos=(-0.448, 0.088), resolution=(1280, 720)), 5)
        sleep(1.5)
        touch(P[PM.spell][s])
    except TargetNotFoundError:
        logger.error("use_spell fail, spell: " + str(s))

def auto_retry():
    """
        战斗结算重试+符卡|技能页面收回
        最终异常处理
    """
    if exists(T[TM.battle_fail]):
        touch(T[TM.battle_fail])
        return

    if exists(T[TM.battle_success]):
        touch(T[TM.battle_success])
        return
    #删除了旧版的结算决定按键

    if exists(T[TM.spell_expanded]):
        touch(T[TM.spell_expanded])
        return

    if exists(T[TM.skill_expanded]):
        touch(T[TM.skill_expanded])  
        return
    exit()

def boost():
    """使用P点一次"""
    touch(P[PM.pboost])
    sleep(0.5)

def exit():
    """中途退出战斗"""
    if exists(T[TM.battle_menu]):
        touch(T[TM.battle_menu])
    if exists(T[TM.quit_battle]):
        touch(T[TM.quit_battle])
    if exists(T[TM.quit_confirm]):
        touch(T[TM.quit_confirm])
        return True
    return False

def select_level(level:Level):
    """
        选择关卡
        example->select_level(Level.M1)
    """
    try:
        touch(P[PM.level][level])
        return True
    except:
        return False

def AtHome():
    """是否在主界面"""
    if exists(T[TM.explore]):
        return True
    return False

def GoHome():
    """返回主界面"""
    auto_timeout()
    if AtHome():
        return True
    #有回家按钮直接点
    if exists(T[TM.home]):
        touch(T[TM.home])
        sleep(3)
    #如果在战斗中退出战斗之后点
    elif exists(T[TM.battle_menu]):
        if exit():
            sleep(3)
            touch(T[TM.home])
            sleep(3)
    #另一种特殊情况
    elif exists(T[TM.next]):
        touch(P[PM.next])
        sleep(3)
        touch(T[TM.home])
        sleep(3)
    
    return AtHome()

def GoExplore():
    """进入探索[战斗地图]页面"""
    if exists(T[TM.explore]):
        touch(T[TM.explore])

def SelectExplore(e:Explore):
    """
        选择战斗类别
        example-> SelectExplore(Explore.A)
    """
    touch(P[PM.explore][e])
    sleep(0.5)

def GoFarSeek():
    """进入远征页面"""
    if exists(T[TM.farseek]) or exists(T[TM.farseek_temp]):
        touch(T[PM.farseek])
        sleep(0.5)
        return True
    return False

def SwipeLevel(up:bool=True):
    """滑动当前关卡总览"""
    if up:
        swipe(P[PM.swipe][1], P[PM.swipe][0], duration=1, steps=20)
    else:
        swipe(P[PM.swipe][0], P[PM.swipe][1], duration=1, steps=20)

def WaitStatic(picture=T[TM.p], max_time=5, timeout=5):
    """
        等待动画结束
        picture:特征图 默认为战斗中的P点标识
        max_time:最大重试次数
        timeout:每次重试最长等待时间
    """
    return wait_until_stable(v=picture, timeout=timeout, interval=0.5, trytimes=max_time)

def Back():
    """
        返回[特殊]
    """
    if exists(T[TM.back]):
        touch(T[TM.back])

def SelectEvent(event:Event):
    '''
        切换章节
        example:SelectEvent(Event.Story1)
    '''
    touch(P[PM.event][event])
    sleep(0.5)

def SelectDifficulty(d:Difficulty):
    '''
        切换副本难度
        example:SelectDifficulty(Difficulty.normal)
    '''
    if d in [Difficulty.normal,Difficulty.hard,Difficulty.lunatic]:
        #pos = PointSet([427, 652], src_resolution)
        for i in range(3):
            if not exists(T[d]):
                touch(P[PM.difficultychange])
                sleep(1)
            else:
                break

def ChangeGroup(last=False):
    '''
        切换打本队伍
        last=True 选择向左切换 False向右切换
    '''
    if last:
        touch(P[PM.group][0])
    else:
        touch(P[PM.group][1])
        
def FindMap(m, times = 5):
    """
        查询图片是否存在
        m:airtest.cv.Template
        times:重试次数
    """
    try:
        for i in range(times):
            findit = exists(m)
            if findit:
                return True
            else:
                SwipeLevel()
                sleep(1.5)
    except TargetNotFoundError:
        logger.error("cannot find map")
    return False

def Whereami():
    """返回自身当前位置"""
    pass