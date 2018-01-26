import os
import sys
import signal
import atexit
from TimeTask import TimeTask

class Daemonize:
    pidFile = '/tmp/timeTask.pid'
    stdin = '/tmp/timeTaskIn.log'
    stdout = '/tmp/timeTaskOut.log'
    stderr = '/tmp/timeTaskErr.log'
    configDir = None    #业务配置文件路径

    def __init__(self):
        self.timeTask = None
        Daemonize.configDir = os.getcwd()

    def start(self):
        '''
        在Unix/Linux操作系统提供了一个fork()函数，它非常特殊，调用一次，返回两次，
        因为操作系统将当前的进程（父进程）复制了一份（子进程），然后分别在父进程和子进程内返回。
        '''

        # 检测文件是否存在
        if os.path.exists(Daemonize.pidFile):
            with open(Daemonize.pidFile, 'r') as  f:
                pid = int(f.read())
                if pid > 0:
                    print("已经启动了一个服务！")
                    sys.exit()


        pid = os.fork()
        # 下面的逻辑将会被执行两次，主进程一次，子进程一次
        # 子进程的pid一定为0，父进程大于0, 如果杀死了父进程，那么子进程就变成了就变成了主进程，所以pid也就立即变为了0

        # 退出父进程，sys.exit()方法比os._exit()方法会多执行一些刷新缓冲工作
        if pid > 0:
            sys.exit()

        # 子进程默认继承父进程的工作目录，最好是变更到根目录，否则回影响文件系统的卸载
        os.chdir("/")
        # 子进程默认继承父进程的umask（文件权限掩码），重设为0（完全控制），以免影响程序读写文件
        os.umask(0)
        # 让子进程成为新的会话组长和进程组长
        os.setsid()
        # 注意了，这里是第2次fork，也就是子进程的子进程，我们把它叫为孙子进程
        _pid = os.fork()
        if _pid > 0:
            sys.exit()
        # 此时，孙子进程已经是守护进程了，接下来重定向标准输入、输出、错误的描述符(是重定向而不是关闭, 这样可以避免程序在 print 的时候出错)
        # 也就是说将print等输入输出信息存入下面指定的位置，因为没有终端显示了
        # 刷新缓冲区先，小心使得万年船
        sys.stdout.flush()
        sys.stderr.flush()
        # dup2函数原子化地关闭和复制文件描述符，重定向到/dev/nul，即丢弃所有输入输出
        with open(Daemonize.stdin, 'w+', 1) as f:
            os.dup2(f.fileno(), sys.stdin.fileno())
        with open(Daemonize.stdout, 'w+', 1) as f:
            os.dup2(f.fileno(), sys.stdout.fileno())
        with open(Daemonize.stderr, 'w+', 1) as f:
            os.dup2(f.fileno(), sys.stderr.fileno())

        # 把pid写到PID文件里面
        with open(Daemonize.pidFile, 'w', 1) as f:
            print(os.getpid(), file=f)

        # 程序退出的时候把pid文件移除
        atexit.register(lambda:self.delFile())


        # 注册信号
        self.registerSignal()

        # 运行执行程序
        self.timeTask = TimeTask(configDir=Daemonize.configDir)
        self.timeTask.run()

    def delFile(self):
        os.remove(Daemonize.pidFile)
        os.remove(Daemonize.stdin)
        os.remove(Daemonize.stdout)
        os.remove(Daemonize.stderr)

    def registerSignal(self):
        signal.signal(signal.SIGINT, self.reloadHandler) #注册一个重新加载配置文件的信号
        signal.signal(signal.SIGQUIT, self.stopHandler) #注册一个停止程序信号

    def stopHandler(self, signum, frame):
        sys.exit()

    def reloadHandler(self, signum, frame):
        self.timeTask.reload()


    # 下面处理第二次指令过来的时候
    def stop(self):
        # 检测文件是否存在
        if os.path.exists(Daemonize.pidFile):
            with open(Daemonize.pidFile, 'r') as  f:
                pid = f.read()
                os.kill(int(pid), signal.SIGQUIT) #发送停止信号
            print("停止信号已经发送，您可以通过查看pid("+pid+")是否还存在，来判断是否关停成功")
        else:
            print("程序未启动！不能停止")
            sys.exit()


    def reload(self):
        # 检测文件是否存在
        if os.path.exists(Daemonize.pidFile):
            with open(Daemonize.pidFile, 'r') as  f:
                pid = f.read()
                os.kill(int(pid), signal.SIGINT)  # 发送停止信号
            print("重新加载配置文件成功")
        else:
            print("程序未启动！不能停止")
            sys.exit()