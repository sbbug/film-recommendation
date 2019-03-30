# -*- coding: utf-8 -*-
"""
Created on Mon Mar 18 21:55:25 2019

@author: sun
"""

import numpy as np
import random
import pandas as pd

vars = {}
vars['K'] = 5
# vars['K'] = 10
# vars['K'] = 20
vars['alpha'] = 1
vars['eta'] = 0.001
vars['iterations'] = 10

#导入全局数据集
data = pd.read_table("./data.dat",sep="\t",names=['userid','itemid','rating','timestamp'])

#首先获取电影*用户矩阵数据，内容存储的是主题数据，初始化生成
#获取主题*用户矩阵，内容存储的是每个用户所属于某个主题的权重系数
def getFilmUserAndTopicUserMatrix(film_count,user_count):
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
#操作电影-用户矩阵，统计每个文档中对应k号主题出现的频数
def getSumBy(film_user,k,d):
    n = 0
    for i in film_user[d]:
        if i==k:
           n=n+1
    return n
#获取电影*主题矩阵
def getFilmTopicMatrix(film_count,film_user):
    
    film_topic = np.zeros((film_count,film_user))
    for f in range(film_count):
        for t in range(vars["K"]):
            film_topic[f][t] = getSumBy(ta,t,f)

    return dt

 


#读取文档到列表
#文档集合是预先处理好的数据
def getDocsList():
    # file = "../data/test2.txt"
    file = "../data/process.txt"
    f = open(file,"r+",encoding="utf-8")
    line = f.readline()
    docs = []
    while line and line!='\n':
        # print("==="+line)
        line = line.replace("\n","")
        docs.append(line.split(" "))
        line = f.readline()

    return docs
#从文档集合中获取字典列表
#字典是预先处理好的数据，当然也可以从文档集合中重新获取一次
#从文档中重新获取字典
def getVocab(docs):
    vocab = []
    n=0
    for d in docs:
         for w in d:
             n=n+1
             print("==="+str(n))
             if w not in vocab:
                 vocab.append(w)
    print("vocab=========")
    print(vocab)
    return vocab
#直接从文件里读取字典
def getVocabFromFile():
    vocab = []
    f = open("../data/dict.txt","r+",encoding="utf-8")
    line = f.readline()

    while line and line!='\n':
        line = line.split("\n")
        if line[0] not in vocab:
            vocab.append(line[0])

        line = f.readline()

    return vocab

#将文档集合中的单子向量化，就是编码
def getDocWordId(docs,vocab):
    docs_word_id = []
    for d in docs:
        doc_id = []
        #print(d)
        for w in d:
            id = vocab.index(w)
            doc_id.append(id)
        docs_word_id.append(doc_id)

    return docs_word_id
#获取主题-单词矩阵:每个主题下的单词词频分布
#获取文档-单词矩阵:每个文档下的每个单词的主题
def getWtTa(docs_word_id,docs,vocab):
    #初始化主题-单词矩阵
    wt = []
    for i in range(vars['K']):
        t = []
        for j in range(len(vocab)):
            t.append(0)
        wt.append(t)
    #初始化文档-单词矩阵
    ta = []
    for d in docs:
        t = []
        for w in d:
            t.append(1)
        ta.append(t)

    #文档-单词矩阵中每个单词随机分配主题
    #并同时计算主题单词分布矩阵
    for d in range(len(docs)):
        for w in range(len(docs[d])):
            ta[d][w] = random.randint(0,vars['K']-1)
            ti = ta[d][w]
            wi = docs_word_id[d][w]
            wt[ti][wi] = wt[ti][wi]+1

    return wt,ta
#操作文档-单词矩阵，统计d号文档中k号主题出现的频数
def getSumBy(ta,k,d):
    n = 0
    for i in ta[d]:
        if i==k:
           n=n+1
    return n
#获取文档-主题矩阵:每个文档中的主题词频分布
def getDt(docs,ta):
    dt = np.zeros((len(docs),vars["K"]))

    for d in range(len(docs)):
        for t in range(vars["K"]):
            dt[d][t] = getSumBy(ta,t,d)

    return dt
#根据wt矩阵，计算其每一行的和，
#这里计算主题-单词矩阵：每个文档的单词总数
def rowSum(wt):
    res = []
    for row in wt:
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
#计算主题-单词矩阵中单词wid在所有主题中出现的频数，并附加常数b
def cal(wt,wid,b):

    res = []
    for i in range(len(wt)):
        res.append(wt[i][wid]+b)
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
#LDA算法
def Lda(vocab,docs_word_id,ta,dt,wt):

    for i in range(vars['iterations']):  #迭代次数，重复迭代就是为了收敛
        for d in range(len(docs_word_id)): #遍历每个文档
            for w in range(len(docs_word_id[d])): #遍历每个文档下的单词

                #获取当前文档下当前单词主题
                t0 = ta[d][w]
                #获取单词对应wid,及编码
                wid = docs_word_id[d][w]
                #相应矩阵频数减一，因为我们要把当前文档中的次单词主题重新赋值，所以t0这个旧主题对应的频数都要减一
                dt[d][t0] = dt[d][t0]-1
                wt[t0][wid] = wt[t0][wid]-1

                #计算d号文档下的单词总数，并加一个常数vars['K']*vars['alpha']
                denom_a = sum(dt[d])+vars['K']*vars['alpha']
                #根据wt矩阵，计算每个文档对的单词总数，并相加一个常数len(vocab)*vars['eta']
                denom_b = rowAddb(rowSum(wt),len(vocab)*vars['eta'])

                #获取当前文档下的当前单词位于每个主题下的词频分布
                p_z = dot(div(cal(wt,wid,vars['eta']),denom_b),div(rowAddb(dt[d],vars['alpha']),denom_a))
                p_z = div(p_z,sum(p_z))
                p = np.array(p_z)
                np.random.seed(0)
                #根据当前的单词位于主题的概率分布，随机选取一个新的主题
                #print(p)
                t1 = np.random.choice(range(0,vars['K']),p = p.ravel())

                #重新更细矩阵
                ta[d][w] = t1
                dt[d][t1] = dt[d][t1]+1
                wt[t1][wid] = wt[t1][wid]+1
                if t0!=t1:
                    print("=========="+str(i))

    #统计结果
    a = addAlp(dt,vars['alpha'])
    b = rowSum(a)
    theta = matDivVec(a,b)
    # print(theta)

    a = addAlp(wt, vars['eta'])
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

    print("获取文档列表")
    docs = getDocsList()

    print("获取词汇列表")
    #vocab = getVocab(docs)
    vocab = getVocabFromFile()

    print("获取文档单词的index")
    docs_word_id = getDocWordId(docs,vocab)

    print("获取wt,ta")
    wt,ta = getWtTa(docs_word_id,docs,vocab)

    print("获取dt")
    dt = getDt(docs,ta)

    print("开始训练模型")
    theta,phi = Lda(vocab, docs_word_id, ta, dt, wt)

    print("保存训练好的结果")
    saveData(theta,"../data/theta_1.txt")
    saveData(phi,"../data/phi_1.txt")
    print("theta--------")
    print(theta)
    print("phi---------")
    print(phi)