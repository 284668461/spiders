# -*- coding: UTF-8 -*-
'''
 @description:
 @program: vmgirls 
 @author: 284668461@qq.com
 @create: 2020-02-29 17:46
'''

import  requests
import datetime
from spiders import headers as h
import re
import os
from pyquery import PyQuery as pq
from concurrent.futures import ThreadPoolExecutor
thread_pool = ThreadPoolExecutor(100)

Path = "D:/vmgirls/"

passUrl = []
from threading import Lock
threadLock = Lock()


requests.packages.urllib3.disable_warnings()

'''
 @Description  图片下载器
 @Author 284668461@qq.com
 @Date 2020/3/1 9:37 
'''
def down(info):
    imgUrl = info["imgUrl"]
    pathtitle = info["pathtitle"]
    title= info["title"]


    global Path,threadLock

    filePath = "{}{}".format(Path,pathtitle)

    threadLock.acquire()

    if os.path.exists(filePath):
        pass
    else:
        try:
            os.mkdir(filePath)
        except Exception as e:
            os.makedirs(filePath)


    # 判断该文件是否已存在
    flag2 = os.path.exists( "{}/{}".format(filePath,title) )

    threadLock.release()

    if flag2:
        print("{}已存在，跳过".format(title))
        return
    else:
        print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "下载图片:{},到:{}".format(imgUrl, pathtitle))

        resource = requests.get(imgUrl, headers=h.getHeader(), verify=False)
        with open("{}/{}".format(filePath,title), mode="wb") as fh:
            fh.write(resource.content)





'''
 @Description  请求网页
 @Author 284668461@qq.com
 @Date 2020/2/29 17:47 
'''
def getUrl(url):
    tempUrl = url.lstrip("https://www.vmgirls.com")
    for i in passUrl:
        if(i == tempUrl):
            return
    try:

        threadLock.acquire()
        passUrl.append(tempUrl)

        threadLock.release()
        res = requests.get(url, headers=h.getHeader(), verify=False)
        html = res.text
        filterUrl(html,url)
    except Exception as e:
        pass




'''
 @Description  过滤url
 @Author 284668461@qq.com
 @Date 2020/3/1 9:13 
'''
def filterUrl(text,url):
    doc = pq(text)
    #判断是否是图片内容页
    ispage = doc(".nc-light-gallery")
    if(len(ispage)>0):

        # 判断是单页还是多页
        if(len(doc(".post-page-numbers")) > 0):

            thread_pool.submit(pages, text)

        else:

            thread_pool.submit(page, text)

    else:
        # 不是图片内容页 ，继续请求
        # 获得本页所有url
        urls = doc("a").attr.href
        for u in urls:
            # 判断字符串是否是 https://www.vmgirls.com/ 开头
            if (u.startswith("https://www.vmgirls.com/")):
                thread_pool.submit(getUrl, u)

        # 判断是否有加载更多 ajax 请求
        if( len( doc(".ajax-loading") ) >0 ):
            for i in range(1,1000):
                try:

                    headers = {
                        'User-Agent': h.getHeader2(),
                        "referer": url
                    }

                    d = {"append": "list-archive",
                         "paged": i,
                         "action": "ajax_load_posts",
                         "query": 33,
                         "page": "cat"
                         }
                    res = requests.post(url, headers=headers, data=d, verify=False)
                    # print(res.text)
                    if (res.status_code != 200):
                        break

                    # 获得本页所有url
                    domTemp = pq(res.text)
                    urls2 = re.findall('<a href="(.*?)" class="list-title text-md h-2x"',res.text)

                    for u2 in urls2:

                        # 判断字符串是否是 https://www.vmgirls.com/ 开头
                        if (u2.startswith("https://www.vmgirls.com/")):
                            # getUrl(u2)
                            thread_pool.submit(getUrl, u2)
                except Exception as e:
                    # print("filterUrl 出现异常",e)
                    break

'''
 @Description  单页
 @Author 284668461@qq.com
 @Date 2020/3/1 9:37 
'''
def page(html):
    doc = pq(html)
    info = doc(".nc-light-gallery").find( 'img' ).items()
    for i in info:

        pathTitle = i.attr("alt")
        imgurl =  i.attr("data-src")
        title =  imgurl.split("/")

        d = {}
        d["imgUrl"] = imgurl
        d["pathtitle"] = pathTitle
        d["title"] = title[ len(title) -1]
        thread_pool.submit(down,d)



'''
 @Description  多页
 @Author 284668461@qq.com
 @Date 2020/3/1 9:37 
'''
def pages(html):
    doc = pq(html)
    nextPage = doc("div.nav-links>a.post-page-numbers")

    pathTitle =  doc("h1.post-title").text()

    imgurl = re.findall("pic: '(.*?)',",html)[0]
    title = imgurl.split("/")

    d = {}
    d["imgUrl"] = imgurl
    d["pathtitle"] = pathTitle
    d["title"] =  title[len(title) - 1]
    thread_pool.submit(down, d)

    for n in nextPage:

        urlTemp = pq(n).attr("href")
        try:

            for i in passUrl:
                if (i == urlTemp.lstrip("https://www.vmgirls.com") ):
                    return

            res = requests.get(urlTemp, headers=h.getHeader(), verify=False)

            doc = pq(res.text)

            info = doc(".nc-light-gallery").find('a')

            for i in info:
                d = pq(i)
                pathTitle = d.attr("alt")
                imgurl = d.attr("href")
                title = imgurl.split("/")

                d = {}
                d["imgUrl"] = imgurl
                d["pathtitle"] = pathTitle
                d["title"] = title[len(title) - 1]
                thread_pool.submit(down, d)

            threadLock.acquire()
            passUrl.append( urlTemp.lstrip("https://www.vmgirls.com") )

            threadLock.release()


        except Exception as e:
            pass






if __name__ == '__main__':


    print("{:*^50}".format("vmGirls 全站爬虫 V1.0"))
    print("{}".format("author：Mine_希冀"))
    print("{}".format("date：2020-03-01"))
    print("本程序为爬虫程序，不出意外且一直运行的话，将会抓取 https://www.vmgirls.com/ 下所有的图片。\n请保持磁盘有足够的空间，所以")
    while True:

        try:
            num = int( input("是否要修改存储位置？(请输入序号，进行下一步操作)\n 1，不修改(默认位置：{}) \n 2、修改 \n".format(Path)) )
        except:
            print("您输入的格式有误")
            continue
        if (num == 1):
           break

        if (num == 2):
            while True:

                try:
                    num2 = int(input("请选择对应的的盘符 \n 1、C  \n 2、E \n 3、F \n 4、G \n 5、H  \n"))
                except:
                    print("您输入的格式有误")
                    continue

                if(num2 <= 5):

                    if(num2 == 1):
                        Path = "C:/vmgirls/"
                    elif(num2 == 2):
                        Path = "E:/vmgirls/"
                    elif (num2 == 3):
                        Path = "F:/vmgirls/"
                    elif (num2 == 4):
                        Path = "G:/vmgirls/"
                    elif (num2 == 5):
                        Path = "H:/vmgirls/"
                    break
                else:
                    print("您输入的序号有误")

            print("爬虫文件保存目录为：{}".format("{}".format(Path)))
            break

    print("开始程序")
    getUrl("https://www.vmgirls.com/")