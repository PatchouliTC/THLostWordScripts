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

        if plans:
            self.plans=plans
        self.cycletime=cycletime if cycletime >0 else self.cycletime

        if self.cycletime<=0:
            logger.info(f'错误的总循环次数(定义值:{self.cycletime})')
            return False
        if len(self.plans)<=0:
            logger.info(f'没有计划被导入(计划总数:{len(self.plans)})')
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
        logger.info(f"加载了{norp+timp}个任务单元(循环任务:{norp},定时任务:{timp}),将循环执行{self.cycletime}轮")
        return True

    def run_plans(self):
        for i in range(self.cycletime):
            logger.info(f"第{i+1}次循环---->>>")
            for p in self.plans:
                if p['type']==PlanType.normal:
                    for t in range(p['times']):
                        #check need run timeplan
                        self.run_time_plan()
                        logger.debug(f"尝试执行任务:{p['script'].ScriptName}(第{t}次)")
                        try:
                            if not p['Script'].should_run():
                                logger.info(f"{p['script'].ScriptName}提前终止(已运行总数:{t-1})")
                                break
                            #上一次执行的脚本为空，直接保存当前脚本并start
                            if not self.lastrunplan:
                                self.lastrunplan=p['Script']
                                p['Script'].start()
                            else:
                                #如果之前脚本不是当前脚本，调用之前脚本的结束方法并调用当前脚本的启动方法,之后保存当前执行脚本
                                if self.lastrunplan.ScriptName!=p['Script'].ScriptName:
                                    self.lastrunplan.finish()
                                    p['Script'].start()
                                    self.lastrunplan=p['Script']
                            #执行当前脚本循环方法
                            p['script'].run()
                        except Exception as e:
                            logger.error(f"在第{t}次执行{p['script'].ScriptName}脚本时发生错误({str(e)})")
        #所有循环任务和主题大循环次数均运行完毕，查看时间任务，如果还有时间任务未完成，
        logger.info(f"所有循环任务执行完毕，侦测定时任务>>>>>>")
        while len(self.scheduler.get_jobs())>0:
            logger.debug(f"{len(self.scheduler.get_jobs())} plans left")
            tp=self.time_plan.get()
            logger.info(f'尝试执行{tp.ScriptName}')
            try:
                tp.run()
            except Exception as e:
                logger.error(f"任务{tp['script'].ScriptName}执行中发生异常({str(e)})")
                
                
    def run_time_plan(self):
        while not self.time_plan.empty():
            tp=self.time_plan.get(timeout=1)
            logger.info(f'尝试执行{tp.ScriptName}')
            try:
                if not tp.should_run():
                    logger.info(f"{tp.ScriptName}提前终止")
                    self.remove_time_job(tp.ScriptName)
                    return
                if not self.lastrunplan:
                    self.lastrunplan=tp
                    tp.start()
                else:
                #如果之前脚本不是当前脚本，调用之前脚本的结束方法并调用当前脚本的启动方法
                    if self.lastrunplan.ScriptName!=tp.ScriptName:
                        self.lastrunplan.finish()
                        tp.start()
                        self.lastrunplan=tp
                tp.run()
            except Exception as e:
                logger.error(f"定时任务{tp['script'].ScriptName}发生异常({str(e)})")


    def clear_time_jobs(self):
        self.scheduler.remove_all_jobs()
        self.time_plan.queue.clear()
        logger.info('清理完毕所有时间任务队列信息')

    def remove_time_job(self,name:str):
        try:
            self.scheduler.remove_job(name)
        except:
            logger.debug("No this Script Plan")
        return
    
    def planexcute(self,plan):     
        #将函数添加到时间任务队列
        self.time_plan.put(plan['script'])
        #该时间任务执行次数+1
        plan['currenttime']+=1
        logger.info(f"时间任务{plan['script'].ScriptName}已添加进计划单，将在下一次执行任务时执行")
        #excute limit
        if plan['maxtimes']>0 and plan['currenttime']>=plan['maxtimes']:
            logger.debug(f"任务{plan['script'].ScriptName}已达计划次数上限，取消该任务")
            self.remove_time_job(plan['script'].ScriptName)
            return