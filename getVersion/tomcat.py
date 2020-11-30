import xml.etree.ElementTree as ET
from lxml import etree
import requests
import re
import json


def get_latest_version():
    url="https://tomcat.apache.org/"
    try:
        res = res=requests.get(url=url)
        datas = res.text
    except Exception as e:
        print(e)
    html = etree.HTML(datas)
    result = html.xpath("//div[@id='content']/h3")
    list=[]
    pattern=re.compile("[7-9]\.\d+\.\d+")
    for item in result:
        temp=item.attrib['id']
        result=re.findall(pattern,temp)
        if len(result)!= 0:
            list.append(result[0])
    return list

def get_security_version():

    url_list=['https://tomcat.apache.org/security-9.html','http://tomcat.apache.org/security-8.html','http://tomcat.apache.org/security-7.html']
    # 匹配版本号 使用正向肯定预查
    pattern2=re.compile("(?<=Fixed_in_Apache_Tomcat_)[789]\.\d+\.\d+")
    version_list=[]
    for url in url_list:
        try:
            res = requests.get(url=url)
            datas = res.text
        except Exception as e:
            print(e)
        html = etree.HTML(datas)

        result = html.xpath("//div[@id='content']/*")
        version_text = ""
        for i in range(len(result)):

            if result[i].tag =='div':
                sub_html=str(etree.tostring(result[i]))
                if "Important:" in sub_html:
                    end_html=str(etree.tostring(result[i-1]))
                    version=re.findall(pattern2,end_html)[0]
                    version_list.append(version)
                    break
    return version_list

def get_version():
    lat_ver=get_latest_version()
    sec_ver=get_security_version()
    return {"security":sec_ver,"latest":lat_ver}


if __name__ == '__main__':
    print(get_security_version())