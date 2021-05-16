# -*- coding: utf-8 -*-

# 对时间进行处理的函数，统一时间的格式进行存储
import re
import random
from datetime import datetime


def Baijiahao_time(date):
    md = re.search(r"(\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2})", date)
    year = datetime.now().strftime('%Y')
    return year + '-' + md.group(0)

def ppxw_time(date):
    return date

def txxw_time(date):
    # 202105/0615:51
    md = re.search(r"(\d{1,2}/\d{1,2})", date)
    time = re.search(r"(\d{1,2}:\d{1,2})", date)
    # print(md.group(0).replace('/', '-'))

    year = datetime.now().strftime('%Y')
    return year + '-' + md.group(0).replace('/', '-') + ' ' + time.group(0)

def wyxw_time(date):
    time = re.search(r"(\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2})", date)
    return time.group(0)

def fhxw_tiem(date):
    time = re.search(r"(\d{4}年\d{1,2}月\d{1,2}日\s\d{1,2}:\d{1,2})", date)
    return time.group(0).replace('年', '-').replace('月', '-').replace('日', '')

def shxw_time(date):
    return date

def sina_time(date):
    time = re.search(r"(\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2})", date)
    return time.group(0)

# str = '发布时间: 20-12-18 22:14'
# str1 = '202105/0615:51'
# str2 = '2020-10-07 05:31:02　来源: 吃喝玩乐在长沙举报'
# str3 = '2021年04月27日 20:30:02'
# str4 = '2021-05-09 07:57'
# str5 = '浙江融媒体 2021-05-11 21:24:52'
# print(Baijiahao_time(str))
# print(txxw_time(str1))
# print(wyxw_time(str2))
# print(fhxw_tiem(str3))
# print(shxw_time(str4))
# print(sina_time(str5))
# https://blog.csdn.net/maizi_jie/article/details/82152042?utm_medium=distribute.pc_relevant_bbs_down.none-task-blog-baidujs-1.nonecase&depth_1-utm_source=distribute.pc_relevant_bbs_down.none-task-blog-baidujs-1.nonecase