import os
from multiprocessing.pool import Pool
from .my_01_get_ua import main_head
from .my_03_get_person import get_every_page, get_every_person
from .my_04_save_images import downloads


# 这里的 proxy 是从 my_01_get_proxy 中获取的
proxy = {'https': '218.91.151.242:58892'}


def get_img_href():
    """
    与用户交互获取文件保存的路径, 使用多进程-多线程,下载图片
    :return: 图片保存情况
    """
    url = "http://www.cct58.com/mneinv/1.html"
    # head = main_head()

    save_path = input("文件保存在: ")

    # 根据电脑CPU个数, 创建多进程
    os.cpu_count()
    # pool = Pool(os.cpu_count())
    pool = Pool(10)

    # 遍历获取每一页的url链接
    for href in get_every_page(url, main_head(), proxy):
        try:
            for person_mx27, title in get_every_person(href, main_head(), proxy):
                # print(person_mx27, title)     http://www.cct58.com/mneinv/19497/mx27/  夏夏

                # downloads(person_mx27, head, proxy,save_path)
                pool.apply_async(downloads, args=(person_mx27, main_head(), proxy, save_path))
        except:
            continue
    pool.close()
    pool.join()


if __name__ == '__main__':
    get_img_href()

    
