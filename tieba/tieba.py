# -*- coding: UTF-8 -*-
'''
 @description: 百度贴吧邮箱爬虫
 @program: spider
 @author: 284668461@qq.com
 @create: 2020-03-12 15:25
'''
import requests
from spiders import headers as h
import re
import time
from pyquery import PyQuery as pq

'''
 @Description  写入到txt
 @Author 284668461@qq.com
 @Date 2020/3/21 9:47 
'''
def write(list):

    # 去重
    newList = []
    for id in list:
        if id not in newList:
            newList.append(id)


    filePath = r'D:\Email.txt'
    f = open(filePath, 'a')
    for i in newList:
        f.writelines(i)
        f.write('\n')
    f.close()


'''
 @Description  请求url
 @Author 284668461@qq.com
 @Date 2020/3/21 9:47 
'''
def getUrl(url,max_behot_time=0):

    headers = {
        "user-agent":h.getHeader2()
    }


    res = requests.get(url,headers=headers)

    return filter(res.text)


'''
 @Description  过滤
 @Author 284668461@qq.com
 @Date 2020/3/12 15:54 
'''
def filter(dom):

    # 提取数据
    email = re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", dom)
    print(email)
    write(email)



if __name__ == '__main__':


    url = "https://tieba.baidu.com/p/5858684223"
    headers = {
        "User-Agent":h.getHeader2()
    }

    res = requests.post(url,headers = headers)
    html = res.text.replace('<?xml version="1.0" encoding="UTF-8"?>',"")
    doc = pq(html)
    # 获得页数
    pageNum = doc("#thread_theme_7>div.l_thread_info >ul>li:nth-child(2)>span:nth-child(2)").text()

    filter(html)

    # 构造下一页
    for i in range(1, int(pageNum)):
        urltemp = "{}?pn={}".format(url,i)
        print("抓取",urltemp)
        getUrl(urltemp)

        time.sleep(20)













