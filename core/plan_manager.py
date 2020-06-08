import os
from queue import Queue
from apscheduler.schedulers.background import BackgroundScheduler
from core.helper import make_plan,PlanType
from core.logger import get_logger

logger=get_logger(__name__)

class planmanager(object):
    def __init__(self):
        self.plans=dict(),
        self.cycletime=0
        self.lastrunplan=None
        self.time_plan=Queue()
        self.scheduler=BackgroundScheduler()
        self.scheduler.start()

    def set_plan(self,plans:dict=dict(),cycletime:int=0):
        #clear old timeplans
        self.clear_time_jobs()

        if plans is not None:
            self.plans=plans
        self.cycletime=cycletime if cycletime >0 else self.cycletime

        if self.cycletime<=0:
            logger.info(f'No cycle Time(define time:{self.cycletime})')
            return False
        if len(self.plans)<=0:
            logger.info(f'No plan imort(plan num:{len(self.plans)})')
            return False
        
        norp=0
        timp=0
        for plan in self.plans:
            #add time plans
            if plan['type']==PlanType.time:
                timp+=1
                self.scheduler.add_job(func=self.planexcute,trigger='interval',id=plan['script'].ScriptName,seconds = plan['interval'],args=[plan,])
            else:
                norp+=1
        logger.info(f"Loading {norp+timp} plans(normal:{norp},time:{timp}),expect run {self.cycletime} times")
        return True

    def run_plans(self):
        for i in range(self.cycletime):
            logger.info(f"{i+1}th cycle---->>>")
            for p in self.plans:
                if p['type']==PlanType.normal:
                    for t in range(p['times']):
                        self.run_time_plan()
                        logger.info(f"Try Run Normal plan {p['script'].ScriptName}({t}th Run)")
                        try:
                            #如果之前脚本不是当前脚本，调用之前脚本的结束方法并调用当前脚本的启动方法
                            if self.lastrunplan is None or self.lastrunplan.ScriptName!=p['Script'].ScriptName:
                                if self.lastrunplan is not None:
                                    self.lastrunplan.finish()
                                p['Script'].start()
                                self.lastrunplan=p['Script']
                            p['script'].run()
                        except Exception as e:
                            logger.error(f"{t}th run {p['script'].ScriptName} happend error({str(e)})")
        logger.info(f"Static Queue Run Finish,run only time plan>>>>>>")
        while len(self.scheduler.get_jobs())>0:
            logger.debug(f"{len(self.scheduler.get_jobs())} time plan left")
            tp=self.time_plan.get()
            logger.info(f'Try Run Time plan {tp.ScriptName}')
            try:
                tp.run()
            except:
                logger.error(f"Run Time Plan {tp['script'].ScriptName} happend error")
                
                
    def run_time_plan(self):
        while not self.time_plan.empty():
            tp=self.time_plan.get(timeout=1)
            logger.info(f'Try Run Time plan {tp.ScriptName}')
            try:
                #如果之前脚本不是当前脚本，调用之前脚本的结束方法并调用当前脚本的启动方法
                if self.lastrunplan is None or self.lastrunplan.ScriptName!=tp.ScriptName:
                    if self.lastrunplan is not None:
                        self.lastrunplan.finish()
                    tp.start()
                    self.lastrunplan=tp
                tp.run()
            except:
                logger.error(f"Run Time Plan {tp['script'].ScriptName} happend error")


    def clear_time_jobs(self):
        self.scheduler.remove_all_jobs()
        self.time_plan.queue.clear()

    def planexcute(self,plan):     
        #add time script cls
        self.time_plan.put(plan['script'])
        plan['currenttime']+=1
        logger.info(f"{plan['script'].ScriptName} add into queue,nexttime it will run")
        #excute limit
        if plan['maxtimes']>0 and plan['currenttime']>=plan['maxtimes']:
            try:
                logger.debug(f"Run Times at Max Value,remove {plan['script'].ScriptName} plan next time")
                self.scheduler.remove_job(plan['script'].ScriptName)
            except:
                logger.debug("No this Script Plan")
            return