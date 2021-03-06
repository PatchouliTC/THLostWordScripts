# -*- coding: utf-8 -*-

import logging
import signal
import sys

from airtest.core.android.adb import ADB
from airtest.core.api import connect_device
from airtest.core.api import device as G
from airtest.utils.logger import set_root_logger_level

from core import setup_log
from core.helper import make_plan, grant_adb_permission
from core.plan_manager import planmanager as pm
from core.setting import Settings as ST

logger = setup_log()


def cancel_handler(signal, frame):
    ST.MANUAL_CANCEL = True
    logger.info('人工终止')
    if G:
        ADB().disconnect()
    ADB().kill_server()
    sys.exit(0)


def setup(debugmode: bool = False):
    """
        setup project if cli give run command
        :param debugmode:Set logger level debug or not
        :return :bool
    """

    signal.signal(signal.SIGINT, cancel_handler)
    signal.signal(signal.SIGTERM, cancel_handler)

    # LOG SET:DEBUG OR NOT
    if debugmode:
        set_root_logger_level(logging.DEBUG)
    else:
        set_root_logger_level(logging.INFO)
        ST.LOG_LEVLE = logging.INFO

    device, cycletime, plans = make_plan()

    grant_adb_permission(device)

    planmanager = pm()

    if not planmanager.set_plan(plans, cycletime):
        logger.info('无计划任务，直接终止')
        return False

    # Droid Connection
    if not device:
        logger.info('未定义目标设备，搜寻并返回可用android设备...')
        try:
            devices = ADB().devices(state="device")
            if len(devices) == 0:
                raise Exception
        except:
            logger.info('无可用android设备')
            ADB().kill_server()
            return False
        print(f'可用设备列表---》》》')
        for d in range(len(devices)):
            print(f"{d + 1}.{devices[d][0]}")
        num = int(input('输入希望链接的设备编码[1,2,3,4...]:'))
        try:
            device = devices[num - 1][0]
        except:
            logger.info('非法输入,选择第一个设备作为可用设备')
            device = devices[0][0]

        instance = connect_device(f'android:///{device}')
    else:
        logger.info(f"尝试链接设备[{device}]")
        try:
            instance = connect_device(device)
        except Exception as e:
            logger.error(f'连接发生错误({str(e)})')
            instance = None

    if instance:
        logger.info(f"连接成功，开始执行计划任务")
        planmanager.run_plans()
        logger.info('计划执行结束')
        if ST.MANUAL_CANCEL:
            return True
        try:
            ADB().disconnect()
        except:
            pass
    else:
        logger.error('连接失败')

    ADB().kill_server()
    return True


def generate_device_url(args):
    print("not finished")
