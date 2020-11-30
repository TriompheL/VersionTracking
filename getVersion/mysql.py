import xml.etree.ElementTree as ET
from lxml import etree
import requests
import re

def get_latest_version():
    """
    获取最新稳定版本
    :return: list
    """
    # 获取msyql信息的rss
    url = "https://dev.mysql.com/downloads/rss.php"
    list=[]
    try:
        res=requests.get(url=url)
        datas=res.text
    except Exception as e:
        print(e)
    #读取root信息
    root =ET.fromstring(datas)
    #遍历item
    for item in root.iter('item'):
        title=item.find('title').text
        if 'Community Server' in title:
            description=item.find('description').text
            pattern=re.compile(r'\d+\.\d+\.\d+(?=\sGA)')
            result=pattern.findall(description)
            if len(result)!=0:
                list.append(result[0])
    return list


def get_security_version():
    """
    获取最新安全稳定版本
    :return: list
    """
    releas_root_url=['https://dev.mysql.com/doc/relnotes/mysql/8.0/en/',
                     'https://dev.mysql.com/doc/relnotes/mysql/5.7/en/',
                     'https://dev.mysql.com/doc/relnotes/mysql/5.6/en/']
    list=[]
    for root_url in releas_root_url:
        sub_url_list = []
        security_version = ""
        try:
            res = requests.get(url=root_url)
            datas = res.text
        except Exception as e:
            print(e)

        html = etree.HTML(datas)
        result = html.xpath("//div[@class='docs-sidebar-nav-link']/a")
        pattern = re.compile('\d{4}-\d{2}-\d{2}.*General')
        # 获取所有的sub_url
        for item in result:
            find_result = re.findall(pattern, item.text)
            if len(find_result) != 0:
                sub_url_list.append(item.get('href'))
        temp=get_sub_url(root_url,sub_url_list)
        pattern2 = re.compile("\d+-\d+-\d+")
        version = re.findall(pattern2, temp)[0]
        version=version.replace('-', '.')
        list.append(version)
    return list

def get_sub_url(root_url,list):
    # 根据sub_url查看每个页面
    for sub_url in list:
        url = root_url + sub_url
        try:
            res = requests.get(url=url)
            datas = res.text
        except Exception as e:
            print(e)
        sub_html = etree.HTML(datas)
        sub_result = sub_html.xpath("//div[@class='section']/div[@class='itemizedlist']/ul/li/p/a")
        for sub_item in sub_result:
            if 'Security Notes' in sub_item.text:
                return sub_url
    return ""

def get_version():
    lat_ver=get_latest_version()
    sec_ver=get_security_version()
    return {"security":sec_ver,"latest":lat_ver}

if __name__ == '__main__':
    print(get_version())