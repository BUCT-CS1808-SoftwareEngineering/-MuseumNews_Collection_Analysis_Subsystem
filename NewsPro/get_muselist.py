# -*- coding: utf-8 -*-
import pandas as pd

def get_list():

    df = pd.read_excel('./muselist.xlsx', usecols=[1], engine='openpyxl')
    data = df.values
    muse_list = []
    # print(type(data))
    # print(data)
    for i in data:
        i = list(i)
        # print(type(i))
        # print(i)
        if type(i[0]) is not type('博物馆'):
            continue
        muse_list.append(i[0])

    return muse_list

# print(get_list())