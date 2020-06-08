import os
from core.logger import get_script_logger,logging
import core.shot_record as Record

class ScriptBase(object):
    """
        ScriptTemplate
        Create your Script By inheritance this Object
    """
    ScriptName=None
    Description=''
    ENABLERECORD=False
    BASEPATH=None
    Logger=None
    def __init__(self,base:str=None,module:str=__name__,level:int=logging.INFO):
        """
            base:对应脚本的记录保存根目录
            module：脚本模块路径，用于获取logger
            level：该脚本日志记录消息过滤等级
        """
        if base is not None:
            self.BASEPATH=self.get_record_path(base)
        self.Logger=get_script_logger(module,os.path.join(self.BASEPATH,'result.log'),level)
        if self.ENABLERECORD:
            self.record=Record.Record(self.BASEPATH,self.Logger)
        else:
            self.record=None
        super().__init__()

    def run(self):
        raise NotImplementedError('BaseScript-main error-No Function Defined')

    def finish(self):
        raise NotImplementedError('BaseScript-finish error-No Function Defined')

    @classmethod
    def get_record_path(cls,base):
        if cls.ScriptName is None:
            return base
        else:
            path=os.path.join(base,cls.ScriptName)
            if not os.path.exists(path):
                os.makedirs(path)
            return path

    def __repr__(self):
        return f'{self.ScriptName}({self.Description})' if self.ScriptName is not None else "BaseScript--NoWorkSet!"