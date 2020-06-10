# -*- encoding=utf8 -*-
from enum import IntEnum,auto
from core.general import load_img as li
from core.setting import Settings as CST

from airtest.core.api import ST
from airtest.core.cv import Template,PointSet
from airtest.utils.transform import TargetPos

from core.logger import get_logger
logger=get_logger(__name__)

ST.FIND_TIMEOUT_TMP=2

class IEnum(IntEnum):
    """
        自增IntEnum+避免重复值
        X=auto()
    """
    def __init__(self, *args):
        cls = self.__class__
        if any(self.value == e.value for e in cls):
            a = self.name
            e = cls(self.value).name
            raise ValueError(f"{cls.__name__}存在值相等情况:{a}->{e}")
    
    #从0开始自增
    def _generate_next_value_(name, start, count, last_values):
        for last_value in reversed(last_values):
            try:
                return last_value + 1
            except TypeError:
                pass
        else:
            #I need start with 0
            return 0

class TemplateMode(Enum):
    """
        特征图枚举
        templates直接使用此KEY表获取对应图
        example:templates[TemplateMode.spread_shoot]
    """
    #战斗定义---
    #扩散平A
    spread_shoot=auto(),
    #集中平A
    focus_shoot=auto(),

    #信息框标题
    msg_box_title=auto(),
    #信息框确定按钮
    msg_box_confirm=auto(),
    #信息框失败时返回按钮
    msg_box_fail=auto(),
    #信息框确定按钮-无边框
    msg_box_confirm_noborder=auto(),

    #战斗失败标记
    battle_fail=auto(),
    #战斗胜利标记
    battle_success=auto(),
    #删除了旧版的结算确定按键
    #使用符卡页面展开
    spell_expanded=auto(),
    #使用技能页面展开
    skill_expanded=auto(),
    #战斗中菜单按钮
    battle_menu=auto(),
    #退出战斗
    quit_battle=auto(),
    #退出确认按钮
    quit_confirm=auto(),
    #主页面探索按钮
    explore=auto(),
    #返回主页面按钮
    home=auto(),
    #远征标记
    farseek=auto(),
    #临时远征标记
    farseek_temp=auto(),

    #P-BOOST标记-用于判断战斗界面UI移动是否结束
    p=auto(),
    #符卡
    spell_card=auto(),
    #结界
    graze=auto(),
    #技能
    skill=auto(),

    #返回按钮
    back=auto(),
    #cancel->next
    next=auto(),
    #战斗结束重新战斗按钮
    rebattle=auto(),
    #准备房间出发按钮
    startbattle=auto(),

class OffsetMode(IEnum):
    skill=auto(),
    spell=auto(),
    level=auto(),
    event=auto(),
    explore=auto(),

class PointMode(Enum):
    """
        单独坐标点枚举
    """
    #护盾
    graze=auto(),
    #展开技能详情
    skill_open=auto(),
    confirm=auto(),
    #技能详情收起skill_shrink->skill_expanded
    skill_expanded=auto(),
    #展开符卡详情
    spell_open=auto(),
    #使用P点
    pboost=auto(),
    
    level=auto(),
    spell=auto(),
    swipe=auto(),
    event=auto(),
    #切换队伍
    group=auto(),
    skill=auto(),
    #难度变更点
    difficultychange=auto(),
    #进入探索
    explore=auto(),
    #进入远征
    farseek=auto(),
    #cancel->next
    next=auto(),
    #重新战斗
    rebattle=auto(),
    #战斗结算
    battle_success=auto(),

class Skill(IntEnum):
    """
        技能
    """
    A=0,
    B=1,
    C=2

class Spell(IntEnum):
    """
        符卡
    """
    A=0,
    B=1,
    C=2,
    D=3,
    LW=4
    
class Difficulty(IntEnum):
    """
        难度
    """
    normal=1110,
    hard=1111,
    lunatic=1112

class Level(IntEnum):
    """
        关卡
    """
    M1=0,
    M2=1,
    M3=2

class Event(IntEnum):
    """
        章节
    """
    Story1=0,
    Story2=1,
    Story3=2,
    Story4=3

class Group(IntEnum):
    """
        队伍左右切换
    """
    last=0,
    next=1

class Explore(IntEnum):
    A=0,
    B=1,
    C=2

cuntom_offsets={
    OffsetMode.skill:[[197, 592], [292, 591], [381, 589]],
    OffsetMode.spell:[[230, 407], [416, 328], [614, 266], [805, 225], [1007, 207]],
    OffsetMode.level:[[876, 506], [876, 354], [876, 206]],
    OffsetMode.event:[[885, 546], [870, 392], [863, 250], [886, 144]],
    OffsetMode.explore:[[669, 652], [895, 649], [1111, 655]],
}

