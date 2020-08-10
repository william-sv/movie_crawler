#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
 @Project   : movie_crawler
 @FileName  : crawler.py
 @Time      : 2020/8/9 11:33 下午
 @Author    : william.sv@icloud.com

"""
import requests
import time
import csv


class Crawler:
    def __init__(self):
        self.host = 'movie.douban.com'
        self.tag = ['日剧']
        self.headers = {
            'Accept': '*/*',
            'Accept-Language': 'zh-cn',
            'Host': 'movie.douban.com',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.2 Safari/605.1.15',
            # 'Referer': 'https://movie.douban.com/tv/',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'X-Requested-With': 'XMLHttpRequest',
        }
        self.s = requests.session()

    def get_tv(self):
        self.headers['Referer'] = 'https://movie.douban.com/tag/'
        parameters = {
            'type': '',
            'tag': '',
            'sort': '',
            'page_limit': '',
            'page_start': ''
        }
        i = 2080
        flag = True
        while flag:
            # url = 'https://movie.douban.com/j/search_subjects?type=tv&tag=日剧&sort=recommend&page_limit=20&page_start=' + str(i)
            url = 'https://movie.douban.com/j/new_search_subjects?sort=&range=0,10&tags=%E7%94%B5%E8%A7%86%E5%89%A7&start=' + str(i) + '&countries=%E6%97%A5%E6%9C%AC'
            print(url)
            try:
                r = self.s.get(url=url,headers=self.headers,timeout=5)
                result = r.json()
                if 'data' not in result or len(result['data']) == 0:
                    flag = False
                self.save_csv(result['data'])
                time.sleep(15)
                i += 20
                self.s.get(url='https://movie.douban.com/subject/' + result['data'][0]['id'])
            except Exception as e:
                print(e)

    def save_csv(self, data):
        with open('./riju3.csv','a',encoding='utf-8') as f:
            wf = csv.writer(f)
            for item in data:
                wf.writerow([item['id'],item['title'],item['rate']])


if __name__ == '__main__':
    Crawler().get_tv()
