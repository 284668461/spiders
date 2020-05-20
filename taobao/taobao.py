# -*- coding: UTF-8 -*-
'''
 @description:淘宝爬虫
 @program: spider 
 @author: 284668461@qq.com
 @create: 2020-03-21 17:53
'''

from selenium import webdriver
import time

driver = ""
pageNum = 0


'''
 @Description  搜索指定关键字
 @Author 284668461@qq.com
 @Date 2020/3/21 21:22 
'''
def search(key):
    print("search")
    input =  driver.find_element_by_id('q')
    input.send_keys(key)

    btn = driver.find_element_by_class_name('search-button')
    btn.click()

    #等待10秒，手动登录
    time.sleep(10)
    filter()

    # 等待一秒切换到下一页
    time.sleep(1)
    toggleNextPage()


'''
 @Description  过滤
 @Author 284668461@qq.com
 @Date 2020/3/21 21:23 
'''
def filter():
    print("filter")

    items = driver.find_elements_by_css_selector('#mainsrp-itemlist  div.items > div.item')

    for item in items:
        price = item.find_elements_by_css_selector('div.price.g_price.g_price-highlight > strong')[0].text

        title = item.find_elements_by_css_selector('div.title')[0].text

        shop = item.find_elements_by_css_selector('div.shop > a > span:nth-child(2)')[0].text

        print(title,price,shop)

    time.sleep(3)
    toggleNextPage()


'''
 @Description  切换下一页
 @Author 284668461@qq.com
 @Date 2020/3/22 10:01 
'''
def toggleNextPage():
    print("toggleNextPage")
    #获得页数
    pageStr = driver.find_element_by_css_selector("div.total").text

    pageNum = int(  pageStr.lstrip("共").rstrip("页，") )

    thisPage = int( driver.find_element_by_css_selector("#mainsrp-pager li.active>span.num").text )


    print("共有页数:{},当前所在页:{}".format(pageNum,thisPage))

    if(thisPage<pageNum):
        # 切换到下一页
        driver.find_element_by_css_selector("#mainsrp-pager li.next").click()

        time.sleep(3)
        filter()




if __name__ == '__main__':

    key = input("请输入查找关键字\n")

    path = 'chromedriver80.exe'
    driver = webdriver.Chrome(executable_path=path)

    url = 'http://www.taobao.com/'
    driver.get(url)

    search(key)


