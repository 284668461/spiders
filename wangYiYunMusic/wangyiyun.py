# -*- coding: UTF-8 -*-
'''
 @description: 网易云热歌榜音乐爬虫
 @program: spider 
 @author: 284668461@qq.com
 @create: 2020-03-21 14:31
'''


import requests
import json
from lxml import etree

'''
 @Description  请求链接
 @Author 284668461@qq.com
 @Date 2020/3/21 14:37 
'''
def getUrl(url):

    headers = {
        'path':'/discover/toplist?id=3778678',
        'Accept': '*/*',
        'Accept-Encoding': 'gzip,deflate,sdch',
        'Accept-Language': 'zh-CN,zh q=0.8,gl q=0.6,zh-TW q=0.4',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'music.163.com',
        'Referer': 'http://music.163.com/search/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0  WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
        'Cookie': '_iuqxldmzr_=32  _ntes_nnid=3781266ef61a5aa2d7ede27aa0183bc1,1551083564434  _ntes_nuid=3781266ef61a5aa2d7ede27aa0183bc1  WM_TID=OZGc1XNosq1FFVUURUIpkhlLoMCtrNMy  WM_NI=8rKLP6ufZLsNyeHmP9SDIvgYp6Yeuuu9ZGfzbCvvrI%2B%2FXUYhDsvVVFRPPcN1ekPJXIbE%2FYcXpJhEf9dT8jQQUfTaONE8iXIYAb%2F6FvZ0Xr4hoDjDHTgTPQpejvbJ0%2FIHU2Q%3D  WM_NIKE=9ca17ae2e6ffcda170e2e6ee92ef80fbaeb9d8b67b94a88ab2c85e829b9aafee7df4eda58df544a68f00d7ae2af0fea7c3b92afcae85add33eb7ba96adf246bbbb888ed333919c8797e653b4ea9786f87fb7e796a8e572a29dba97f143e9f198b6dc6488adbab7d54e9290a084cd3ba7b5a0abdb43a29be1bae254b496a8a6e533a88cf88bd45b97ba9c82ce4687e8a7b9cc5383bee1d7c57e9af09893b764ad9ca6a5cb60a58ca0b2f36faaaaaeabb3258b989bd3d437e2a3  JSESSIONID-WYYY=%2B0ojNXAeyKT7wKzj1AnD3RXYergSXK5S70VlZwNdlKqvuFDjOfb1Ao2PGtbBUf38RohOpdmBfcMpY3eM2jp5WiRsaJ22nosm%2F1AwqaJgomKkGAY5VfXyM%2BcVUrlgTEZFHaMNUcePUXY05Ks23XgW4yr1gPmb%2FJbtbks9nbC0OUlX82cn%3A1551237928176'
    }

    data = {
        "id":"3778678"
    }
    res = requests.get(url,headers=headers,data=data)

    filter(res.text)


'''
 @Description  过滤，提取数据
 @Author 284668461@qq.com
 @Date 2020/3/21 15:50 
'''
def filter(html):

    parser = etree.HTMLParser(encoding="utf-8")
    data = etree.HTML(html, parser=parser)

    songList = data.xpath('//*[@id="song-list-pre-data"]/text()')


    print("网易云热歌榜")
    print("-" * 50)

    for i in json.loads( songList[0] ):

        print("{:<}      歌手：{:>}".format(i["album"]["name"], i["artists"][0]["name"]))




if __name__ == '__main__':

   getUrl("https://music.163.com/discover/toplist?id=3778678")
