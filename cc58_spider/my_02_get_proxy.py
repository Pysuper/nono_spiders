import requests
from lxml import etree
from .my_01_get_ua import main_head


def get_html(head):
    """
    使用可用的代理IP获取当前网页的源码
    :param head: 模拟的浏览器User-Agent
    :return: 当前访问的浏览器源码
    """
    proxy = {'https': '183.129.244.17:10080'}
    for i in range(1, 6):
        url = "http://www.xicidaili.com/nn/%s" % i
        response = requests.get(url, headers=head, proxies=proxy)
        response.encoding = "utf-8"
        if response.status_code == 200:
            return response.text
        else:
            print("无法访问...")


def parse(response_text, head):
    """
    使用 xpath 获取页面中的 IP 信息,并通过随机访问网页,根据返回的状态码,判断当前代理IP是否可用
    :param response_text: 获取代理IP的网页源码
    :param head: 模拟的浏览器User-Agent
    :return: 可用的代理IP
    """
    response = etree.HTML(response_text)
    ip = response.xpath('//tr[@class]/td[2]/text()')
    port = response.xpath('//tr[@class]/td[3]/text()')
    agreement_type = response.xpath('//tr[@class]/td[6]/text()')
    for ip, port, agreement_type in zip(ip, port, agreement_type):

        # 将获取的数据拼接为正确的proxy格式
        proxy = {"%s" % agreement_type.lower(): "%s:%s" % (ip, port)}
        try:
            resp = requests.get('http://icanhazip.com', headers=head, proxies=proxy, timeout=3)
            if resp.status_code == 200:
                yield proxy
            else:
                continue
        except:
            continue


def main_proxy():
    """
    从 my_02_get_ua 中随机获取一个User-Agent,并传入 request 请求, 获取西刺代理中的可用代理
    :return: 将所有可用的代理IP及端口号,按照proxy的标准格式输出
    """
    head = main_head()
    response = get_html(head)
    for proxy in parse(response, head):
        print(proxy)

