#coding=utf-8

import requests
from lxml import etree
import re
import json


def get_latest_version():
    url = "https://projects.apache.org/json/foundation/releases.json"
    try:
        res = requests.get(url=url)
        datas = res.text
    except Exception as e:
        print(e)
    load_data=json.loads(datas)['httpd']
    list=[]
    for item in load_data.keys():
        if 'httpd' in item:
            item_list=item.split('-')
            list.append(item_list[1])
    return list

def get_security_version():
    url = "http://httpd.apache.org/security/vulnerabilities_24.html"
    try:
        res = requests.get(url=url)
        datas = res.text
    except Exception as e:
        print(e)
    html = etree.HTML(datas)
    result = html.xpath("//div[@id='apcontents']/h1")
    list = []
    for item in result:
        title=item.text
        if 'Fixed' in title:
            list.append(item.attrib['id'])
            break
    return list

def get_version():
    lat_ver=get_latest_version()
    sec_ver=get_security_version()
    return {"security":sec_ver,"latest":lat_ver}

# if __name__ == '__main__':
#     print(get_version())