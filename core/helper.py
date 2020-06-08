import os
import inspect
from importlib import import_module
from .script_base import ScriptBase
from airtest import aircv
import json
from enum import IntEnum
from .logger import get_logger

logger=get_logger(__name__)

def load_img(fpn):
    try:
        return aircv.imread(fpn)
    except:
        return None

def load_scripts(modulepath:str='scripts'):
    scriptinstance=dict()
    for f in os.listdir(modulepath):
        if f.endswith(".py"):
            if f!='__init__.py':
                t=f.split('.')[0]
                for _,cla in inspect.getmembers(import_module(f'{modulepath}.{t}'),inspect.isclass):
                    if issubclass(cla,ScriptBase) and cla.ScriptName is not None:
                        scriptinstance[cla.ScriptName]=cla()
    return scriptinstance

def load_plan(planpath:str='plan.json'):
    try:
        with open(planpath,'r',encoding='utf-8') as f:
            data=json.load(f)
        return data
    except Exception as e:
        logger.error(f'Failed when try open plan json file({str(e)})')
        return None

class PlanType(IntEnum):
    normal=1,
    time=2

def make_plan(scripts:dict=load_scripts(),planpath:str='plan.json'):
    """
        装载并制定执行计划
        scripts:可用脚本库
        planpath:任务json文件
    """
    plans=load_plan(planpath)
    if plans is None:
        return None
    device=plans['device'] if plans['device'] is not None and len(plans['device'])>1 else ""
    cycletime=plans['cycle_times'] if plans['cycle_times'] is not None else 0

    planqueue=[]
    logger.info(f"Finding {len(plans['plan'])} plans...")
    for plan in plans['plan']:
        if plan['enable'] and plan['script'] in scripts:

            if plan['times']>0 and (plan['interval'] is None or plan['interval']<=0):
                planqueue.append({'type':PlanType.normal,
                                    'script':scripts[plan['script']],
                                    'times':plan['times']})

            elif plan['interval'] is not None and plan['interval']>0:
                planqueue.append({'type':PlanType.time,
                                        'script':scripts[plan['script']],
                                        'maxtimes':(plan['times'] if plan['times'] is not None and plan['times']>0 else -1),
                                        'currenttime':0,
                                        'interval':plan['interval']})
    return device,cycletime,planqueue