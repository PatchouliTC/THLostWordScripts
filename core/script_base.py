import os
from core.logger import get_script_logger,logging,ROOT
import core.shot_record as Record

class ScriptBase(object):
    """
        ScriptTemplate
        Create your Script By inheritance this Object
    """
    ScriptName=None#脚本名称 不得重复 同时用于plan.json定位
    Description=''#无用【看心情
    ENABLERECORD=False#是否启用记录统计功能，如果不启动self.record将为None不进行初始化
    RESAULTPATH=None#脚本对应的基础路径，将用于保存log和记录图片等内容
    Logger=None#脚本挂载的日志模块
    def __init__(self,base:str=None,module:str=__name__,level:int=logging.INFO):
        """
            Script类初始化
            :param templatebase:脚本的图片根目录
            :param base:对应脚本的记录保存根目录
            :param module：脚本模块路径，用于获取logger
            :param level：该脚本日志记录消息过滤等级
        """
        if base:
            self.RESAULTPATH=self.get_path(base)
        else:
            self.RESAULTPATH=ROOT
        self.Logger=get_script_logger(module,os.path.join(self.RESAULTPATH,'result.log'),level)
        if self.ENABLERECORD:
            self.record=Record.Record(self.RESAULTPATH,self.Logger)
        else:
            self.record=None
        super().__init__()

    def start(self):
        """
            start方法，当该脚本相对于前一次运行的脚本不是同一个脚本的时候将会执行的内容
        """
        raise NotImplementedError('BaseScript-start error-No Function Defined')
    
    def run(self):
        """
            run方法，该脚本具体循环的执行方式，对于循环顺序执行脚本该方法在没有其他脚本计划
            加入的时候将会循环执行
        """
        raise NotImplementedError('BaseScript-main error-No Function Defined')

    def finish(self):
        """
            finish方法，当该脚本下一轮不为该脚本循环的时候将会执行一次
        """
        raise NotImplementedError('BaseScript-finish error-No Function Defined')
    
    def start_record(self):
        """
            开始记录
        """
        if self.record:
            self.record.StartRecord()
    
    def end_record(self,success:bool):
        """
            终止记录
        """
        if self.record:
            self.record.EndRecord(success)

    def write_result(self):
        """
            进行结果记录
        """
        if self.record:
            self.record.RecordResult()
    @classmethod
    def should_run(cls):
        """
            该脚本是否继续执行
            按需进行重写
            返回值为True表示继续计划
            False表示提前终止计划
        """
        return True

    @classmethod
    def get_path(cls,base):
        if cls.ScriptName is None:
            return base
        else:
            path=os.path.join(base,cls.ScriptName)
            if not os.path.exists(path):
                os.makedirs(path)
            return path

    def __repr__(self):
        return f'{self.ScriptName}({self.Description})' if self.ScriptName is not None else "BaseScript--NoWorkSet!"