# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 17:18:16 2026

@author: LENOVO
"""

import requests,time,os
from datetime import datetime, timedelta


def write_log(msg):
    log_path = ""
    with open("gitee_stock_result.log", "a", encoding="utf-8") as f_txt:
        print('已写入log...')
        utc_now = datetime.utcnow()  # naive UTC 时间
        cst_now = utc_now + timedelta(hours=8)  # 变成 UTC+8 的 naive 时间
        f_txt.write(f"{cst_now}：{msg}\n")

def send_msg(numbers):
    # numbers = 【代码，名称，现价】
    
    # 从环境变量中读取 Token
    my_token = os.getenv("pushplus_TOKEN")
    u = f'http://www.pushplus.plus/send?token={my_token}&title={numbers[1]},价到达{numbers[2]}&content=代码：{numbers[0]}，</br>{numbers[1]}，</br>价格到达{numbers[2]}，</br>委托卖出价：{numbers[3]}'
    try:
        r1 = requests.get(u, timeout=50).json()
        print(f"通知发送结果: {r1}")
    except Exception as e:
        print(f"通知发送失败: {e}")


def get_tencent_hq(stock):
    headers = {
        "accept": "*/*",
        "accept-language": "zh-CN,zh;q=0.9",
        "cache-control": "no-cache",
        "pragma": "no-cache",
        "referer": "https://gu.qq.com/",
        "sec-ch-ua": "\"Not A(Brand\";v=\"8\", \"Chromium\";v=\"132\", \"Google Chrome\";v=\"132\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "script",
        "sec-fetch-mode": "no-cors",
        "sec-fetch-site": "cross-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36"
    }


    r=requests.get(f'https://qt.gtimg.cn/?q={stock}',headers=headers).text
    
    # print(r)
    
    # pattern = r'\d+\.\d+'
    # numbers = re.findall(pattern, r)
    
    numbers = r.split("~")
    
    # print(numbers)
    
    # 根据字符串结构，（索引1为股票名称，索引2为股票代码，索引3为最新价）
    if len(numbers) >= 3:
        now_price = float(numbers[3])
        # print('名称:',str(numbers[1]).strip(),'现价：',price)
        open_price = float(numbers[5])
        high_price = float(numbers[33])
        low_price = float(numbers[34])
        return {
                'now_price':now_price,
                'open_price':open_price,
                'high_price':high_price,
                'low_price':low_price
            }
    else:
        return {
                'now_price':0,
                'open_price':0,
                'high_price':0,
                'low_price':0
            }
        


r=requests.get('https://gitee.com/isforker/dj/raw/master/result_sell_stock.json').json()
print(r)

# 获取当前本地时间戳（秒）
current_time_sec = time.time()
target_time_sec = int(r.get('unix_time',0)) / 1000

# 得到的target_time_sec目标时间是北京时间，要转换为美国时间（UTC+0），即减去8个小时的时间，单位换算成为秒
target_time_sec =  target_time_sec - ( 8 * 60 * 60)



# 计算差值的绝对值（秒）
diff_seconds = abs(current_time_sec - target_time_sec)

if diff_seconds < 10 * 60: # 10分钟内

    if r.get('tencent_stock_code') and r.get('sell_price'):
        while True:
    
            tencent_stock_code = r.get('tencent_stock_code')
            
            my_price = float(r.get('sell_price'))
            
            tencent_price = get_tencent_hq(tencent_stock_code)
            # print(tencent_price)
            print(r.get('stock_name'),'，现价：',tencent_price.get('now_price'),"，目标价：",my_price)
            
            if(tencent_price.get('now_price') > my_price or (datetime.now().hour == 9 and tencent_price.get('high_price') > my_price)):
                
                send_msg([tencent_stock_code,r.get('stock_name'),tencent_price.get('now_price'),my_price])
                msg = f'代码：{tencent_stock_code}，{r.get("stock_name")}，价格到达{tencent_price.get("now_price")}，委托卖出价：{my_price}'
                write_log(msg)
                break
                
            time.sleep(3)
            
            if  datetime.now().hour >= 4 : # 对应北京时间的12点钟
                write_log('未在12点前达到价格要求，结束运行...')
                break
            
else:
    msg = '未读取到有效的信息:时间无效...end...'
    print(msg)
    write_log(msg)
    
time.sleep(60)
    
