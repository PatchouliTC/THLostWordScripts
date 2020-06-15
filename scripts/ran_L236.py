# -*- coding: utf-8 -*-

from core.battle import *
from . import RESAULTPATH, TEMPLATEPATH

class ran_L236(Battle):
    ScriptName='ran_L236'
    Description='蓝 L236'
    ENABLERECORD=False
    #关卡
    LEVEL_NAME = "L236"
    #队伍
    group = Template(image=li(os.path.join(TEMPLATEPATH, "group", r"ran.png")), threshold=0.85, resolution=(1280, 720))

    def __init__(self):
        super().__init__(base=RESAULTPATH)