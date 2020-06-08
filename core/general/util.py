# -*- encoding=utf8 -*-
from .cache import templates as T,points as P,TemplateMode as TM,PointMode as PM

from .cache import Skill,Spell,Level,Event,Group,Explore,Difficulty

from airtest.core.api import touch,wait,exists,sleep,wait_until_stable,swipe
from airtest.core.cv import TargetNotFoundError

from core.logger import get_logger
logger=get_logger(__name__)

def spread_shoot():
    try:
        touch(wait(T[TM.spread_shoot],3))
        return True
    except TargetNotFoundError:
        logger.error("spread_shoot fail")
        return False

def focus_shoot():
    try:
        touch(wait(T[TM.focus_shoot], 3))
        return True
    except TargetNotFoundError:
        logger.error("focus_shoot fail")
        return False

def graze():
    touch(P[PM.graze])
    sleep(0.5)

def auto_timeout():
    if exists(T[TM.msg_box_title]):
        touch(T[TM.msg_box_confirm])
        return True
    return False

def use_skill(*args:Skill):
    """
        param:0,1,2-->1,2,3 skill
        example-> use_skill(0,1,2)
    """
    try:
        touch(P[PM.skill_open])
        sleep(1)
        for i in args:
            touch(P[PM.spell][i.value])
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
        param:0/1/2/3/4-->1/2/3/4/5 spell
        example-> use_spell(0)
    """
    try:
        #wait(Template(r"tpl1588523129888.png", record_pos=(-0.448, 0.089), resolution=(1280, 720)))
        #touch(Template(r"tpl1588523129888.png", record_pos=(-0.448, 0.089), resolution=(1280, 720)))
        touch(P[PM.spell_open])
        #wait(Template(r"tpl1588559730239.png", record_pos=(-0.448, 0.088), resolution=(1280, 720)), 5)
        sleep(1.5)
        touch(P[PM.spell][s.value])
    except TargetNotFoundError:
        logger.error("use_spell fail, spell: " + str(s))

def auto_retry():
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

def touch_p():
    touch(P[PM.pboost])
    sleep(0.5)

def boost():
    touch(P[PM.pboost])
    sleep(0.5)

def exit():
    if exists(T[TM.battle_menu]):
        touch(T[TM.battle_menu])
    if exists(T[TM.quit_battle]):
        touch(T[TM.quit_battle])
    if exists(T[TM.quit_confirm]):
        touch(T[TM.quit_confirm])
        return True
    return False

def select_level(level:Level):
    '''0,1,2 ↑'''
    try:
        touch(P[PM.level][level.value])
        return True
    except:
        return False

def AtHome():
    if exists(T[TM.explore]):
        return True
    return False

def GoHome():
    auto_timeout()
    if exists(T[TM.home]):
        touch(T[TM.home])
        sleep(3)
    elif exists(T[TM.battle_menu]):
        if exit():
            sleep(3)
            touch(T[TM.home])
            sleep(3)
    elif exists(T[TM.next]):
        touch(P[PM.next])
        sleep(3)
        touch(T[TM.home])
        sleep(3)
    
    return AtHome()

def GoExplore():
    if exists(T[TM.explore]):
        touch(T[TM.explore])

def SelectExplore(e:Explore):
    '''→012'''
    touch(P[PM.explore][e.value])
    sleep(0.5)

def GoFarSeek():
    if exists(T[TM.farseek]) or exists(T[TM.farseek_temp]):
        touch(T[PM.farseek])
        sleep(0.5)
        return True
    return False

def SwipeLevel():
    swipe(P[PM.swipe][0], P[PM.swipe][1], duration=1, steps=20)

def WaitStatic(picture=T[TM.p], max_time=5, timeout=5):
    return wait_until_stable(v=picture, timeout=timeout, interval=0.5, trytimes=max_time)

def Back():
    if exists(T[TM.back]):
        touch(T[TM.back])

def SelectEvent(event:Event):
    '''↑0/1/2/3'''
    touch(P[PM.event][event.value])
    sleep(0.5)

def SelectDifficulty(d:Difficulty):
    '''0=normal, 1=hard, 2=lunatic'''
    if d in [TM.normal,TM.hard,TM.lunatic]:
        #pos = PointSet([427, 652], src_resolution)
        for i in range(3):
            if not exists(T[d.value]):
                touch(P[PM.difficultychange])
                sleep(1)
            else:
                break

def ChangeGroup(last=False):
    '''last=True select last group'''
    if last:
        touch(P[PM.group][0])
    else:
        touch(P[PM.group][1])
        
def FindMap(m, times = 5):
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
    pass