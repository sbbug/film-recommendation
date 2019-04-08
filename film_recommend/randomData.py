import numpy as np
import random
import pandas as pd
import matplotlib.pyplot as plt
from pylab import mpl
from matplotlib.ticker import MultipleLocator,FormatStrFormatter
import time

mpl.rcParams['font.sans-serif'] = ['FangSong'] # 指定默认字体
mpl.rcParams['axes.unicode_minus'] = False # 解决保存图像是负号'-'显示为方块的问题

# times = [1227571200, 962150400, 1199923200, 1222041600, 1105920000,
#          1172275200, 1183334400, 1233100800, 1249689600, 1260748800,
#          1021161600, 1157587200, 980640000,1334534400, 1253491200,
#          1076544000, 1036022400, 995500800, 1349395200, 1131926400]
# users = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
# items = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
#
# times = sorted(times,reverse=False)
#
# records = []
# for k in range(20):
#     for i in range(random.randint(15,20)):
#         user_id = users[random.randint(0,14)]
#         item_id = items[random.randint(0,19)]
#         time = times[k]
#         score = random.randint(1,5)
#         record = [user_id,item_id,score,time]
#         records.append(record)
# print(records)
# print(len(records))
#
# records = pd.DataFrame(records)
# print(records)
#
# records.to_csv("./data/test.dat",sep="\t",index=False,header=False)




#根据时间片从数据集筛选数据
def getSliceData(data,times):

    m_in = min(times)
    m_ax = max(times)

    return data[(data['timestamp']>=m_in)&(data['timestamp']<=m_ax)]

#获取划分好的时间片集合
def getSliceTime(times,n):

    time_slices = []
    times = sorted(times, reverse=False)
    dx = len(times) // n
    for i in range(n):

        start = i * dx
        end = i * dx + dx
        if end >= len(times):
            end = len(times)

        time_slices.append(times[start:end + 1:1])
    return time_slices

if __name__ =="__main__":
    data = pd.read_table("./data/test.dat", sep="\t", names=['userid', 'itemid', 'rating', 'timestamp'])
    times = list(set(data['timestamp']))
    print(times)
    n = 10
    slices = getSliceTime(times,n)
    for slice in slices:
        print(getSliceData(data,slice))
        print("----------------")