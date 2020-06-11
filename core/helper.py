# -*- coding: utf-8 -*-

import inspect
import json
import os
import platform
import subprocess
from enum import IntEnum
from importlib import import_module

from airtest import aircv

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
        scripts:可用脚本库
        planpath:任务json文件
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

            if plan['times'] > 0 and (plan['interval'] is None or plan['interval'] <= 0):
                planqueue.append({'type': PlanType.normal,
                                  'script': scripts[plan['script']],
                                  'times': plan['times']})

            elif plan['interval'] is not None and plan['interval'] > 0:
                planqueue.append({'type': PlanType.time,
                                  'script': scripts[plan['script']],
                                  'maxtimes': (
                                      plan['times'] if plan['times'] is not None and plan['times'] > 0 else -1),
                                  'currenttime': 0,
                                  'interval': plan['interval']})
    return device, cycletime, planqueue


def grant_adb_permission(device):
    """Grant permission to AirTest ADB

    To grant the executable permission to AirTest ADB in Darwin or Linux (included Linux ARM).

    Args:
        device: Android device object
    """

    if device is not None:
        logger.info('Device detected, handling adb permission...')
        # Import AirTest module as a object
        import airtest as _airtest_module

        # Get current Operating System platform
        os_platform = platform.system()
        logger.info(f'Operating System platform: {os_platform}')

        # Get AirTest module path from imported object `_airtest_module`
        airtest_path = os.path.dirname(_airtest_module.__file__)
        logger.debug(f'AirTest module path: {airtest_path}')

        if os_platform == 'Darwin':
            # if current OS is macOS, grant the permission to AirTest macOS ADB
            adb_path = f'{airtest_path}/core/android/static/adb/mac/adb'
            logger.info(f'AirTest ADB path: {adb_path}')

            subprocess.call(['chmod', '+x', adb_path])
        elif os_platform == 'Linux':
            # if current OS is Linux/Linux Arm, grant the permission to AirTest Linux ADB and Airtest Linux ARM ADB
            adb_path = f'{airtest_path}/core/android/static/adb/linux/adb'
            logger.info(f'AirTest ADB path: {adb_path}')
            adb_for_arm_path = f'{airtest_path}/core/android/static/adb/linux_arm/adb'
            logger.info(f'AirTest ADB path: {adb_for_arm_path}')

            subprocess.call(['chmod', '+x', adb_path])
            subprocess.call(['chmod', '+x', adb_for_arm_path])
