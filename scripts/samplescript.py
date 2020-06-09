import os
from core.script_base import ScriptBase
from . import load_img as li,TEMPLATEPATH,RESAULTPATH
from core.general import util

#image save at scripts/template
#use li to load scriptimage--> image=li(r"t112521512.png")
class SampleScript(ScriptBase):
    ScriptName='sample1'
    Description='This is Sample1 Description'
    ENABLERECORD=False

    def __init__(self):
        super().__init__(RESAULTPATH,__name__)

    def start(self):
        print(f'Sample1 脚本准备启动...')
        print(f'准备脚本真实内容要求的条件和环境...')
        #raise NotImplementedError('BaseScript-start error-No Function Defined')

    def run(self):
        print(f'Sample1脚本真实循环执行的逻辑...')
        #self.Logger.info('sample1 run')

    def finish(self):
        print(f'Sample1脚本循环结束，返回主界面,方便其他脚本运行')
        #raise NotImplementedError('BaseScript-finish error-No Function Defined')