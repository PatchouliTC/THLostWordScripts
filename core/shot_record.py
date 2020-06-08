import os
import time
from airtest.core.api import snapshot

class Record(object):

    def __init__(self, path,logger):
        self.path=path
        self.logger=logger
        self.fail_count = 0
        self.success_count = 0
        self.all_ticks = []
        self.start_ticks = time.time()
        self.init_ticks = time.time()
            
    #开始记录
    def StartRecord(self):
        self.start_ticks = time.time()
    #结束记录并打印结果
    def EndRecord(self, success):
        if success:
            self.success_count += 1
        else:
            self.fail_count += 1
            
        ticks = time.time() - self.start_ticks
        all_ticks = time.time() - self.init_ticks
        self.logger.info(f'average sec:{str(all_ticks/(self.success_count + self.fail_count))} this time:{str(ticks)}')
        self.logger.info(f'total sec:{str(self.success_count + self.fail_count)} success:{str(self.success_count)} fail:{str(self.fail_count)}')

    def RecordResult(self):
        filename = os.path.join(self.path, time.strftime("%Y%m%d-%H%M%S", time.localtime()) + ".jpg")
        self.logger.info(f"image save at {filename}")
        snapshot(filename, "result snapshot", 99)
