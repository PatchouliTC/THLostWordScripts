import os
from core.script_base import ScriptBase
from . import load_img as li,TEMPLATEPATH,RESAULTPATH
from core.general import util
import core.shot_record as Record

#image save at scripts/template
#use li to load scriptimage--> image=li(r"t112521512.png")
class SampleScript(ScriptBase):
    ScriptName='sample1'
    Description='SampleS1'
    ENABLERECORD=False

    def __init__(self):
        super().__init__(RESAULTPATH,__name__)

    def run(self):
        self.Logger.info('sample1 run')

    def finish(self):
        raise NotImplementedError('BaseScript-finish error-No Function Defined')