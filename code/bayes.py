# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 22:05:48 2019

@author: sun
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")

plt.rcParams['font.sans-serif']=['SimHei']

data = pd.read_csv("../data/data.dat",sep="\t",names=['userid','itemid','rating','timestamp'])

item_list = list(set(data['itemid']))
print(item_list)

# #获取用户列表
# user_list = list(set(data['userid']))
# for i in range(len(user_list)):
#     if i+1>=len(user_list):
#         break;
#
#     if user_list[i+1]-user_list[i]!=1:
#         print("error")
#
# #计算用户1的兴趣演化分析
#
# #关于用户1的数据
# user_one = data.loc[data['userid']==1]
#
# print(user_one)

# #用户1的时间序列
# user_one_t_seq = list(set(user_one['timestamp']))
#
# #用户时间序列评分
# user_time_rating = []
#
# for t in user_one_t_seq:
#     #temp = user_one.loc[user_one['timestamp']==t]
#     #print(temp)
#
#     user_time_rating.append(round(user_one.loc[user_one['timestamp']==t]['rating'].mean(),1))
#
# print(len(user_one))
#
# print(user_time_rating)
#
# print(user_one_t_seq)
#
# #计算p(x1=r1)
# x = [i for i in range(len(user_one_t_seq))]
# y = user_time_rating
#
# plt.plot(x, y)
#
#
# plt.title('用户电影兴趣走势')
# plt.xlabel('时间序列')
# plt.ylabel('电影平均评分')
#
# plt.show()
