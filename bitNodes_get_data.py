import json
import threading
from queue import Queue
import requests
# 阿里巴巴的
# 此程序用于多线程获取bitnodes网络快照
# 1638979373
# 1-590
START_PAGE = 1
END_PAGE = 300
CRAWL_EXIT = False    # 采集网页页码队列是否为空的信号
URL_EXIT = False
proxy_ip = []


class ThreadCrawlUrl(threading.Thread):

    def __init__(self,threadName,pageQueue,urlQueue):
        threading.Thread.__init__(self)
        self.threadName=threadName   # 线程名
        self.pageQueue=pageQueue    # 页码队列
        self.urlQueue = urlQueue  # 数据队列
        # 请求报头
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36"}

    def run(self):
        print("启动 "+self.threadName)
        while not URL_EXIT:
            try:
                # 从dataQueue中获取每一个页码数字，先进先出
                # 可选参数block，默认值是True
                # 如果队列为空，block为True，会进入阻塞状态，直到队列有新的数据
                # 如果队列为空，block为False，会弹出一个Queue.empty 异常
                page = self.pageQueue.get(False)
                # 构建网页的URL地址
                url ="https://bitnodes.io/api/v1/snapshots/?page="+str(page)
                #proxies = getProxyIP.get_random_ip(proxy_ip)
                content = requests.get(url,headers = self.headers).text
                # 将提取content中的url
                dir_data = json.loads(content)

                # 放入队列
                for item_url in dir_data['results']:
                    # <class 'dict'>
                    # {'url': 'https://bitnodes.io/api/v1/snapshots/1632195964/', 'timestamp': 1632195964, 'total_nodes': 11414, 'latest_height': 701516}
                    self.urlQueue.put(item_url)
                    # print(item_url)
                    # print(type(item_url))
            except:
                pass
        print("结束"+self.threadName)


class ThreadCrawlSnapshots(threading.Thread):

    def __init__(self, threadName, urlQueue):
        threading.Thread.__init__(self)
        self.threadName = threadName   # 线程名
        self.urlQueue = urlQueue    # 页码队列
        # 请求报头
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36"}

    def run(self):
        print("启动 "+self.threadName)
        while not CRAWL_EXIT:
            try:
                # 从dataQueue中获取每一个页码数字，先进先出
                # 可选参数block，默认值是True
                # 如果队列为空，block为True，会进入阻塞状态，直到队列有新的数据
                # 如果队列为空，block为False，会弹出一个Queue.empty 异常
                url_dir = self.urlQueue.get(False)
                url = url_dir['url']
                # 构建网页的URL地址
                # proxies = getProxyIP.get_random_ip(proxy_ip)
                content = requests.get(url,headers = self.headers).text
                # 将抓取到的网页源码放入dataQueue队列中
                # print(content)
                dir_data = json.loads(content)
                writeFile(dir_data)
                # self.dataQueue.put(dir_data)
            except:
                pass
        print("结束"+self.threadName)


def writeFile(dir_data):

    file_name = "AllSnapshots1/" + str(dir_data['timestamp']) + ".json"
    with open(file_name, "w") as f:
        json.dump(dir_data, f)
    print("写入"+file_name+"文件")


def main(start_page,end_page):
    # global proxy_ip
    # proxy_ip = getProxyIP.get_IP()
    # 页码队列
    pageQueue = Queue(end_page-start_page+1)

    for i in range(start_page,end_page+1):
        pageQueue.put(i)

    urlQueue = Queue()

    get_url_workers = ['采集线程1号', '采集线程2号', '采集线程3号', '采集线程4号', '采集线程5号', '采集线程6号', '采集线程7号', '采集线程8号']
    url_list = []
    for threadName in get_url_workers:
        t = ThreadCrawlUrl(threadName,pageQueue, urlQueue)
        t.start()
        url_list.append(t)

    crawList = ['获取线程1号', '获取线程2号', '获取线程3号', '获取线程4号', '获取线程5号', '获取线程6号', '获取线程7号', '获取线程8号']

    # 创建、启动和存储三个采集线程
    threadCrawls = []
    for threadName in crawList:
        thread = ThreadCrawlSnapshots(threadName,urlQueue)
        thread.start()
        threadCrawls.append(thread)

    while not pageQueue.empty():
        pass
    global URL_EXIT
    URL_EXIT=True
    print("pageQueue为空")
    for thread in url_list:
        thread.join()

    while not urlQueue.empty():
        pass
    global CRAWL_EXIT
    CRAWL_EXIT = True
    print("urlQueue为空")
    for thread in threadCrawls:
        thread.join()


if __name__ == '__main__':
    main(START_PAGE, END_PAGE)