import csv

name_list = []
url_list = []

url = 'http://g2.ltfc.net/suhaindex?author=NAME&current=1&pageSize=12'

with open('中华珍宝馆-书画家数据.csv', encoding='utf-8')as f:
    f_csv = csv.reader(f)
    for row in f_csv:
        name = row[0]
        # print(row[0])
        name_list.append(name)
        new_url = url.replace('NAME', name)
        url_list.append(new_url)

print(url_list)