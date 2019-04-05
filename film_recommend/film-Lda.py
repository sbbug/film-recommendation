# -*- coding: utf-8 -*-
"""
Created on Mon Mar 18 21:55:25 2019

@author: sun
"""

import numpy as np
import random
import pandas as pd
import matplotlib.pyplot as plt
from pylab import mpl
from matplotlib.ticker import MultipleLocator,FormatStrFormatter


mpl.rcParams['font.sans-serif'] = ['FangSong'] # 指定默认字体
mpl.rcParams['axes.unicode_minus'] = False # 解决保存图像是负号'-'显示为方块的问题
vars = {}
vars['K'] = 10
# vars['K'] = 10
# vars['K'] = 20
vars['alpha'] = 1
vars['eta'] = 0.001
vars['iterations'] = 1000
vars['gap']=100
#导入全局数据集
data = pd.read_table("./data/test.dat",sep="\t",names=['userid','itemid','rating','timestamp'])

#获取电影总数
vars['film_count'] = len(list(set(data['itemid'])))
#获取用户总数
vars['user_count'] = len(list(set(data['userid'])))

#获取用户对电影的评分矩阵
def getUserFilmScore(film_count,user_count,):
    data.set_index("rating")
    user_film_score = []

    for i in range(user_count):
        film = [0.0]*(film_count)
        temp = data[data['userid']==(i+1)]
        itemlist = list(temp['itemid'])

        print("user----"+str(i))
        for j in range(len(itemlist)):
            film[itemlist[j]-1] = temp[temp['itemid']==itemlist[j]]['rating'].values[0]

        user_film_score.append(film)

    return user_film_score


#首先获取电影*用户矩阵数据，内容存储的是主题数据，初始化生成
#获取主题*用户矩阵，内容存储的是每个用户所属于某个主题的权重系数
def getFilmUserAndTopicUserMatrix(film_count,user_count,user_film_score):
       
     #初始化主题*用户矩阵
    topic_user = []
    print("初始化user_count")
    for i in range(vars['K']):
        t = []
        for j in range(user_count):
            t.append(0)
        topic_user.append(t)
    #初始化电影*用户矩阵
    print("初始化film_user")
    film_user = []
    for f in range(film_count):
        t = []
        for u in range(user_count):
            t.append(1)
        film_user.append(t)

    print("----")
    #电影*用户矩阵中每个用户随机分配主题
    #并同时计算主题*用户分布矩阵
    for f in range(film_count):
        print(f)
        for u in range(user_count):
            film_user[f][u] = random.randint(0,vars['K']-1)
              
            #获取f-u下对应的主题
            ti = film_user[f][u]
            #获取对应的用户id
            wi = u

            topic_user[ti][wi] = topic_user[ti][wi]+user_film_score[wi][f]

    return topic_user,film_user
#操作电影-用户矩阵，统计每个文档中对应k号主题出现的频数
def getSumBy(film_user,k,d):
    n = 0
    for i in film_user[d]:
        if i==k:
           n=n+1
    return n
#获取电影*主题矩阵
def getFilmTopicMatrix(film_count,film_user):
    
    film_topic = np.zeros((film_count,vars["K"]))
    for f in range(film_count):
        for t in range(vars["K"]):
            film_topic[f][t] = getSumBy(film_user,t,f)

    return film_topic

#根据topic_user矩阵，计算其每一行的和，
def rowSum(topic_user):
    res = []
    for row in topic_user:
        t = 0
        for v in row:
             t=t+v
        res.append(t)
    return res
#实现向量与常数的相加
def rowAddb(row,b):
    res = []
    for r in row:
        r = float(r)+b
        res.append(r)

    return res
#计算主题-用户矩阵中单词wid在所有主题中出现的频数，并附加常数b
def cal(topic_user,u,b):

    res = []
    for i in range(len(topic_user)):
        res.append(topic_user[i][u]+b)
    return res
#实现向量相除
def div(a,b):
    res = []

    if isinstance(a,list) and isinstance(b,list):
        for i in range(len(a)):
            t = a[i] / b[i]
            res.append(t)
    elif  isinstance(a,list) and (isinstance(b,list)==False):
        if b == 0:
            b = 1
        for i in range(len(a)):
            t = a[i] / b
            res.append(t)

    return res
#实现向量相乘
#
def dot(a_list,b_list):
    res = []
    for i in range(len(a_list)):
        t = a_list[i]*b_list[i]
        t = round(t,10)
        res.append(t)

    return res
#实现矩阵中每个元素加常数
def addAlp(dt,alpha):
    for i in range(len(dt)):
        for j in range(len(dt[i])):
            dt[i][j] = dt[i][j]+alpha

    return dt
