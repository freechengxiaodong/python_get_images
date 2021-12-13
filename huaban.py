import os
import re
import time

import requests

global i
i = 0


def getImages(keyword, url):
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1', }
    html = requests.get(url, headers=header, verify=False).text

    pic_url = re.findall('"objURL":"(.*?)",', html, re.S)
    global i

    for each in pic_url:
        print(each)
        try:
            pic = requests.get(each, timeout=1)
        except requests.exceptions.ConnectTimeout:
            print('哎呀！图片链接已失效')
            continue
        except requests.exceptions.Timeout:
            print('链接不行了')
            continue
        except requests.exceptions.ConnectionError:
            print('哎呀！超时了')
            continue

        if os.path.exists(keyword + '\pictures'):
            continue
        else:
            os.makedirs(keyword + '\pictures')

        string = keyword + '\pictures\\' + str(i) + '.jpg'

        fp = open(string, 'wb')
        fp.write(pic.content)
        fp.close()
        i += 1


keyword = input('请输入关键词:')

n = input('请输入需要爬取的前 n 页:')

page = 0
counter = 1
while counter <= int(n):
    url = "http://image.baidu.com/search/flip?tn=baiduimage&word=" + keyword + "&pn=" + str(page)

    getImages(keyword, url)
    page += 20
    counter += 1

print('本次爬取结束，共获取%s张图片' % i)
