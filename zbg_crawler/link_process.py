import csv

name_list = []
url_list = []

url = 'http://g2.ltfc.net/suhaindex?author=NAME&current=NUM&pageSize=12'

with open('中华珍宝馆-书画家数据.csv', encoding='utf-8') as f:
    f_csv = csv.reader(f)
    for row in f_csv:
        name = row[0]
        # print(row[0])
        if '佚名' in name or '敦煌' in name:
            continue
        if '爱新觉罗' in name:
            name = name.replace('爱新觉罗', '')
            name = name.replace('·', '')
        elif len(name) >= 5:
            continue
        name_list.append(name)
        tmp_url = url.replace('NAME', name)
        for i in range(1, 21):
            new_url = tmp_url.replace('NUM', str(i))
            url_list.append(new_url)

print(url_list)

with open('links.csv', 'w', newline='', encoding='utf-8') as writefile:
    writer  = csv.writer(writefile)
    for row in url_list:
        writer.writerow([row])
