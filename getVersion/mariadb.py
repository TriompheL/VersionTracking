#coding=utf-8

import requests
from lxml import etree
import re

def get_latest_version():
    """
    获取最新稳定版本
    :return:
    """
    url ="https://mariadb.org/"
    try:
        res=requests.get(url=url)
        datas=res.text
    except Exception as e:
        print(e)
    list=[]
    html = etree.HTML(datas)
    result = html.xpath("//section[@id='text-15']/div/p/strong/a")

    for item in result:
        list.append(item.text)

    return list

def get_security_version():
    """

    :return:
    """
    url_series=['https://mariadb.com/kb/en/release-notes-mariadb-101-series/','https://mariadb.com/kb/en/release-notes-mariadb-102-series/',
                'https://mariadb.com/kb/en/release-notes-mariadb-103-series/','https://mariadb.com/kb/en/release-notes-mariadb-104-series/',
                'https://mariadb.com/kb/en/release-notes-mariadb-105-series/']
    url="https://mariadb.com/kb/en/security/"
    try:
        res=requests.get(url=url)
        datas=res.text
    except Exception as e:
        print(e)
    list=[]
    html = etree.HTML(datas)
    result = html.xpath("//ul[@class='cves']/li/a")
    version_list=[]
    #因为目前稳定版本是10.x.x 所以去掉其他开头的
    pattern=re.compile('10\.\d+\.\d+')
    for item in result:
        if 'MariaDB' in item.text:
            version=re.findall(pattern,item.text)
            if len(version)!=0:
                version_list.append(version[0])
    # print(version_list)
    #存储第二位版本号对应的最大的第三位版本号。如 10.2.xx xx为最大
    dict={}
    #处理 10.x.x
    for item in version_list:
        list=item.split('.')
        if list[1] in dict.keys():
            if int(list[2]) > int(dict[list[1]]):
                dict[list[1]]=list[2]
        else:
            dict[list[1]]=list[2]
    list=[]
    for i in dict:
        list.append('10.'+str(i)+'.'+dict[i])
    return list

def get_version():
    lat_ver=get_latest_version()
    sec_ver=get_security_version()
    return {"security":sec_ver,"latest":lat_ver}