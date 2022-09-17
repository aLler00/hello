from selenium.webdriver import Firefox
from selenium.webdriver import FirefoxOptions
import time,re
from bs4 import BeautifulSoup
import pandas as pd
from pyecharts.charts import Geo
from pyecharts import options as opts
from pyecharts.globals import ThemeType

option = FirefoxOptions()
option.add_argument("--headless")  # 隐藏浏览器
# option.add_argument('--no-sandbox')
browser = Firefox(executable_path='geckodriver',options=option)
url = "http://www.nhc.gov.cn/xcs/yqtb/list_gzbd.shtml"
browser.get(url)
time.sleep(3)   #火狐需要人为等待，设置等待时间为5s
# print(browser.page_source)     #查看源码
def getContent(html):
    bsobj=BeautifulSoup(html,'html.parser')
    time.sleep(10)
    cnt=bsobj.find('div',attrs={"id":"xw_box"}).find_all("p")
    time.sleep(10)
    s=""
    if cnt:
        for item in cnt:
            s+=item.text
        return s
#全部连接
alls = browser.find_elements_by_css_selector("li a")
for i in alls:
    print(i.get_attribute('href'),i.text)   #i.get_attribute('href')是首页所有连接（不打算写其他页了）

new_url = browser.find_element_by_css_selector("li a").get_attribute('href')   #以一个为例
browser.get(new_url)
time.sleep(3)
news = browser.page_source
content = getContent(news)
#print(content)
regex = re.compile('；本土病例[0-9]+例（.{3,200}），含')
x = regex.findall(content)
regex1=re.compile('（.{3,300}）')
y=regex1.findall(str(x))
#print(y)
regex2=re.compile('[^例）（，]+')
k=str(y).removeprefix('[')
z=regex2.findall(k)
z=str(z).removeprefix('[')
regex3=re.compile('[0-9]+')
l=regex3.findall(str(z))
regex4=re.compile('[\u4e00-\u9fa5]+')
m=regex4.findall(str(z))
#print(l)
#print(m)
cont = dict(zip(m,l))
#print (cont)
key = list(cont.keys())
value = list(cont.values())
#print(key)
#print(value)

# 利用pandas模块先建立DateFrame类型，然后将两个上面的list存进去
'''
result_excel = pd.DataFrame()
result_excel["省份"] = key
result_excel["新增确诊病例"] = value
# 写入excel
result_excel.to_excel('9.16新增确诊病例.xlsx')
'''

regex5=re.compile('新增无症状感染者[0-9]+例，其中境外输入[0-9]+例，本土[0-9]+例（.{3,300}）')
a= regex5.findall(content)
#print(a)
regex6=re.compile('当日解除医学观察的无症状感染者[0-9]+例，其中境外输入[0-9]+例，本土[0-9]+例（.{3,300}）')
b=regex6.findall(str(a))
regex7=re.compile('（.{3,300}）')
c=regex7.findall(str(b))
regex8=re.compile('[^例）（，]+')
d=regex8.findall(str(c))
regex9=re.compile('[0-9]+')
e=regex9.findall(str(d))
regex10=re.compile('[\u4e00-\u9fa5]+')
f=regex10.findall(str(d))
cont1 = dict(zip(f,e))
#print (cont1)
key1 = list(cont1.keys())
value1 = list(cont1.values())
result_excel = pd.DataFrame()
result_excel["省份"] = key1
result_excel["新增无症状感染者"] = value1
# 写入excel
result_excel.to_excel('9.16新增无症状感染者.xlsx')
keys = cont.keys()
vals = cont.values()
lst = [(key, val) for key, val in zip(keys, vals)]


geo=Geo(init_opts=opts.InitOpts(theme=ThemeType.WHITE),is_ignore_nonexistent_coord = True)#初始化
geo.add_schema(maptype='china')#中国地图
geo.add('',lst,symbol_size=5,itemstyle_opts=opts.ItemStyleOpts(color="red"))#导入数据、设置图中点大小、颜色
geo.set_series_opts(label_opts=opts.LabelOpts(is_show=False),type='effectScatter')#设置画图类型
geo.set_global_opts(visualmap_opts=opts.VisualMapOpts(min_=1,max_=1000),title_opts=opts.TitleOpts(title="疫情分布",pos_left="center"))#设置岗位阈值、标题位置
geo.render("疫情分布.html")#存储成html格式




