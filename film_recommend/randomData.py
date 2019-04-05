import numpy as np
import random
import pandas as pd
import matplotlib.pyplot as plt
from pylab import mpl
from matplotlib.ticker import MultipleLocator,FormatStrFormatter

times = [1227571200, 962150400, 1199923200, 1222041600, 1105920000,
         1172275200, 1183334400, 1233100800, 1249689600, 1260748800,
         1021161600, 1157587200, 980640000,1334534400, 1253491200,
         1076544000, 1036022400, 995500800, 1349395200, 1131926400]
users = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
items = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]


records = []
for k in range(20):
    for i in range(random.randint(15,20)):
        user_id = users[random.randint(0,14)]
        item_id = items[random.randint(0,19)]
        time = times[k]
        score = random.randint(1,5)
        record = [user_id,item_id,score,time]
        records.append(record)
print(records)
print(len(records))

records = pd.DataFrame(records)
print(records)

records.to_csv("./data/test.dat",sep="\t",index=False,header=False)

# f = open("./data/test.dat", "rb")
#
# for record in records:
#     f.write()
#     f.write(str(record[0])+"\t"+str(record[1])+"\t"+str(record[2])+"\t"+str(record[3])+"\n")
#     #f.writelines(record)
# f.close()
# data = pd.read_table("./data/data.dat",sep="\t",names=['userid','itemid','rating','timestamp'])
#
# timestamp = list(set(data['timestamp']))
# print(timestamp)
#获取用户总数
#vars['user_count'] = len(list(set(data['userid'])))