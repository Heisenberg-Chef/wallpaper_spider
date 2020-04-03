import urllib.request as u
import urllib.parse as p
import ssl
import json
import re
import os
global vocabulary, url_8k, url_4k, man_made, earth
main_url = r'https://wall.alphacoders.com/?lang=Chinese'
url_8k = r'https://wall.alphacoders.com/by_resolution.php?w=7680&h=4320'
url_4k = r'https://wall.alphacoders.com/by_resolution.php?w=3840&h=2160'
man_made = r'https://wall.alphacoders.com/by_category.php?id=16&name=Man+Made+Wallpapers&filter=4K+Ultra+HD'
earth = r'https://wall.alphacoders.com/by_category.php?id=10&name=Earth+Wallpapers&filter=4K+Ultra+HD'

vocabulary = ''


def search_mainpage():
    headers = {
        'Accept': r'application/json, text/javascript, */*; q=0.01',
        'Content-Type': r'application/x-www-form-urlencoded; charset=UTF-8',
        'User-Agent': r'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/605.1.15\
                 (KHTML, like Gecko) Version/13.0.4 Safari/605.1.15',
    }
    url = re.split(r'&', 'https://wall.alphacoders.com/search.php?search=&lang=Chinese')
    global vocabulary, url_8k, url_4k, man_made, earth
    vocabulary = input("请输入您想查找的关联词#中、英:")
    if vocabulary == '4k':
        link = url_4k
    elif vocabulary == '8k':
        link = url_8k
    elif vocabulary == r'man made':
        link = man_made
    elif vocabulary == r'earth':
        link = earth
    else:
        link = url[0] + vocabulary + '&' + url[1]
    uncheck = ssl._create_unverified_context()
    resp = u.urlopen(link, context=uncheck)
    html = resp.read().decode('utf-8')
    # 索引的信息

    total = re.findall(r'<h1 class=(?:.*)>\s*(\d*\w*)\s*</h1>', html)
    #print("%s" % (total[0]))
    #print("------------------------------------------------------------------")
    try:
        os.mkdir(os.getcwd() + os.sep + vocabulary)
    except:
        print("The directory is existed..")
    print("All of your wanted PIC will store in " + vocabulary + " directory.")
    return html, link


def change_mainpage(link, num):
    '''num 为翻页的页数，main—page的第一页已经加载，所以从2开始'''
    url = link + r"&page=" + str(num)
    print(url)
    uncheck = ssl._create_unverified_context()
    resp = u.urlopen(url, context=uncheck)
    html = resp.read().decode('utf-8')
    return html


def max_num(html):
    '''aqqqaqaz搜索页最大翻页数量'''
    max_num = re.findall(r'<input type="text" class="form-control" placeholder="输入页数 / (\d*)">', html)
    max_num = max_num[0]
    return max_num


def link_dialog(html):
    '''元素信息返回是一个数组，如果图片是充满的，则有30个div'''
    # id信息
    id = re.findall('id="thumb_(.*)\"', html)
    # 服务器信息,图片格式，向前断言
    service_tag = re.findall(
        r'<img class=(?:.+) data-src="https://(?=image)(.*)\.alphacoders.com(?:.*)\.(.*)"[\s9890-7807656789097]alt="(?:.*)"',
        html)
    # 图片信息
    info = re.findall(r'<a href=(?:.*)title=(.*)?>\s*<img', html)
    # 图片格式
    return id, service_tag, info,


def merge_url(id, num):
    # 组合pic_url
    pic_url = r'https://wall.alphacoders.com/big.php?i=' + str(id[num])
    return pic_url


def download_pic(pic_url, id, service_tag):
    headers = {
        'Accept': r'application/json, text/javascript, */*; q=0.01',
        'Content-Type': r'application/x-www-form-urlencoded; charset=UTF-8',
        'Origin': r'https://wall.alphacoders.com',
        'Accept-Language': r'en-US,en;q=0.9',
        'Host': r'api.alphacoders.com',
        'Origin': r'https://wall.alphacoders.com',
        'User-Agent': r'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/605.1.15\
             (KHTML, like Gecko) Version/13.0.4 Safari/605.1.15',
        'Referer': str(pic_url),
        'Accept-Encoding': r'gzip, deflate, br',
        'Connection': r'keep-alive'
    }

    # 再请求下载链接的时候，需要图片的ID，

    data = {
        'content_id': str(id),
        'content_type': r'wallpaper',
        'file_type': str(service_tag[1]),
        'image_server': str(service_tag[0])
    }

    uncheck = ssl._create_unverified_context()
    data_b = p.urlencode(data).encode("utf-8")
    req = u.Request(r'https://api.alphacoders.com/content/get-download-link', data=data_b, headers=headers)
    resp = u.urlopen(req, context=uncheck, timeout=15)

    html = resp.read().decode('utf-8')
    dict_html = json.loads(html)
    downloadlink = dict_html['link']
    pic = u.urlopen(downloadlink, context=uncheck, timeout=15)
    global vocabulary
    with open(os.getcwd() + os.sep + vocabulary + os.sep + id + r'.' + service_tag[1], "wb") as f:
        f.write(pic.read(amt=52428800))
