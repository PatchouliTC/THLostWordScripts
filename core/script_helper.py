from .general.util import *



#切换队伍
def select_group(target,changetime=2):
    if not exists(target):
        ChangeGroup(True)
        sleep(changetime)
        return False
    return True

#前往关卡页面
def Go_level():
    pass


