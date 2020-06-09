import os
import sys
import logging
from apscheduler.schedulers.background import BackgroundScheduler

from airtest.utils.logger import set_root_logger_level
from airtest.core.android.adb import ADB
from airtest.core.api import connect_device

set_root_logger_level(logging.INFO)

from core.helper import make_plan
from core.plan_manager import planmanager as pm
from core.logger import init_logging

logger=init_logging(level=logging.INFO)

if __name__ == "__main__":

    device,cycletime,plans=make_plan()


    planmanager=pm()
    if not planmanager.set_plan(plans,cycletime):
        logger.info('None Plans,no more running')
        sys.exit(0)
    deviceavilable=False
    logger.info('Searching Avilable Android Devices...')
    try:
        devices = ADB().devices(state="device")
        if len(devices) == 0:
            raise Exception
        for dev in devices:
            if device==dev[0]:
                logger.debug('Find Plan Device')
                deviceavilable=True
                break
    except Exception as berr:
        logger.info('No Useable Device,quit')
        ADB().kill_server()
        sys.exit(0)
    
    logger.info('Not find plan device in useable devices')
    print(f'Avilable Devices---》》》')
    for d in range(len(devices)):
        print(f"{d+1}.{devices[d][0]}")
    num=int(input('Enter Num to select:'))
    try:
        device=devices[num-1][0]
    except:
        logger.info('Error input,select default')
        device=devices[0][0]

    connect_device(f'android:///{device}')

    planmanager.run_plans()

    logger.info('Plan_Finish')
    ADB().kill_server()


    





