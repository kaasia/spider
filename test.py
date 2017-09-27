# coding = utf-8

from selenium import webdriver
import time
driver = webdriver.Chrome()

driver.get('https://www.zhihu.com#signin')

print(driver.title)

driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/div[2]/div[1]/div[1]/div[2]/span").click()
driver.find_element_by_name("account").send_keys("15064156315")
driver.find_element_by_name("password").send_keys("zhihu@ABCD1234")
time.sleep(10)
driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/div[2]/form/div[2]/button").click()
#driver.quit()