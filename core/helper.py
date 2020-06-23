# -*- coding: utf-8 -*-

import inspect
import json
import os
import platform
import subprocess
from enum import IntEnum
from importlib import import_module

from airtest import aircv
from airtest.core.android.adb import ADB

from .logger import get_logger
from .script_base import ScriptBase

logger = get_logger(__name__)


def load_img(fpn):
    try:
        return aircv.imread(fpn)
    except Exception as e:
        logger.error(f'Load Image Failed({str(e)}),FileTarget is {fpn}')
        return None


def load_scripts(modulepath: str = 'scripts'):
    scriptinstance = dict()
    for f in os.listdir(modulepath):
        if f.endswith(".py"):
            if f != '__init__.py':
                t = f.split('.')[0]
                for _, cla in inspect.getmembers(import_module(f'{modulepath}.{t}'), inspect.isclass):
                    if issubclass(cla, ScriptBase) and cla.ScriptName is not None:
                        scriptinstance[cla.ScriptName] = cla()
    return scriptinstance


def load_plan(planpath: str = 'plan.json'):
    try:
        with open(planpath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except Exception as e:
        logger.error(f'Failed when try open plan json file({str(e)})')
        return None


class PlanType(IntEnum):
    normal = 1,
    time = 2


def make_plan(scripts=None, planpath: str = 'plan.json'):
    """
        装载并制定执行计划
        :param scripts:可用脚本库
        :param planpath:任务json文件
    """
    if scripts is None:
        scripts = load_scripts()
    plans = load_plan(planpath)
    if plans is None:
        return None
    device = plans['device'] if plans['device'] is not None and len(plans['device']) > 1 else ""
    cycletime = plans['cycle_times'] if plans['cycle_times'] is not None else 0

    planqueue = []
    logger.info(f"读取到 {len(plans['plan'])} 个计划...")
    for plan in plans['plan']:
        if plan['enable'] and plan['script'] in scripts:

            if plan['times'] > 0 and (not plan['interval'] or plan['interval'] <= 0):
                planqueue.append({'type': PlanType.normal,
                                  'script': scripts[plan['script']],
                                  'times': plan['times']})

            elif plan['interval'] and plan['interval'] > 0:
                planqueue.append({'type': PlanType.time,
                                  'script': scripts[plan['script']],
                                  'maxtimes': (
                                      plan['times'] if plan['times'] is not None and plan['times'] > 0 else -1),
                                  'currenttime': 0,
                                  'interval': plan['interval']})
    return device, cycletime, planqueue


def grant_adb_permission(device):
    """给AirTest ADB赋予权限

    为Darwin (macOS)和Linux，以及Linux ARM系统下的AirTest ADB赋予可执行权限.

    :param device: Android设备对象
    """

    if device is not None:
        logger.info('检测到已接入的设备，正在处理AirTest ADB权限...')

        # 获取当前操作系统的平台名称
        system = platform.system()
        logger.info(f'当前操作系统: {system}')

        # 通过AirTest的ADB静态方法获取ADB路径
        adb_path = ADB.builtin_adb_path()
        logger.debug(f'AirTest ADB路径: {adb_path}')

        if system == 'Darwin' or system == 'Linux':
            # if current OS is macOS, Linux or Linux Arm, grant the permission to AirTest ADB
            subprocess.call(['chmod', '+x', adb_path])
