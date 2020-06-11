# -*- coding: utf-8 -*-

import logging
import sys

from airtest.core.android.adb import ADB
from airtest.core.api import connect_device
from airtest.utils.logger import set_root_logger_level

from core.helper import make_plan, grant_adb_permission
from core.logger import init_logging
from core.plan_manager import planmanager as pm

set_root_logger_level(logging.INFO)

logger = init_logging(level=logging.INFO)

if __name__ == "__main__":

    device, cycletime, plans = make_plan()

    grant_adb_permission(device)

    planmanager = pm()

    if not planmanager.set_plan(plans, cycletime):
        logger.info('无计划任务，直接终止')
        sys.exit(0)

    if not device:
        logger.info('未定义目标设备，搜寻并返回可用android设备...')
        try:
            devices = ADB().devices(state="device")
            if len(devices) == 0:
                raise Exception
        except Exception as berr:
            logger.info('无可用android设备,结束')
            ADB().kill_server()
            sys.exit(0)
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
        instance = connect_device(device)
    if instance:
        logger.info(f"连接成功，开始执行计划任务")
        planmanager.run_plans()
    else:
        logger.error('连接失败')
    logger.info('计划执行结束')
    ADB().kill_server()
