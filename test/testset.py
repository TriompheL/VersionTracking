import re
import requests
from lxml import etree

url_list = ['https://tomcat.apache.org/tomcat-9.0-doc/changelog.html',
            'https://tomcat.apache.org/tomcat-8.5-doc/changelog.html']
# 匹配CVE
pattern = re.compile("CVE-\d{4}-\d+")
# 匹配版本号 使用正向肯定预查
pattern2 = re.compile("(?<=Tomcat_)[789]\.\d+\.\d+")
version_list = []
'''
开始处理7.0的页面
'''
url_7 = "https://tomcat.apache.org/tomcat-7.0-doc/changelog.html"
try:
    res = requests.get(url=url_7)
    datas = res.text
except Exception as e:
    print(e)
html = etree.HTML(datas)
result = html.xpath("//td[@id='mainBody']/table")
version_text = ""
for item in result:
    sub_html = str(etree.tostring(item))
    print(sub_html)
    cve = re.findall(pattern, sub_html)
    if len(cve) != 0:
        version_text = sub_html
        break
version_end = re.findall(pattern2, version_text)
if len(version_end) != 0:
    version_list.append(version_end[0])

print(version_list)