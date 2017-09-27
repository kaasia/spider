# -*- coding: utf-8 -*-
'''
爬取山大继续教育学院管理系统，爬取学生照片
'''
import requests
from selenium import webdriver
from selenium.webdriver.support.select import Select
import time
from bs4 import BeautifulSoup
from lxml import etree

def login1(url):
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(5)
    js = 'document.getElementsByClassName("zaf_ul")[0].style.display="block";' 
    driver.execute_script(js)
    time.sleep(5)
    driver.find_element_by_xpath("/html/body/div[3]/div/ul/li/div/ul/li[2]/a").click()
    time.sleep(5)
def login2(url):
    driver = webdriver.Chrome()
    driver.get(url)
    driver.find_element_by_xpath('//*[@id="userName"]').send_keys("*****")
    driver.find_element_by_xpath('//*[@id="passWord"]').send_keys("*****")
    time.sleep(5)
    #等手动输入验证码
    driver.find_element_by_xpath('//*[@id="loginForm"]/table/tbody/tr[4]/td[2]/input').click()
    time.sleep(2)
    driver.find_element_by_xpath('//*[@id="main"]/div[1]/div/div[2]/div/ul/li[5]/p/a').click()
    time.sleep(2)
    driver.find_element_by_xpath('//*[@id="main"]/div[1]/div/div[2]/div/ul/li[5]/ul/li[1]/a').click()
    time.sleep(2)
    driver.find_element_by_xpath('//*[@id="main"]/div[1]/div/div[2]/div/ul/li[5]/ul/li[1]/ul/li[1]/a').click()
    time.sleep(5)
    driver.switch_to.frame("frame_content")
    for page in range(1,14551):
        js2 = 'location.href=\"/xs/xsxx/list/3?currentPage='+str(page)+'&pageSize=10&ssxxzx=&zyid=&zxnjid=&ccid=&xh=&xm=&zjh=&xjzt=&zhsxtj=\"'
        driver.execute_script(js2)
        time.sleep(3)
        imgs = driver.find_elements_by_class_name('samllImg')
        for i in range(0,len(imgs)):
            #data = etree.HTML(driver.page_source)d
            download(imgs[i].find_element_by_xpath('.//img').get_attribute("src"))
        
def download(attribute):
        print("download:"+attribute)
        file_name = attribute.split('/')[-1]
        r = requests.get(attribute,stream=True)
        with open(file_name,'wb') as f:
            for chunk in r.iter_content(chunk_size=1024*1024):
                if chunk:
                    f.write(chunk)
        print("%s download!\n" %file_name)



    

if __name__ == '__main__':
    url = ""
    url2 = ""
    login2(url2)