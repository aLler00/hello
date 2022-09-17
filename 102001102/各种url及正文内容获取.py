
from selenium.webdriver import Firefox
from selenium.webdriver import FirefoxOptions
import time,re
from bs4 import BeautifulSoup
import requests
def getpageurl():#获得疫情官网中前7页的大url链接
    for page in range(1,8):
      if page ==1:
          yield "http://www.nhc.gov.cn/xcs/yqtb/list_gzbd.shtml"

      else:
        url='http://www.nhc.gov.cn/xcs/yqtb/list_gzbd_'+str(page)+'.shtml'
        yield url
def getContent(html):#获取大url链接中每个小url连接中正文的内容
    bsobj=BeautifulSoup(html,'html.parser')
    time.sleep(10)
    cnt=bsobj.find('div',attrs={"id":"xw_box"}).find_all("p")#获取正文内容
    time.sleep(10)
    s=""
    if cnt:
        for item in cnt:
            s+=item.text
        return s

    return "爬取失败！"
for url in getpageurl():
     soup = BeautifulSoup('<html><body><p>data</p></body></html>', 'lxml')
     option = FirefoxOptions()
     option.add_argument("--headless")  # 隐藏浏览器
     # option.add_argument('--no-sandbox')
     browser = Firefox(executable_path='geckodriver', options=option)
     browser.get(url)
     time.sleep(10)
     data=browser.page_source
     soup=BeautifulSoup(data,'lxml')
     #alls = browser.find_elements_by_css_selector("li a")
     #for i in alls:
        #print(i.get_attribute('href'), i.text)
     url_list= soup.find('div',class_='list').find_all('li')
     alls = browser.find_elements_by_css_selector("li a")
     for i in alls:
         print(i.get_attribute('href'), i.text)  # i.get_attribute('href')是首页所有连接（不打算
     for i in url_list:#获取每个url链接中所有的内容
         url='http://www.nhc.gov.cn/' + i.find('a')['href']
         #print(url)
         browser.get(url)
         news = browser.page_source
         #print(news)
         content=getContent(news)
         print(content)
'''
wb_data = requests.get(url)
ws_data=requests.get(url158)
soup = BeautifulSoup(wb_data.text, 'lxml')
soup1 = BeautifulSoup(ws_data.text, 'html.parser')
#soup1 = BeautifulSoup(open('index.html'))
print(soup1.prettify())
'''
