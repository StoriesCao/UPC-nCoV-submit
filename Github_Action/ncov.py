import requests
import json,urllib,time,http
import time 
import math
import datetime
from datetime import timedelta


curr_time = datetime.datetime.now()
# UTC时间整体转换成北京时间
curr_time = curr_time + timedelta(hours=8)

#使用前请修改以下路径，例如 C:/cookie.txt
cookie_file='./cookies.txt' #保存cookie文件
user_file="./user.txt"   #用户信息文件
log_file="./result.txt"     #日志文件
cookie = http.cookiejar.LWPCookieJar(cookie_file)
handler = urllib.request.HTTPCookieProcessor(cookie)

# 模拟浏览器，要不然访问被拒绝了
headers_tmp = ('User-Agent','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',)
headers_2_tmp=('X-Requested-With', 'XMLHttpRequest')
opener = urllib.request.build_opener(handler)
opener.addheaders = [headers_tmp,headers_2_tmp]
with open(user_file,'r',encoding='utf8') as load_f:
    userinfo = json.load(load_f)
params = urllib.parse.urlencode(userinfo)
with opener.open('https://app.upc.edu.cn/uc/wap/login/check', data=bytes(params, 'utf-8')) as resp:
    print(resp.read().decode('utf-8'))
cookie.save(ignore_discard=True, ignore_expires=True)

headers1 = ('User-Agent','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',)
headers2=('X-Requested-With', 'XMLHttpRequest')
cookie = http.cookiejar.LWPCookieJar()
cookie.load(cookie_file, ignore_discard=True, ignore_expires=True)
handler = urllib.request.HTTPCookieProcessor(cookie)
opener = urllib.request.build_opener(handler)
opener.addheaders = [headers1,headers2]

with opener.open('https://app.upc.edu.cn/ncov/wap/default/index') as resp:
    result=json.loads(resp.read().decode("utf8"))['d']['oldInfo']
with opener.open('https://app.upc.edu.cn/ncov/wap/default/index') as resp:
    result1=json.loads(resp.read().decode("utf8"))['d']['info']

result["date"]=time.strftime("%Y%m%d", time.localtime())
result['created']=result1['created']
result['id']=result1['id']

with open(log_file,"a",encoding='utf8') as p :     
    jsObj = json.dumps(result)
    p.write("\n--------------------------\n")
    p.write(jsObj)
    p.write("\n"+time.ctime()+"\n--------------------------\n")
params = urllib.parse.urlencode(result)
with opener.open('https://app.upc.edu.cn/ncov/wap/default/save', data=bytes(params, 'utf-8')) as resp:
    print(resp.read().decode('utf-8'))

# 显示分7:06而不是7:6
if curr_time.minute < 10:
    str = '0' + str(curr_time.minute)
else:
    str = str(curr_time.minute)
    
dic = {"title": "签到成功",
       "body": f"UPC-疫情防控通已上报({curr_time.month}月{curr_time.day}日{curr_time.hour}:{str})",
       "group": "疫情防控通签到",
       "icon": "https://raw.githubusercontent.com/G-Cao/UPC-nCoV-submit/master/alarm.png"}

response = requests.request('get', f'https://api.day.app/qjUhpKS9bJxkCyrsSxUzU5/', json=dic)
print(response)
