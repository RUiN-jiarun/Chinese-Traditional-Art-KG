import csv
import pandas as pd

name_list = []
dynasty_list = []

with open('raw_data.csv', encoding='utf-8') as f:
    f_csv = csv.reader(f)
    for row in f_csv:
        data = row[2]
        # print(row[2])
        l = data.split()
        # print(l)
        if l[0] == '年代':
            continue
        if len(l) >= 2:
            dynasty_list.append(l[0])
            name_list.append(l[1])
        else:
            dynasty_list.append(l[0])
            name_list.append(l[0])
    
file = pd.read_csv('raw_data.csv', encoding='utf-8')
file_new = file.drop('年代 作者', axis=1)
file_new['年代'] = dynasty_list
file_new['作者'] = name_list
file_new.to_csv('data.csv', mode='a', index=False)

# TODO: 统一年代的称谓
# 事实上是成画的时间而不是作者的年代
# 所以似乎也没有问题？

# print(name_list)