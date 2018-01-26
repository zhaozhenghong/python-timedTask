import json
import time
import threading
import pycurl
import io



class TimeTask:
    configDir = None    #配置文件目录
    configJson = None
    tLists = {} # 每天定时任务 {'HMS':[url1,url2,...]}
    dLists = {} # 某天定时任务 {'YmdHMS':[url1,url2,...]}

    def __init__(self, configDir):
        TimeTask.configDir = configDir

    def run(self):
        self.load()
        while True:
            ls = time.localtime(time.time())
            tTime = time.strftime('%H%M%S',ls)
            dTime = time.strftime('%Y%m%d%H%M%S',ls)
            if TimeTask.tLists.__contains__(tTime):
                # 创建线程执行URL
                lists = TimeTask.tLists[tTime]
                for url in lists:
                    t = threading.Thread(target=self.curlRun,args=(url,tTime,))
                    t.start()
            if TimeTask.dLists.__contains__(dTime):
                lists = TimeTask.dLists[dTime]
                for url in lists:
                    t = threading.Thread(target=self.curlRun, args=(url,dTime,))
                    t.start()
            #print(tTime)
            #print(dTime)
            time.sleep(1)

    def reload(self):
        self.load()

    def load(self):
        with open(TimeTask.configDir+'/config.json', 'r' , encoding='utf-8') as f:
            TimeTask.configJson = json.load(f)
        for itme in TimeTask.configJson:
            url = TimeTask.configJson[itme]['url']
            times = TimeTask.configJson[itme]['times']
            for t in times:
                if len(t) == 8: # 时间格式
                    t = t.replace(':','')
                    if TimeTask.tLists.__contains__(t) :
                        TimeTask.tLists[t].append(url)
                    else:
                        TimeTask.tLists[t] = [url]
                else:   # 日期格式
                    t = t.replace('-', '')
                    t = t.replace(' ', '')
                    t = t.replace(':', '')
                    if TimeTask.dLists.__contains__(t):
                        TimeTask.dLists[t].append(url)
                    else:
                        TimeTask.dLists[t] = [url]
        #print(TimeTask.tLists)
        #print(TimeTask.dLists)

    def curlRun(self, url, timeStr):
        try:
            i = 1
            while True:
                buffer = io.BytesIO()
                c = pycurl.Curl()  # 创建一个curl对象
                c.setopt(pycurl.URL, url)  # 指定请求的URL
                c.setopt(pycurl.WRITEDATA, buffer)  # 将返回的HTML内容定向到fileobj文件对象
                c.perform()
                c.close()
                body = buffer.getvalue().decode('iso-8859-1')
                if body.lower() == 'success':
                    break
                elif i == 3:
                    print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+'执行采集时间为【'+timeStr+'】的URL【'+url+'】返回了异常信息：'+body+'\n\n')
                    break
                i += 1
        except BaseException as e:
            print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(
                time.time())) + '执行采集时间为【' + timeStr + '】的URL【' + url + '】发生了程序异常错误，错误信息为：' + str(e) + '\n\n')
        finally:
            return True




# obj = TimeTask()
# obj.run()