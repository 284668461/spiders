# spiders 爬虫合集
以下无特别说明均是使用python 3.7开发。

## vmgirls
>### 简介
    抓取网站 https://www.vmgirls.com/ 所有图片
>### 使用技术
    requests、pyquery、
>### 注意事项
    大概一个小时内可以抓取完整个网站，完成后没提示，请自行查看
>### 最后更新 
    20200520

---------

## hahamx
>### 简介
    抓取网站 https://www.hahamx.cn/pic 下的搞笑图片
>### 使用技术
    requests、pyquery、re、
>### 注意事项
    网站有反爬措施。使用自建ip代理池，突破反爬
>### 最后更新 
    20200520

--------


## taobao
>### 简介
    抓取网站 https://www.taobao.com/
>### 使用技术
    selenium、
>### 注意事项
    需要手动登录淘宝
>### 最后更新 
    20200321
--------


## wangYiYunMusic
>### 简介
    网易云热歌榜爬虫，抓取网站 music.163.com/discover/toplist?id=3778678
>### 使用技术
    requests、lxml、xpath、
>### 最后更新 
    20200321

-----

## tieba
>### 简介
    百度贴吧邮箱爬虫，抓取网站 https://tieba.baidu.com/p/5858684223 
    可自行更改为有邮箱的帖子
>### 使用技术
    requests、re、PyQuery、
>### 最后更新 
    20200312

------------

## txt80
>### 简介
    80电子书爬虫，抓取网站 www.txt80.com
    获得小说基本信息，保存到csv中。

>### 使用技术
    scrapy、xpath、
>### 注意事项
    没做反反爬，会被封ip
>### 最后更新
    20200524
