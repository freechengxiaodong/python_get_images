'''
基于python3的定向定数据量的百度图片爬虫
__auther__ = chengxiaodong
'''
#-*- coding:utf-8 -*-
#所需类模块引入
import re
import requests
#全局变量声明
global i
i = 0
#编写自定义函数
def getImages(url):
    #向指定url发送数据，并获取返回结果
    html = requests.get(url).text
    #在返回结果中用正则规则匹配需要的内容
    pic_url = re.findall('"objURL":"(.*?)",', html, re.S)
    global i
    #循环遍历内容数组，下载图片资源，超时错误预处理
    for each in pic_url:
        print(each)
        try:
            pic = requests.get(each, timeout=1)
        except requests.exceptions.Timeout:
            print('链接不行了')
            continue
        except requests.exceptions.ConnectTimeout:
            print('哎呀！图片链接已失效')
            continue
        except requests.exceptions.ConnectionError:
            print('哎呀！超时了')
            continue
        #拼接图片根目录及新的文件名
        string = 'pictures\\' + str(i) + '.jpg'
        #文件打开及写入操作
        fp = open(string, 'wb')
        fp.write(pic.content)
        fp.close()
        i += 1
#主程序开始
#提示用户输入关键词
keyword = input('请输入关键词:')
#提示用户输入获取的数据量  默认一页60条数据(不排除链接失效的图片)
n = input('请输入需要爬取的前 n 页:')
#循环开始
page = 0
counter = 1
while counter <= int(n):
    #拼接新的url
    url = "http://image.baidu.com/search/flip?tn=baiduimage&word=" + keyword + "&pn=" + str(page)
    #向本次拼接的新url发送图片抓取请求
    getImages(url)
    page += 20
    counter += 1

#程序结束提示本次获取的有图片数量
print('本次爬取结束，共获取%s张图片'%i)
