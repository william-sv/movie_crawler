#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
 @Project   : movie_crawler
 @FileName  : crawler.py
 @Time      : 2020/8/5 11:37 下午
 @Author    : william.sv@icloud.com

"""

import requests
from bs4 import BeautifulSoup as bs
import time
import re

class Crawler:
    def __init__(self):
        self.host = 'www.zhuixinfan.com'
        self.headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate',
            'Host': self.host,
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36',
            'Accept-Language': 'zh-cn',
            'Referer': 'http://www.zhuixinfan.com/viewall-tvplay-1.html',
            'Connection': 'keep-alive',
            'X-Requested-With': 'XMLHttpRequest'
        }
        self.s = requests.session()
        self.s.get(url='http://www.zhuixinfan.com/viewall-tvplay-1.html')

    def get(self):
        television = []
        url = 'http://www.zhuixinfan.com/main.php?mod=viewall&action=tvplay&area=1&alpha=&orderby=fp_date&sort=DESC&inajax=1'
        r = self.s.get(url=url,headers=self.headers)
        result = r.text.replace('<?xml version="1.0" encoding="utf-8"?>', '').replace('<root><![CDATA[', '').replace(']]></root>', '') # 如果不替换掉xml头，第一条数据就无法获取到
        soup = bs(result, 'lxml')
        television_list = soup.select('tr')
        for item in television_list:
            television_name = item.select('.td2 > a')[1].string
            television_url = 'http://' + self.host + '/' + item.select('.td2 > a')[1]['href']
            television_pid = re.search(r'\d{1,20}', television_url).group(0)
            television_type = item.select('.td3')[0].string
            television_status = item.select('.td4')[0].string
            television_download_torrent_urls = self.__get_television_download_url(television_pid)
            print(television_name,television_url,television_type,television_status,television_pid,television_download_torrent_urls)

    def __get_television_download_url(self, pid):
        television_download_urls = []
        url = 'http://www.zhuixinfan.com/main.php?mod=viewtvplay&action=list_file&pid=' + str(pid) + '&sort=all&inajax=1'
        r = self.s.get(url=url)
        result = r.text.replace('<?xml version="1.0" encoding="utf-8"?>', '').replace('<root><![CDATA[', '').replace(']]></root>', '') # 如果不替换掉xml头，第一条数据就无法获取到
        soup = bs(result, 'lxml')
        download_urls = soup.select('tr')
        for item in download_urls:
            download_name = item.select('.td2 > a')[0].string
            download_url = 'http://' + self.host + '/' + item.select('.td2 > a')[0]['href']
            torrent_url = self.__get_television_download_torrent_url(download_url)
            television_download_urls.append({
                'name': download_name,
                'torrent_url': torrent_url
            })
        return television_download_urls

    def __get_television_download_torrent_url(self,url):
        r = self.s.get(url=url)
        soup = bs(r.content, 'html5lib')
        torrent_url = soup.select('#torrent_url')[0].string
        return torrent_url


if __name__ == '__main__':
    Crawler().get()
