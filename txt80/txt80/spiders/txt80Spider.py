# -*- coding: utf-8 -*-
import scrapy
from lxml import etree
import csv

class Txt80spiderSpider(scrapy.Spider):
    name = 'txt80Spider'
    allowed_domains = ['www.txt80.com']
    start_urls = ['http://www.txt80.com/']



    def parse(self, response):

        html = etree.HTML(response.text)

        urls = html.xpath("//a/@href")

        # 获得当前访问的URL ,并分割，判断是否为小说详情页
        thisUrl = response.request.url
        bookUrl = str(thisUrl).split("/")[-1]

        #  断当前页面是否为小说详情页  若为小说详情页，则过滤信息，给保存页
        if((bookUrl.startswith("txt")) and (bookUrl.endswith(".html"))):
            self.Filter(html)

        for url in urls:
            temp = "http://www.txt80.com"+url
            print("请求",temp)
            yield scrapy.Request(temp)





    #过滤信息
    def Filter(self,html):

        bookName = html.xpath('//*[@id="container"]/div[8]/div[2]/dl/dd[1]/h2/text()')[0]
        bookAuthor = html.xpath('//*[@id="container"]/div[8]/div[2]/dl/dd[2]/a/text()')[0]
        bookSize = html.xpath('//*[@id="container"]/div[8]/div[2]/dl/dd[7]/span/text()')[0]
        publishData = html.xpath('//*[@id="container"]/div[8]/div[2]/dl/dd[8]/span/text()')[0]
        # //*[@id="container"]/div[11]/div[1]/div[2]/div/text()[1]
        bookIntro = html.xpath('//*[@id="container"]/div[11]/div[1]/div[2]/div/text()')[0]

        data= (bookName,bookAuthor,bookSize,publishData,bookIntro)

        self.saveInfo(data)


    # 保存到 csv文件
    def saveInfo(self,info):

        f = open('D:/80txt.csv', 'a',newline="")
        writer = csv.writer(f)

        writer.writerow(info)
        f.close()