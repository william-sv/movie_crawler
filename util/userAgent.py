#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
 @Project   : movies
 @FileName  : userAgent.py
 @Time      : 2020/8/4 11:07 下午
 @Author    : william.sv@icloud.com

"""
import random

user_agents = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.2 Safari/605.1.15'
]


def get_user_agent():
    return random.choice(user_agents)
