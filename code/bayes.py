# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 22:05:48 2019

@author: sun
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import numpy as np
import random
import pandas as pd

vars = {}
vars['K'] = 5
#首先获取电影*用户矩阵数据，内容存储的是主题数据，初始化生成
#获取主题*用户矩阵，内容存储的是每个用户所属于某个主题的权重系数
def getFilmUserMatrix(film_count,user_count):
     #初始化主题*用户矩阵
    topic_user = []
    for i in range(vars['K']):
        t = []
        for j in range(user_count):
            t.append(0)
        topic_user.append(t)
    #初始化电影*用户矩阵
    film_user = []
    for f in range(film_count):
        t = []
        for u in range(user_count):
            t.append(1)
        film_user.append(t)

    #电影*用户矩阵中每个用户随机分配主题
    #并同时计算主题*用户分布矩阵
    for f in range(film_count):
        for u in range(user_count):
            film_user[f][u] = random.randint(0,vars['K']-1)
              
            #获取f-u下对应的主题
            ti = film_user[f][u]
            #获取对应的用户id
            wi = u
            #获取权重系数
            temp = data[data['userid']==u]
            
            weight=0.0
            if len(temp[temp['itemid']==f]['rating'])==0:           
               weight = temp[temp['itemid']==f]['rating']
            else:
               weight = 0.0
                
            topic_user[ti][wi] = topic_user[ti][wi]+weight

    return topic_user,film_user


plt.rcParams['font.sans-serif']=['SimHei']

data = pd.read_table("../data/data.dat",sep="\t",names=['userid','itemid','rating','timestamp'])


def getUserFilmScore(user_count,film_count):
    data.set_index("rating")

    user_film_score = []

    for i in range(user_count):
        film = [0.1]*(film_count+1)
        temp = data[data['userid']==(i+1)]
        itemlist = list(temp['itemid'])
        print("user--"+str(i))
        for id in itemlist:
            film[id] = temp[temp['itemid']==id]['rating'].values[0]

        user_film_score.append(film)


#获取用户列表
user_list = list(set(data['userid']))
film_list = list(set(data['itemid']))
print(len(user_list))
#getUserFilmScore(len(user_list),len(film_list))
# #print(user_list)
#
# a,b = getFilmUserMatrix(len(film_list),len(user_list))
#
# print(a)
# print(b)

'''
temp = data[data['userid']==1]
res = temp[temp['itemid']==-1]['rating']
print(len(res))
'''


#计算用户1的兴趣演化分析




'''
#关于用户1的数据
user_one = data.loc[data['userid']==1]
#用户1的时间序列
user_one_t_seq = list(set(user_one['timestamp']))

#用户时间序列评分
user_time_rating = []

for t in user_one_t_seq:
    #temp = user_one.loc[user_one['timestamp']==t]
    #print(temp)
    
    user_time_rating.append(round(user_one.loc[user_one['timestamp']==t]['rating'].mean(),1))

print(len(user_one))

print(user_time_rating)

print(user_one_t_seq)

#计算p(x1=r1)
x = [i for i in range(len(user_one_t_seq))]
y = user_time_rating
 
plt.plot(x, y)

 
plt.title('用户电影兴趣走势')
plt.xlabel('时间序列')
plt.ylabel('电影平均评分')
 
plt.show()
'''