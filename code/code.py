import pandas as pd
import numpy as np
import math

def randomTar(size):
    r = [np.random.random() for i in range(1, size+1)]
    s = sum(r)
    r = [i / s for i in r]

    return r

#定义计算的函数
def E(x):
    if x>=0.6:
       return math.log(x-0.5)
    elif x<0.6:
       return -(1/x)+ E(1)

def Ex(x):
    return math.exp(x)

def Normalize(vector):

    m = np.mean(vector)
    mx = max(vector)
    mn = min(vector)

    dir = mx-mn

    if dir==0:
        dir=1

    return [(float(i) - m) / (dir) for i in vector]

#计算某一列的和
def calColSum(w,n):

    sum=0
    for i in range(len(w)):
        sum = sum + w[i][n]
    return sum

#计算某一列的和
def calSomeColSum(w,n):

    sum=0
    for i in range(len(w)):
        sum = sum + w[i][n]
    return sum

data = pd.read_csv("../data/temp.dat",sep="\t",names=['userid','itemid','rating','timestamp'])

film_list = list(set(data['itemid']))
film_count = len(film_list)
N = film_count

user_list = list(set(data['userid']))
user_count = len(user_list)

print(len(film_list))

var = {}
var['k'] = 10 #主题个数
var['v'] = 5  #评分级别数目
var['iter'] = 100
var['user_count'] = len(user_list)
var['film_count'] = film_count
#分布超参数
α = np.empty(var['k'])
γ = np.empty(var['k'])
Φ = np.zeros([user_count,film_count,var['k']])

β = [] #np.empty([var['v'],film_count])

#参数初始化
print("开始初始化αγ参数")
for i in range(len(α)):
    α[i] = 50/var['k']
    γ[i] = α[i]+N/var['k']

Φ = np.full(Φ.shape,1/var['k'])

print("开始初始化β参数")
for i in range(film_count):
    β.append(randomTar(var['k']))

β = (np.array(β)).T

print("开始初始化S参数")
S = np.empty([var['k'],film_count,var['v']])
for i in range(var['v']):
    for j in range(film_count):
        temp = randomTar(var['v'])
        for k in range(var['v']):
            S[i][j][k] = temp[k]

#获取用户*电影矩阵，内容存储电影id
w_user_film = []

print("初始化w_user_film参数")
for user in user_list:
    user_info = data.loc[data['userid'] == user]
    #print(list(user_info['itemid']))
    w_user_film.append(list(user_info['itemid']))

# user_info = data.loc[data['userid'] == 1]
# print(list(user_info['itemid']))

#获取用户电影*评分矩阵
w_user_film_score = []
for user in user_list:
    user_info = data.loc[data['userid'] == user]
    #print(list(user_info['itemid']))
    w_user_film_score.append(list(user_info['rating']))

# user_info = data.loc[data['userid'] == 1]
# print(list(user_info['rating']))


if __name__ =="__main__":

   #参数初始化完成
   # print(α)
   # print(Φ)
   print(β.shape)
   # print(S)
   # print(w_user_film)
   print(γ[0])

   for i in range(var['iter']):
       #开始执行E步
       print("开始执行E步")
       for u in range(var['user_count']):
           for n in range(len(w_user_film[u])):
               for i in range(var['k']):

                   Φ[u][n][i] = β[i][w_user_film[u][n]-1]  *  S[i][w_user_film[u][n]-1][w_user_film_score[u][n]-1]  *  Ex(E(γ[i]))
                   #Φ[u][n][i] = β[i][w_user_film[u][n] - 1] *  Ex(ψ(γ[i]))

               #对Φun进行归一化
               Φ[u][n] = Normalize(Φ[u][n])

            #更新参数γ
           print("#更新参数γ")
           for i in range(var['k']):
                γ[i] = α[i]+calColSum(Φ[u],i)


           #开始执行M步
           print("开始执行m步")
           for i in range(var['k']):
               for m in range(var['film_count']):
                   for v in range(var['v']):
                       S[i][m][v] = calColSum(Φ[u],i)

           for i in range(var['k']):
               for m in range(var['film_count']):
                   β[i][m] = calColSum(Φ[u],i)

                   S[i][m] = Normalize(S[i][m])

               β[i] = Normalize(β[i])
               α[i] = np.random.random()



   print("保存完毕")
   #np.savetxt("../data/Φ.npy",Φ)



   res = np.ndarray.tolist(Φ)
   print(res)
   print(S)


