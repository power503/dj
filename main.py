# -*- coding: utf-8 -*-
"""
Created on Wed Jan 28 17:20:46 2026

@author: admin
"""

import requests,time,random
from lxml import html
from datetime import datetime






# 创建会话
session = requests.Session()



def parse_ip_info(html_content):
    """
    解析HTML中class为result的div内容
    跳过包含"失效"的条目
    提取IP地址、物理地址和URL
    """
    # 解析HTML
    tree = html.fromstring(html_content)
    
    # 查找所有class为"result"的div
    result_divs = tree.xpath('//div[@class="result"]')
    
    extracted_data = []
    
    for div in result_divs:
        # 获取div的文本内容
        div_text = div.text_content()
        
        # print(div_text)
        
        # 检查是否包含"失效"字符串
        if "About" in div_text:
            continue  # 跳过包含"失效"的div
        
        # 检查是否包含"失效"字符串
        if "失效" in div_text:
            continue  # 跳过包含"失效"的div
        
        # print(div_text)
        
        # 提取物理地址（从<i>标签中）
        location_element = div.xpath('.//i')
        if location_element:
            # 物理地址在<i>标签内
            location_text = location_element[0].text_content().strip()
            # 处理物理地址文本
            if "上线" in location_text:
                physical_address = location_text.split("上线", 1)[1].strip()
            else:
                physical_address = location_text
        else:
            physical_address = "未找到物理地址"
        
        # 提取URL地址（从包含IP的<a>标签的href属性）
        url_element = div.xpath('.//a[1]/@href')
        if url_element:
            url_address = "http://foodieguide.com/iptvsearch/"  + url_element[0]
        else:
            url_address = "未找到URL"
            
        ip_address = "未知"
        parsed_url = urlparse(url_address)
        params = parse_qs(parsed_url.query)
        
        ip_address = params.get('ip', [None])[0]
        # print(f"提取的IP地址: {ip_address}")
        
        tk = params.get('tk', [None])[0]
        p = params.get('p', [None])[0]
        
        # 将提取的信息添加到列表
        extracted_data.append({
            "IP": ip_address,
            "address": physical_address,
            "URL": url_address,
            "tk":tk,
            "p":p
            
        })
        
        # 筛选 address 包含 "联通" 或者 的项
        result = [
            item for item in extracted_data if "联通" in item.get("address", "") 
            or "阿里云" in item.get("address", "")
            or "贵州" in item.get("address", "")
            ]
    
    return result


def extract_channels(html_string):
    """
    从HTML字符串中提取符合条件的频道信息。
    
    参数:
        html_string (str): 要解析的HTML字符串。
    
    返回:
        list: 包含字典的列表，每个字典有'name'和'url'两个键。
    """
    # 1. 解析HTML
    tree = html.fromstring(html_string)
    
    # 2. 查找所有class为"result"的div元素
    result_divs = tree.xpath('//div[@class="result"]')
    
    extracted_channels = []
    
    for div in result_divs:
        # 获取当前div内的所有文本内容（用于规则判断）
        div_text = div.text_content()
        
        # 3. 应用规则1: 如果包含“来自”，则跳过
        if "来自" in div_text:
            # print(f"跳过包含'来自'的div: {div_text[:30]}...")
            continue
        
        # 4. 应用规则2: 如果不包含“来自”，则进行提取
        # 提取频道名称（从tip div中）
        channel_name_elem = div.xpath('.//div[@class="tip" and @data-title="Play with PC"]')
        if channel_name_elem:
            channel_name = channel_name_elem[0].text_content().strip()
        else:
            channel_name = ""
            print(f"警告: 在div中未找到频道名称元素")
        
        # 提取频道URL（从m3u8表格中）
        url_elem = div.xpath('.//td[contains(text(), "http://")]')
        if url_elem:
            channel_url = url_elem[0].text_content().strip()
        else:
            channel_url = ""
            print(f"警告: 在div中未找到URL元素")
        
        if channel_name and channel_url:
            extracted_channels.append({
                "name": channel_name,
                "url": channel_url
            })
            # print(f"提取到频道: {channel_name} -> {channel_url}")
        else:
            print(f"警告: 在div中找到了元素，但名称或URL为空。")
    
    return extracted_channels



def get_detail_info(url,ip,tk,p):
    
    headers = {
        "Accept": "*/*",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Pragma": "no-cache",
        "Referer": url,
        "Host": 'foodieguide.com',
        "Pragma": 'no-cache',
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
    }
    
    url = f"http://foodieguide.com/iptvsearch/getall.php?ip={ip}&c=&tk={tk}&p={p}"
    
    print("url:",url)
    
    # response = session.get(h, headers=headers)
    # print("\n\n\nresponse.text:"+response.text + "\n\n\n")
    # time.sleep(3)
    response = session.get(url, headers=headers)

    # print("\n\n\nresponse.text:"+response.text + "\n\n\n")
    # print(response)
    
    
        
    # 执行提取
    channels = extract_channels(response.text)
    
    # print('执行提取的详细信息:',channels)
    # print('执行提取的频道数量:',len(channels))
    
    # 打印最终结果
    # print("\n=== 最终提取结果 ===")
    # for idx, channel in enumerate(channels, 1):
    #     print(f"{idx}. 频道名称: {channel['name']}")
    #     print(f"   URL地址: {channel['url']}\n")
        
    return channels

def wait(a,b):
    w = random.randint(a, b)
    print(f'等待{w}秒...')
    time.sleep(w)

def main(urls_template,max_page):
    
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded",
        "Origin": "http://foodieguide.com",
        "Pragma": "no-cache",
        "Referer": "http://foodieguide.com/iptvsearch/",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36"
    }
    
    iptv_urls_lists=[]
    
    for page_num in range(1, 1+max_page):  # 生成 1 到 10
        for template in urls_template:
            
            full_url = template.format(page=page_num)
            print(full_url)  # 或存入列表，或发起请求
            
            wait(3,5)
            try:
                r = session.get(full_url,headers=headers)
                ip_lists = parse_ip_info(r.text)
                # print(ip_lists)
                
                for ip_item in ip_lists:
                    print("当前ip_item:",ip_item)
                    
                    url = ip_item.get("URL","")
                    if url != "":
                        try:
                            ip = ip_item.get("IP","")
                            tk = ip_item.get("tk","")
                            p = ip_item.get("p","")
                            print(f"\nip:{ip},  tk:{tk},  p:{p}")
                            wait(3,6)
                            iptv_url = get_detail_info(url,ip,tk,p)
                            iptv_urls_lists = iptv_urls_lists + iptv_url
                            
                        except Exception:
                            print('error1')

                
            except Exception:
                print('error2')
    
    print("\n\n获取的频道列表:",iptv_urls_lists)
    
    print("\n\n获取的频道数量:",len(iptv_urls_lists))
    
    


    with open('live.txt', 'w', encoding='utf-8') as f:
        f.write(f"# created at {datetime.now().strftime('%Y%m%d_%H%M%S')}\n")
        for item in iptv_urls_lists:
            f.write(f"{item['name']},{item['url']}\n")


        


if __name__ == "__main__":
    
    
    
    urls_template=[
        "http://foodieguide.com/iptvsearch/iptvhotel.php?page=1&iphone16=&code=",
        "http://foodieguide.com/iptvsearch/iptvmulticast.php?page=1&iphone16=&code="
        ]
    
    
    
    max_page = 15
    
    main(urls,max_page)
    
    
    
                
