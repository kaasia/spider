# coding=utf-8
import requests
import time
from selenium import webdriver
# 引入 datetime 模块
import datetime
import pymysql
import logging

#日志初始化
def initLog():
    logger = logging.getLogger(__name__)
    logger.setLevel(level = logging.INFO)
    handler = logging.FileHandler("log.txt")
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

def today():
    return time.strftime('%Y-%m-%d',time.localtime(time.time()))

def yesterday(): 
    today=datetime.date.today() 
    oneday=datetime.timedelta(days=1) 
    yesterday=today-oneday  
    return yesterday.strftime("%Y-%m-%d")
#爬取数据
def getZrjy(url):
    #可视化测试
    #driver = webdriver.Chrome()
    #无头浏览器
    driver = webdriver.PhantomJS(executable_path="phantomjs.exe") 
    driver.get(url)
    time.sleep(2)
    #获取日期
    the_time = yesterday()

    driver.find_element_by_xpath('/html/body/div[3]/div/div[1]/div[3]/ul/li[3]/a').click()
    #切换到数据框架，获取数据
    driver.switch_to.frame("content_main")
    table = driver.find_elements_by_xpath('/html/body/div[5]/div[2]/table/tbody')
    table = table[0]
    trs = table.find_elements_by_tag_name("tr")
    data = []
    for tr in range(1,len(trs)):
        tds = trs[tr].find_elements_by_tag_name("td")
        area = tds[0].find_element_by_xpath("div").text
        loupan = tds[1].find_element_by_xpath("div").text
        loupan = loupan.replace("#","号")
        ts = tds[2].find_element_by_xpath("div").text
        size = tds[3].find_element_by_xpath("div").text
        price = tds[4].find_element_by_xpath("div").text
        #print(area+','+loupan+','+ts+','+size+','+price)
        tempData = (the_time,area,loupan,ts,size,price)
        data.append(tempData)
    driver.close() #关闭当前页面
    driver.quit() #关闭所有由当前测试脚本打开的页面
    #print(data)
    return the_time,data
#数据库连接
def connectSql():
    db =  pymysql.connect("localhost","root","123456","fanchan",charset="utf8")
    return db

#数据库初始化
def initSql():
    db = connectSql()
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    # 使用 execute()  方法执行 SQL 查询 
    cursor.execute("SELECT VERSION()")
    # 使用 fetchone() 方法获取单条数据.
    data = cursor.fetchone()
    print ("Database version : %s " % data)
    # 关闭数据库连接
    # 使用预处理语句创建表
    cursor.execute("DROP TABLE IF EXISTS fanchan")
    sql = """CREATE TABLE `fanchan` (
        `id` int(11) NOT NULL AUTO_INCREMENT,
        `area` varchar(255) DEFAULT NULL COMMENT '地区',
        `loupan` varchar(255) DEFAULT NULL COMMENT '销售楼号',
        `ts` int(255) DEFAULT NULL COMMENT '成交套数',
        `size` float unsigned zerofill DEFAULT NULL COMMENT '成交面积',
        `price` float unsigned zerofill DEFAULT NULL COMMENT '成交单价',
        `date` varchar(255) NOT NULL COMMENT '成交日期',
        PRIMARY KEY (`id`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8;"""
    cursor.execute(sql)
    db.close()
#数据入库
def saveSql(the_time,data):
    db = connectSql()
    cursor = db.cursor()
    check_sql = ""
    if(len(data)>0):
        check_sql = "SELECT COUNT(1) from fanchan where date = '" + the_time + "';"
        insert_result = 0
        try:
            cursor.execute(check_sql)
            check_result = cursor.fetchone()
            if(check_result[0] == 0):
                insert_sql = ''
                sql = "INSERT INTO fanchan (date,area,loupan,ts,size,price) VALUES (%s,%s,%s,%s,%s,%s)"
                insert_result = cursor.executemany(sql,data)
                # 提交到数据库执行
                db.commit()
        except e:
            print(e.message)
            # 发生错误时回滚
            print("数据插入失败")
            db.rollback()
        #print("成功执行："+str(insert_result)+"条记录")
        logger.info(u"成功执行："+str(insert_result)+"条记录")
                    
                    

#url = 'https://cucc.tazzfdc.com/reisPub/pub/averageDailyStatist'
#data = {
#    'statisttype':'1',
#    'designUsages':'1'
#}
#headers = {
#    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
#}
#response = requests.get(url,headers=headers,params=data,verify=False)
#print(response.url)
#print(response.text)
def getUrl(url):
    data = {
        'statisttype':'1',
        'designUsages':'1'
    }
    response = requests.get(url,params=data,verify=False)
    print(response.text)

if __name__ == '__main__':
    
    logger = logging.getLogger(__name__)
    logger.setLevel(level = logging.INFO)
    handler = logging.FileHandler("log.txt",encoding='utf-8')
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    url="https://cucc.tazzfdc.com/reisPub/pub/"
    the_time,data = getZrjy(url)
    saveSql(the_time,data)