def matDivVec(mat,vec):
    for i in range(len(mat)):
        for j in range(len(mat[i])):
            mat[i][j] = round(mat[i][j]/vec[i],10)

    return mat

def normalization(data):
    _range = np.max(data) - np.min(data)
    return (data - np.min(data)) / _range

#LDA算法
def Lda(film_user,film_topic,topic_user,film_user_count,user_film_score,some_user=1):


    print(film_user)
    for i in range(vars['iterations']):  #迭代次数，重复迭代就是为了收敛
        for f in range(len(film_user)): #遍历每个电影
            print(str(i)+"========"+str(f))
            for u in range(len(film_user[f])): #遍历每个电影下的用户

                #获取当前电影下当前用户所属于的主题
                t0 = film_user[f][u]
                #获取单词对应wid,及编码
                wid = u
                #相应矩阵频数减一，因为我们要把当前电影中的用户主题重新赋值，所以t0这个旧主题对应的频数都要减一

                film_topic[f][t0] = film_topic[f][t0]-user_film_score[wid][f]
                topic_user[t0][wid] = topic_user[t0][wid]-user_film_score[wid][f]

                #计算f号电影下的用户总数，并加一个常数vars['K']*vars['alpha']
                denom_a = sum(film_topic[f])+vars['K']*vars['alpha']
                #根据user_topic矩阵，计算每个电影对的用户总数，并相加一个常数film_user_count*vars['eta']
                denom_b = rowAddb(rowSum(topic_user),film_user_count*vars['eta'])

                #获取当前电影下的当前用户位于每个主题下的频数分布
                p_z = dot(div(cal(topic_user,wid,vars['eta']),denom_b),div(rowAddb(film_topic[f],vars['alpha']),denom_a))
                p_z = div(p_z,sum(p_z))
                p = np.array(p_z)
                np.random.seed(0)
                #根据当前的用户位于主题的概率分布，随机选取一个新的主题
                p[p<0] = 0.001
                

                t1 = random.choices(range(0,vars['K']),weights=p)
                t1 = t1[0]

                #重新更细矩阵
                film_user[f][u] = t1
                film_topic[f][t1] = film_topic[f][t1]+user_film_score[wid][f]
                topic_user[t1][wid] =topic_user[t1][wid]+user_film_score[wid][f]
                # if t0!=t1:
                #     print("=========="+str(i))
                    
        #保存某个用户主题演化分析过程的曲线图
        if i%vars['gap']==0:

            temp = np.array(topic_user)
            y = temp[:,some_user]
            y = np.round(y,4)
            y = normalization(y)
            x = [i for i in range(0,vars['K'])]

            xm = MultipleLocator(1)
            fig = plt.figure()
            ax = fig.add_subplot(1, 1, 1)
            ax.set_title(str(some_user)+'号客户兴趣主题演化')
            ax.set_xlabel('主题')
            ax.xaxis.set_major_locator(xm)
            ax.plot(x, y)
            plt.savefig(str(some_user)+"_"+str(i)+"_user.jpg")
            plt.clf()
          
    #电影主题计算
    a = addAlp(film_topic,vars['alpha'])
    b = rowSum(a)
    theta = matDivVec(a,b)
    # print(theta)

    #主题用户计算
    a = addAlp(topic_user, vars['eta'])
    b = rowSum(a)
    phi = matDivVec(a, b)
    # print(phi)

    return theta,phi

#将训练好的模型数据保存到文件里
def saveData(mat,file):

    f = open(file,"w+",encoding="utf-8")
    for m in mat:
        f.write(str(m)+"\n")

    f.close()

if __name__ == '__main__':

    #某一个用户
    some_user=1

    print("获取user_film_score")
    user_film_score = getUserFilmScore(vars['film_count'],vars['user_count'])

    print("获取user_topic,film_user")
    topic_user,film_user = getFilmUserAndTopicUserMatrix(vars['film_count'],vars['user_count'],user_film_score)

    print("获取film_topic")
    film_topic = getFilmTopicMatrix(vars['film_count'],film_user)

    print("开始训练模型")
    theta,phi = Lda(film_user,film_topic,topic_user,vars['user_count'],user_film_score,some_user)

    print("保存训练好的结果")
    theta = np.array(theta)
    phi = np.array(phi)
    np.savetxt("./theta_1.txt",theta)
    np.savetxt("./phi_1.txt", phi)
    print("保存模型")

    # theta = np.loadtxt("./theta_1.txt")
    # phi = np.loadtxt("./phi_1.txt")
    # print("theta--------")
    # print(theta)
    # print("phi---------")
    # print(phi)