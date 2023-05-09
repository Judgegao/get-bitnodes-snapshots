import random
import requests
from lxml import etree
import json
import time
from tqdm import tqdm


# 解析网页，并得到网页中的代理IP
def get_proxy(html):
    List = []
    # 对获取的页面进行解析
    selector = etree.HTML(html)
    print(selector)
    tabel=selector.xpath('//table[@class="fl-table"]/tbody/tr')
    # print(tabel)
    for i in tabel:
        # print(i)
        ip=i.xpath("./td/text()")[0]#.encode('utf-8')
        http_=i.xpath("./td/text()")[1]
        if 'HTTPS'not in http_ and'HTTP' in http_:
            ip_=str(ip).replace('b','')
            List.append(ip)
    useful_ip = test_proxies(List)
    return useful_ip



def get_random_ip(ip_list):
    proxy_list = []
    for ip in ip_list:
        proxy_list.append('http://' + ip)
    proxy_ip = random.choice(proxy_list)
    proxies = {'http': proxy_ip}
    return proxies


# 验证已得到IP的可用性，本段代码通过访问百度网址，返回的response状态码判断（是否可用）。
def test_proxies(List):
    proxies = List
    url = "https://www.baidu.com/"
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
        }
    normal_proxies = []
    count = 1
    for proxy in proxies:
        # print(proxy)
        print("第%s个。。" % count)
        count += 1
        try:
            response = requests.get(url, headers=header, proxies={"http": proxy}, timeout=1)
            if response.status_code == 200:
                print("该代理IP可用：", proxy)
                normal_proxies.append(proxy)
            else:
                print("该代理IP不可用：", proxy)
        except Exception:
            print("该代理IP无效：", proxy)
            pass
    # print(normal_proxies)
    return normal_proxies


# 获取代理IP
def get_IP():
    url = "http://www.xiladaili.com/gaoni/"

    # 获取100页的匿名代理IP，每一页是50个
    # for j in tqdm(range(1,100)):
    #     time.sleep(1)
    #     url=url_+str(j)+'/'
    #
    #     header = {
    #         "User-Agent":
    #             "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
    #     }
    #
    #     response = requests.get(
    #         url,
    #         headers=header,
    #     )
    #
    #     get_proxy(response.text)

    header = {
        "User-Agent":
            "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
    }

    response = requests.get(
        url,
        headers=header,
    )
    useful_ip = get_proxy(response.text)
    return useful_ip