templates={
    TemplateMode.spread_shoot:Template(image=li(r"spread_shoot.png"), target_pos=TargetPos.RANDOMINLINE,record_pos=(-0.346, 0.15), resolution=(1280, 720)),
    TemplateMode.focus_shoot:Template(image=li(r"focus_shoot.png"), target_pos=TargetPos.RANDOMINLINE,record_pos=(-0.02, 0.149), resolution=(1280, 720)),
    #auto_timeout使用,timeout->msg_box_title
    TemplateMode.msg_box_title:Template(image=li(r"msg_box_title.png"), target_pos=TargetPos.RANDOMINLINE,record_pos=(-0.001, -0.125), resolution=(1280, 720)),
    #新增msg_box_confirm,msg_box_fail,msg_box_confirm_noborder
    TemplateMode.msg_box_confirm:Template(image=li(r"msg_box_confirm.png"), target_pos=TargetPos.RANDOMINLINE,record_pos=(0.106, 0.113), resolution=(1280, 720)),
    TemplateMode.msg_box_fail:Template(image=li(r"msg_box_fail.png"), target_pos=TargetPos.RANDOMINLINE, resolution=(1280, 720)),
    TemplateMode.msg_box_confirm_noborder:Template(image=li(r"msg_box_confirm_noborder.png"), target_pos=TargetPos.RANDOMINLINE, resolution=(1280, 720)),
    
    TemplateMode.battle_fail:Template(image=li(r"battle_fail.png"), threshold=0.7, target_pos=TargetPos.RANDOMINLINE,record_pos=(0.0, 0.002), resolution=(1280, 720)),
    TemplateMode.battle_success:Template(image=li(r"battle_success.png"), target_pos=TargetPos.RANDOMINLINE,record_pos=(-0.001, -0.166), resolution=(1280, 720)),
    
    #删除了旧版的结算确定按键

    #更改了名称spell_shrink->spell_expanded
    #skill_shrink->skill_expanded
    TemplateMode.spell_expanded:Template(image=li(r"spell_expanded.png"), target_pos=TargetPos.RANDOMINLINE,record_pos=(-0.448, 0.088), resolution=(1280, 720)),
    TemplateMode.skill_expanded:Template(image=li(r"skill_expanded.png"), target_pos=TargetPos.RANDOMINLINE,record_pos=(0.452, 0.138), resolution=(1280, 720)),
    
    TemplateMode.battle_menu:Template(image=li(r"battle_menu.png"), target_pos=TargetPos.RANDOMINLINE,record_pos=(0.037, -0.259), resolution=(1280, 720)),
    
    #room_confirm->quit_confirm
    TemplateMode.quit_battle:Template(image=li(r"quit_battle.png"), target_pos=TargetPos.RANDOMINLINE,record_pos=(0.395, 0.222), resolution=(1280, 720)),
    TemplateMode.quit_confirm:Template(image=li(r"quit_confirm.png"), target_pos=TargetPos.RANDOMINLINE,record_pos=(0.108, 0.113), resolution=(1280, 720)),

    TemplateMode.explore:Template(image=li(r"explore.png"), target_pos=TargetPos.RANDOMINLINE,record_pos=(0.419, 0.168), resolution=(1280, 720)),
    TemplateMode.home:Template(image=li(r"home.png"), target_pos=TargetPos.RANDOMINLINE,record_pos=(0.473, -0.257), resolution=(1280, 720)),

    #temp_expedition->farseek_temp
    TemplateMode.farseek:Template(image=li(r"farseek.png"), target_pos=TargetPos.RANDOMINLINE,record_pos=(0.37, 0.048), resolution=(1280, 720)),
    TemplateMode.farseek_temp:Template(image=li(r"farseek_temp.png"), target_pos=TargetPos.RANDOMINLINE,record_pos=(0.367, 0.052), resolution=(1280, 720)),

    #static->p
    #新增spell_card,graze,skill
    TemplateMode.p:Template(image=li(r"p.png"), target_pos=TargetPos.RANDOMINLINE,record_pos=(0.305, 0.165), resolution=(1280, 720)),
    TemplateMode.spell_card:Template(image=li(r"spell_card.png"), target_pos=TargetPos.RANDOMINLINE, resolution=(1280, 720)),
    TemplateMode.graze:Template(image=li(r"graze.png"), target_pos=TargetPos.RANDOMINLINE, resolution=(1280, 720)),
    TemplateMode.skill:Template(image=li(r"skill.png"), target_pos=TargetPos.RANDOMINLINE, resolution=(1280, 720)),

    TemplateMode.back:Template(image=li(r"back.png"), target_pos=TargetPos.RANDOMINLINE,record_pos=(-0.471, -0.255), resolution=(1280, 720)),
    
    Difficulty.normal:Template(image=li(r"normal.png"), target_pos=TargetPos.RANDOMINLINE,record_pos=(-0.162, 0.223), resolution=(1280, 720)),
    Difficulty.hard:Template(image=li(r"hard.png"), target_pos=TargetPos.RANDOMINLINE,record_pos=(-0.164, 0.224), resolution=(1280, 720)),
    Difficulty.lunatic:Template(image=li(r"lunatic.png"), target_pos=TargetPos.RANDOMINLINE,record_pos=(-0.16, 0.223), resolution=(1280, 720)),

    #cancel->next
    TemplateMode.next:Template(image=li(r"next.png"), target_pos=TargetPos.RANDOMINLINE,record_pos=(0.419, 0.168), resolution=(1280, 720)),
    TemplateMode.rebattle:Template(image=li(r"rebattle.png"), target_pos=TargetPos.RANDOMINLINE,record_pos=(0.419, 0.168), resolution=(1280, 720)),
    TemplateMode.startbattle:Template(image=li(r"startbattle.png"), target_pos=TargetPos.RANDOMINLINE,record_pos=(0.419, 0.168), resolution=(1280, 720)),
}

