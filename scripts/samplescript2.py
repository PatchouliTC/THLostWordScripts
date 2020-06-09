from core.script_base import ScriptBase
from . import load_img as li,TEMPLATEPATH,RESAULTPATH
from core.general import util
from time import sleep

class Sample2Script(ScriptBase):
    ScriptName='sample2'
    Description='SampleS2'
    ENABLERECORD=False
    
    def __init__(self):
        super().__init__(RESAULTPATH,__name__)

    def init(self):
        self.Logger.info('sample2 init')
        
    def start(self):
        raise NotImplementedError('BaseScript-start error-No Function Defined')

    def run(self):
        self.Logger.info('sample2 run')
        sleep(1)
        
    def finish(self):
        raise NotImplementedError('BaseScript-finish error-No Function Defined')