#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
 @Project   : movies
 @FileName  : crawler.py
 @Time      : 2020/8/4 11:49 下午
 @Author    : william.sv@icloud.com

"""

import requests
from bs4 import BeautifulSoup as bs
import time


class Crawler:
    def __init__(self):
        self.category = ['1_1______','1_2______','1_4______','1_6______']
        self.host = 'www.meijutt.tv'
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Host': self.host,
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.2 Safari/605.1.15',
            'Accept-Language': 'zh-cn',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive'
        }
        self.s = requests.session()

    def get(self):
        for item in self.category[:1]:
            url = 'https://' + self.host + '/' + item + '.html'
            television = self.__get_category(url)
            print(television)
            time.sleep(0.5)

    def __get_category(self,url):
        television = []
        r = self.s.get(url,headers=self.headers)
        soup = bs(r.content, 'html5lib')
        television_list = soup.select('.list3_cn_box > .cn_box2')
        for item in television_list:
            television_name = item.select('.list_20 > li')[0].select('a')[0].string
            television_url = 'https://' + self.host + item.select('.list_20 > li')[0].select('a')[0]['href']
            television_episodes_tmp = [ite for ite in item.select('.list_20 > li')[1].stripped_strings][-1]
            television_episodes = item.select('.list_20 > li')[1].select('span > font')[0].string + (television_episodes_tmp if television_episodes_tmp != '预告' else ' / 未更新')
            # television_last_episode = item.select('.list_20 > li')[1].select('span > font')[0].string + television_episodes
            television_sort = item.select('.list_20 > li')[-1].select('.cor_move_li')[0].string
            television_download_urls = self.__get_television_download_url(television_url)
            television.append({
                'television_name': television_name,
                'television_url': television_url,
                'television_episodes': television_episodes,
                'television_sort': television_sort,
                'television_download_urls': television_download_urls
            })
            time.sleep(0.5)
        return television

    def __get_television_download_url(self, url):
        television_download_urls = []
        r = self.s.get(url)
        soup = bs(r.content, 'html5lib')
        download_urls = soup.select('.current-tab > .down_list > ul > li > input')
        if len(download_urls) > 0:
            for item in download_urls:
                television_download_urls.append(item['value'])
        return television_download_urls


if __name__ == '__main__':
    Crawler().get()
