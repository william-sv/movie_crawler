#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
 @Project   : movies
 @FileName  : crawler.py
 @Time      : 2020/8/4 11:04 下午
 @Author    : william.sv@icloud.com

"""

import requests
from bs4 import BeautifulSoup as bs
import time


class Crawler:
    def __init__(self):
        self.category = ['dongzuo','xiju','kehuan','juqing','zainan','dongman']
        self.host = 'www.piaohua.com'
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Host': 'www.piaohua.com',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36',
            'Accept-Language': 'zh-cn',
            'Referer': 'https://www.piaohua.com',
            'Connection': 'keep-alive',
        }
        self.s = requests.session()

    def get(self):
        for item in self.category:
            url = 'https://' + self.host + '/html/' + item + '/index.html'
            movies = self.__get_category_list(url)
            print(movies)
            time.sleep(0.5)

    def __get_category_list(self, url):
        movies = []
        r = self.s.get(url=url, headers=self.headers)
        soup = bs(r.content,'html5lib')
        movie_list = soup.select('.m-film > .ul-imgtxt2 > li > .txt ')
        for item in movie_list:
            movie_name = ''
            movie_url = 'https://' + self.host + item.select('h3 > a')[0]['href']
            if len(item.select('h3 > a > b > font')) > 0:
                movie_name = item.select('h3 > a > b > font')[0].string
            elif len(item.select('h3 > a > b')) > 0:
                movie_name = item.select('h3 > a > b')[0].string
            movie_download_urls = self.__get_movie_download_url(movie_url)
            movies.append({
                'movie_name':movie_name,
                'movie_url': movie_url,
                'movie_download_urls': movie_download_urls
            })
            time.sleep(0.5)
        return movies

    def __get_movie_download_url(self, url):
        movie_download_urls = []
        r = self.s.get(url)
        soup = bs(r.content, 'html5lib')
        download_urls = soup.select('.bot > a')
        for item in download_urls:
            if item.string == '最新电影下载':
                continue
            movie_download_urls.append(item.string)
        return movie_download_urls


if __name__ == '__main__':
    Crawler().get()