points={
    PointMode.graze:PointSet([1144, 407], (1280, 720), 10),
    PointMode.skill_open:PointSet([1216, 538], (1280, 720), 5),
    PointMode.confirm:PointSet([772, 559], (1280, 720), 5),
    PointMode.skill_expanded:PointSet([1216, 538], (1280, 720), 5),
    PointMode.spell_open:PointSet([57, 478], (1280, 720), 5),
    PointMode.skill:[
        PointSet(cuntom_offsets[OffsetMode.skill][Skill.A], (1280, 720), 5),
        PointSet(cuntom_offsets[OffsetMode.skill][Skill.B], (1280, 720), 5),
        PointSet(cuntom_offsets[OffsetMode.skill][Skill.C], (1280, 720), 5),
    ],

    PointMode.spell:[
        PointSet(cuntom_offsets[OffsetMode.spell][Spell.A], (1280, 720), 5),
        PointSet(cuntom_offsets[OffsetMode.spell][Spell.B], (1280, 720), 5),
        PointSet(cuntom_offsets[OffsetMode.spell][Spell.C], (1280, 720), 5),
        PointSet(cuntom_offsets[OffsetMode.spell][Spell.D], (1280, 720), 5),
        PointSet(cuntom_offsets[OffsetMode.spell][Spell.LW], (1280, 720), 5),
    ],

    PointMode.pboost:PointSet([1060, 582], (1280, 720), 10),

    PointMode.level:[
        PointSet(cuntom_offsets[OffsetMode.level][0], (1280, 720), 10),
        PointSet(cuntom_offsets[OffsetMode.level][1], (1280, 720), 10),
        PointSet(cuntom_offsets[OffsetMode.level][2], (1280, 720), 10),
    ],

    PointMode.swipe:[
        PointSet((640, 500), (1280, 720)),#start
        PointSet((640, 170), (1280, 720)),#end
    ],

    PointMode.event:[
        PointSet(cuntom_offsets[OffsetMode.event][0], (1280, 720), 10),
        PointSet(cuntom_offsets[OffsetMode.event][1], (1280, 720), 10),
        PointSet(cuntom_offsets[OffsetMode.event][2], (1280, 720), 10),
        PointSet(cuntom_offsets[OffsetMode.event][3], (1280, 720), 10),
    ],

    PointMode.group:[
        PointSet([39, 431], (1280, 720)),#last
        PointSet([826, 429], (1280, 720)),#next
    ],

    PointMode.difficultychange:PointSet([427, 652], (1280, 720)),
    PointMode.explore:[
        PointSet(cuntom_offsets[OffsetMode.explore][0], (1280, 720), 5),
        PointSet(cuntom_offsets[OffsetMode.explore][1], (1280, 720), 5),
        PointSet(cuntom_offsets[OffsetMode.explore][2], (1280, 720), 5),
    ],
    PointMode.farseek:PointSet([1110, 434], (1280, 720), 5),
    PointMode.next:PointSet([1140, 650], (1280, 720), 5),
    PointMode.rebattle:PointSet([108, 652], (1280, 720), 5),
    PointMode.battle_success:PointSet([641, 151], (1280, 720), 5)
}

logger.debug('cache generate finish')