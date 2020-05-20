# -*- coding: UTF-8 -*-
'''
 @description: 哈哈网图片爬虫 入口
 @program: hahamx 
 @author: 284668461@qq.com
 @create: 2020-03-19 10:40
'''

import  requests
requests.packages.urllib3.disable_warnings()
import datetime
import headers as h
import re
import os
from pyquery import PyQuery as pq
from concurrent.futures import ThreadPoolExecutor
thread_pool = ThreadPoolExecutor(100)

Path = "D:/hahamx/"

passUrl = []
from threading import Lock
threadLock = Lock()
pageNum = 0

'''
 @Description  图片下载器
 @Author 284668461@qq.com
 @Date 2020/3/1 9:37 
'''
def down(info):
    # print("down")
    imgUrl = ("https:"+info["imgUrl"]).replace("normal","middle")
    title= info["title"]

    global Path,threadLock

    # 加锁
    threadLock.acquire()

    if os.path.exists(Path):
        pass
    else:
        try:
            os.mkdir(Path)
        except Exception as e:
            os.makedirs(Path)

    filePath = "{}/{}.{}".format(Path,title,imgUrl.split(".")[-1])

    # 判断该文件是否已存在
    if os.path.exists( filePath ):

        print("{}已存在，跳过".format(title))

        # 释放锁
        threadLock.release()
        return
    else:
        threadLock.release()
        print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "下载图片:{},到:{}".format( title,Path))

        resource = requests.get(imgUrl, headers=h.getHeader(), verify=False)
        with open(filePath, mode="wb") as fh:
            fh.write(resource.content)


'''
 @Description  请求网页
 @Author 284668461@qq.com
 @Date 2020/2/29 17:47 
'''
def getUrl(url):
    print("getUrl")

    try:
        # 加锁
        threadLock.acquire()
        passUrl.append(url)
        # 释放锁
        threadLock.release()

        print("正在请求",url)
        res = requests.get(url, headers=h.getHeader(), verify=False)
        html = res.text

        thread_pool.submit(filterUrl, html)

    except Exception as e:
        pass




'''
 @Description  过滤url
 @Author 284668461@qq.com
 @Date 2020/3/1 9:13 
'''
def filterUrl(text):
    print("filterUrl")


    dom = pq(text)


    ls = dom("#main>div.joke-list>div.joke-list-item").items()


    for i in ls:

        title = pq(i)("p.joke-main-content-text").text().replace('\n',' ')
        imgUrl = pq(i)("a.joke-main-img-wrapper>img").attr("data-original")
        d = {
            "title": title,
            "imgUrl":imgUrl
        }

        if( imgUrl != None):
            thread_pool.submit(down, d)


if __name__ == '__main__':


    url = "https://www.hahamx.cn/pic"
    res = requests.get(url, headers=h.getHeader(), verify=False)
    dom = pq( res.text )
    ls = dom(".pagination-link").items()

    page = 0

    # 获得总页数
    for i in ls:
        print( i )
        print( i.text() )

        try:
            tempNum = int( i.text() )
            page = tempNum
        except:
            pass

    filterUrl(res.text)

    # 生成下一页
    for i in range(1, page):
        url = "https://www.hahamx.cn/pic/new/{}".format(i)
        thread_pool.submit(getUrl, url)
