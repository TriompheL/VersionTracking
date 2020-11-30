#coding=utf-8

import requests
from lxml import etree
import re
import json


def get_latest_version():
    url = "http://nginx.org/"
    pattern=re.compile("nginx-\d\.\d{2}\.\d{1,2}")
    try:
        res = requests.get(url=url)
        datas = res.text
    except Exception as e:
        print(e)
    html = etree.HTML(datas)
    result = html.xpath("//tr/td/p")
    list=[]
    re_content=""
    for item in result:
        content=str(etree.tostring(item))
        if 'stable version' in content:
            re_content=content
            break
    #nginx-1.18.0 提取版本号
    values=re.findall(pattern,re_content)
    if len(values)!=0:
        value=values[0].split('-')
        list.append(value[1])
    return list

def get_security_version():
    url = "http://nginx.org/en/security_advisories.html"
    pattern=re.compile("(?<=Not vulnerable:\s)\d\.\d{2}\.\d{1,2}")
    try:
        res = requests.get(url=url)
        datas = res.text
    except Exception as e:
        print(e)
    html = etree.HTML(datas)
    result = html.xpath("//*[@id='content']/ul/li[1]/p")
    list=[]
    if len(result)!=0:
        item=result[0]
        html=str(etree.tostring(item))
        version=re.findall(pattern,html)
        list.append(version[0])
    return list

def get_version():
    lat_ver=get_latest_version()
    sec_ver=get_security_version()
    return {"security":sec_ver,"latest":lat_ver}

# if __name__ == '__main__':
#     print(get_version())