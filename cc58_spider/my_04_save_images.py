import os
import time
import requests
import threading
from bs4 import BeautifulSoup
from urllib.request import urlopen


def get_url_html(url, head, proxy):
    """
    传入当前访问url链接, 获取到当前页面的网页源码
    :param url: 要访问的网页链接
    :param head: 从 my_02_get_ua 中随机获取的一个 User-Agent
    :param proxy: 从 my_01_get_proxy 中随机获取的一个代理 IP
    :return: 当前访问的网页源码
    """
    response = requests.get(url, headers=head, proxies=proxy)
    response.encoding = "encoding"
    if response.status_code == 200:
        return response.text


def parse_first_html(html):
    """
    处理第一次访问到的网页源码,获取当前页面中的图片标题,图片链接
    :param html: 第一次访问组图时候的链接
    :return: 当前访问的图片的标题, 组图连接
    """
    first_url_soup = BeautifulSoup(html, 'lxml')
    first_soup_list = first_url_soup.find('div', class_="cn").find_all('a')
    for first_url_info in first_soup_list:
        title = first_url_info.img["alt"]
        href = first_url_info["href"]
        yield title, href


def parse_second_html(second_href_html):
    """
    从第二次访问的图片源码中--首页中的每个人物的链接下的详情页链接, 获取到当前页面中人物的所有组图链接
    :param second_href_html: 当前访问的人物的网页源码
    :return: 当前页面这个任务的所有的组图链接
    """
    second_href_soup = BeautifulSoup(second_href_html, 'lxml')
    second_info_list = second_href_soup.find('div', class_="my-mx-top10").find_all("a")
    for img_href in second_info_list:
        yield img_href


def save_img(img_src, head, save_name, file_name, proxy):
    """
    从当前这张图片的详情中, 获取到图片的具体链接, 并通过获取到的图片链接下载图片
    :param img_src: 当张图片的具体访问地址
    :param head: 模拟的浏览器User-Agent
    :param save_name: 图片最后保存在哪个目录下
    :param file_name: 图片保存时候的名称
    :param proxy: 当前使用的代理IP
    :return: 图片下载时候成功
    """
    try:
        img_info_html = get_url_html(img_src, head, proxy)
        img_info_soup = BeautifulSoup(img_info_html, 'lxml')
        img_href = img_info_soup.find("div", id="content").a.img["src"]
        # print(img_href) http://img.cct58.com/caiji/mm/201707/3003/20170730033922_10632.jpg
        img_name = img_href[-13:]
        content = urlopen(img_href).read()

        if os.path.exists("%s" % save_name):  # 这是images
            if os.path.exists("%s/%s" % (save_name, file_name)):  # 这是./images/人名字
                with open("%s/%s/%s" % (save_name, file_name, img_name), "wb") as f:
                    f.write(content)
                    print("%s----下载完成..." % img_name)
                    time.sleep(.2)
            else:
                os.mkdir("%s/%s" % (save_name, file_name))
                with open("%s/%s/%s" % (save_name, file_name, img_name), "wb") as f:
                    f.write(content)
                    print("%s----下载完成..." % img_name)
                    time.sleep(.2)
        else:
            os.mkdir("%s" % save_name)
            print(save_name, "已创建")
            if os.path.exists("%s/%s" % (save_name, file_name)):  # 这是./images/人名字
                with open("%s/%s/%s" % (save_name, file_name, img_name), "wb") as f:
                    f.write(content)
                    print("%s----下载完成..." % img_name)
                    time.sleep(.2)
            else:
                os.mkdir("%s/%s" % (save_name, file_name))
                with open("%s/%s/%s" % (save_name, file_name, img_name), "wb") as f:
                    f.write(content)
                    print("%s----下载完成..." % img_name)
                    time.sleep(2)
    except:
        pass


def downloads(url, head, proxy, save_name):
    """
    从首页的链接中获取每个人物的信息, 再获取该人物每个组图的链接, 然后获取组图中的每张图片的链接, 最后下载图片
    :param url: 首页的链接
    :param save_name: 图片保存的路径(保存在哪个目录下面)
    :return: 图片的保存情况
    """
    html = get_url_html(url, head, proxy)
    for title, href in parse_first_html(html):

        # print(title,href) 范女郎性感照镜前冷不丁镜后辣人心 http://www.cct58.com/mneinv/37261/mx27id5157/
        second_href_html = get_url_html(href, head, proxy)
        for img_href in parse_second_html(second_href_html):

            # print(img_info["href"]) http://www.cct58.com/mneinv/37261/mx27id5157pg0.html
            img_href = img_href["href"]
            try:
                threading.Thread(target=save_img, args=(img_href, head, save_name, title, proxy)).start()
            except:
                continue

                
