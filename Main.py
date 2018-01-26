import sys
from Daemonize import Daemonize

argvs = sys.argv
if len(argvs) != 2 :
    sys.stdout.write('''
    指令错误，可以使用的指令有：
    start  #启动服务
    stop   #停止服务
    reload #重新加载配置
    help   #帮助说明信息
    \n''');
    sys.exit()

if argvs[1] == 'start':
    obj = Daemonize()
    obj.start()
elif argvs[1] == 'reload':
    obj = Daemonize()
    obj.reload()
elif argvs[1] == 'stop':
    obj = Daemonize()
    obj.stop()
elif argvs[1] == 'help':
    print('''
    1、本程序使用python3开发，python2未做测试
    2、依赖pycurl库
    3、可以修改config.py的内容，然后使用 reload热更新采集配置信息
    4、定时任务如果没有返回 'success' 则会尝试执行3次，如果3此都没有返回success，则会输出一个错误信息
    5、文件的调试和错误信息保存在如下位置：
        pidFile = '/tmp/timeTask.pid'
        stdin = '/tmp/timeTaskIn.log'
        stdout = '/tmp/timeTaskOut.log'
        stderr = '/tmp/timeTaskErr.log'
    \n''')
    sys.exit()
else:
    sys.stdout.write('''
        指令错误，可以使用的指令有：
        start  #启动服务
        stop   #停止服务
        reload #重新加载配置
        help   #帮助说明信息
        \n''')
    sys.exit()