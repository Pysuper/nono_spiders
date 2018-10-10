import requests
from bs4 import BeautifulSoup


def get_url_html(url, head, proxy):
    """
    通过传入的url, 获取当前 url 的网页源码
    :param url: 要访问的网页链接
    :param head: 从 my_02_get_ua 中随机获取的一个 User-Agent
    :param proxy: 从 my_01_get_proxy 中随机获取的一个代理 IP
    :return: 当前url的网页源码
    """
    response = requests.get(url, headers=head, proxies=proxy)
    response.encoding = "utf-8"
    if response.status_code == 200:
        return response.text
    return "无法访问..."


def parse_person_html(first_url_html):
    """
    通过传入的第一个url源码, 获取到当前页面中的所有组图信息
    :param first_url_html: 第一个页面的网页源码
    :return: 当前访问的页面中的组图信息(组图的详情页链接, 组图的标题)
    """
    person_url_soup = BeautifulSoup(first_url_html, 'lxml')
    person_soup_list = person_url_soup.find('div', class_="topc5").find_all('div', class_="listbox")
    for person_soup in person_soup_list:
        person_detail_href = person_soup.a["href"]
        person_detail_title = person_soup.a.img["alt"]
        yield person_detail_href, person_detail_title


def get_every_page(url, head, proxy):
    """
    通过首页的源码, 获取到该标题下的最大页数, 拼接出所有页面的url链接
    :param url: 首页的url链接
    :return: 首页中所有页数中的链接列表
    """
    html = requests.get(url, headers=head, proxies=proxy).text
    soup = BeautifulSoup(html, 'lxml')
    page_soup = soup.find('div', class_="text-c").find_all("a")
    last_page = int(page_soup[-2].text)
    for page_num in range(1,last_page):
        one_url = "http://www.cct58.com/mneinv/%d.html" % page_num
        
        # http: // www.cct58.com / mneinv / 20.html
        yield one_url


def get_every_person(url, head, proxy):
    """
    从当前页面中, 获取当前页面中所有人物的详情页链接
    :param url: 首页的url链接
    :return: 每个人物的详情页链接, 每个人物的名字
    """
    first_url_html = get_url_html(url, head, proxy)
    for person_detail_href, person_detail_title in parse_person_html(first_url_html):
        person_mx27 = person_detail_href + "mx27/"
        
        # http://www.cct58.com/mneinv/37261/mx27/ 冷不丁
        yield person_mx27,person_detail_title
        
        
