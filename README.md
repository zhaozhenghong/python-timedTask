# python-timedTask

> python之定时任务小工具

## 工具说明
    1、本工具是学习python时制作，会有很多不理想的地方（不建议传播），一般简单的需求还是可以使用的。
    2、本程序是以守护进程多线程的方式执行config.json里面的需要定时执行的URL
    3、本程序使用python3开发，python2未做测试
    4、依赖pycurl库
    5、可以修改config.py的内容，然后使用 reload热更新采集配置信息
    6、定时任务如果没有返回 'success' 则会尝试执行3次，如果3此都没有返回success，则会输出一个错误信息
    7、文件的调试和错误信息保存在如下位置：
        pid保存位置（无用）--pidFile = '/tmp/timeTask.pid'
        程序输入信息保存位置（无用）--stdin = '/tmp/timeTaskIn.log'
        程序业务逻辑输出信息保存位置 --stdout = '/tmp/timeTaskOut.log'
        程序运行时系统发生错误信息保存位置 --stderr = '/tmp/timeTaskErr.log'

## config.json配置文件格式说明
``` bash
        #时间格式表示每天执行的任务
        #日期格式表示某天执行的任务
        {
            "itme1": {
                "url": "需要执行的URL",
                "times": ["08:40:00","08:50:00",...,"22:50:00"]
            },
            "itme2": {
                "url": "http://www.yccaiji.com/?a=b&c=t&f=h",
                "times": ["2018-01-01 08:40:00","2019-01-01 08:50:00",...,"2020-01-01 22:50:00"]
            }
        }
```

## 使用说明
``` bash
        $ python3 Main.py start  #启动服务
        $ python3 Main.py stop   #停止服务
        $ python3 Main.py reload #重新加载配置
        $ python3 Main.py help   #帮助说明信息
```

