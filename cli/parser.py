import argparse

def get_parser():
    ap=argparse.ArgumentParser()

    sp=ap.add_subparsers(dest='action',description='启动或生成设备地址')
    ap_gen=sp.add_parser('gd',help='设备链接地址生成')
    ap_run=sp.add_parser('run',help='运行项目')

    runner_parser(ap_run)
    gener_parser(ap_gen)

    return ap

def gener_parser(gen=None):
    if not gen:
        gen=argparse.ArgumentParser()
    sp=gen.add_subparsers(dest='device',help='设备平台',description='生成指定平台链接')

    gen_a=sp.add_parser('droid',help='安卓设备')
    gen_i=sp.add_parser('ios',help='IOS设备')
    gen_w=sp.add_parser('win',help='Windows窗体')
    gen_a_parser(gen_a)
    gen_i_parser(gen_i)
    gen_w_parser(gen_w)

    return gen


def runner_parser(run=None):
    if not run:
        run=argparse.ArgumentParser()

    run.add_argument('-d','--debug',help='以DEBUG模式运行',action='store_true')

    return run

def gen_a_parser(gen):

    gen.add_argument('-hp','--hostp',help='主机地址-格式[host:port]-默认[127.0.0.1:5037]'
                        ,dest='host',nargs='?',type=str,default='127.0.0.1:5037')
    gen.add_argument('-s','--serino',help='目标设备地址或序列码[必填]'
                        ,dest='no',nargs='?',type=str,required=True)
    
    return gen
    
def gen_i_parser(gen):

    gen.add_argument('-hp','--hostp',help='目标设备地址-格式[host:port]-默认[localhost:8100]'
                        ,dest='host',nargs='?',type=str,default='127.0.0.1:8100') 
    return gen

def gen_w_parser(gen):

    gen.add_argument('-hd','--handle',help='目标窗口句柄-无参数默认为桌面'
                        ,dest='handle',nargs='?',type=str,default='')
    gen.add_argument('-t','--title',help='目标窗口标题-正则匹配'
                        ,dest='title',nargs='?',type=str,default='')

    return gen
