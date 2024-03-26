import os
import json
import time
import requests

url = input('请输入欲爬取的采集链接\n')
id = url.split('/')[4]
api = "https://api.huaban.com/boards/"+id+"/pins?limit=40&fields=pins:PIN,board:BOARD_DETAIL,check"
result = requests.get(api)
result.encoding = "utf-8"
arr = json.loads(result.text)
# 时间获取
timestamp = time.time()
timelocal = time.localtime(timestamp)
timecurrentymd = time.strftime("%Y-%m-%d", timelocal)
timecurrenthms = time.strftime("%H-%M-%S ", timelocal)
begin = time.strftime("%H:%M:%S ", timelocal)
filename = timecurrenthms + id
print('正在检查文件夹……')
# 创建save文件夹
dirs = 'save'
if not os.path.exists(dirs):
    os.makedirs(dirs)
# 创建天数文件夹
dirs = 'save\\' + timecurrentymd
if not os.path.exists(dirs):
    os.makedirs(dirs)
# 创建任务文件夹
filetask = 'save\\'+ timecurrentymd + "\\" + filename 
if not os.path.exists(filetask):
    os.makedirs(filetask)
# 创建PIC文件夹
filepic = 'save\\'+ timecurrentymd + "\\" + filename + "\\" + "pic"
if not os.path.exists(filepic):
    os.makedirs(filepic)
print('正在书写缓存……')
f = open(filetask + "\\" +  filename + '.json\\','w' ,encoding='utf-8')
f.write(result.text)
f.close()
total = 0
max = 0
all = arr['board']['pin_count']
while (True):
    if (max != 0):
        api = "https://api.huaban.com/boards/" + id + "/pins?limit=40&max=" + str(max) + "&fields=pins:PIN,board:BOARD_DETAIL,check"
        result = requests.get(api)
        result.encoding = "utf-8"
        arr = json.loads(result.text)
    index = 0
    for fruit in arr['pins']:
        timestamp = time.time()
        timelocal = time.localtime(timestamp)
        timecurrenthms = time.strftime("%H:%M:%S", timelocal)
        print(timecurrenthms + ': 正在保存第' + str(total + 1) + '/'+ str(all) +'张')
        key = arr['pins'][index]['file']['key']
        r = requests.get('https://gd-hbimg.huaban.com/' + key)
        type = arr['pins'][index]['file']['type']
        type = type.split('/')[1]
        filename = key + '.' + type
        with open(filepic + "\\" + filename, "wb") as f:
            f.write(r.content)
            total = total + 1
        max = arr['pins'][index]['pin_id']
        index = index + 1
    if (total == all):
        break
print('爬取完毕~\n开始时间：' + begin + '\n结束时间：' + timecurrenthms + '\n共获取：' + str(all) +'张图片')
    