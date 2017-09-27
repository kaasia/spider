# -*- coding: utf-8 -*-
'''
对报名山大继续教育的学生进行年龄阶段统计
'''
import xlrd
from collections import Counter
import numpy as np    
import matplotlib.mlab as mlab    
import matplotlib.pyplot as plt 
#211322199508142022
def getAge(id):
    if(len(id)==18):
        age = id[6:10]
        current_year = 2017
        if(current_year-int(age)==75):
            print(id)
        return current_year-int(age)
    else:
        return 0

def readExcel(filename):
    data = xlrd.open_workbook(filename)
    table = data.sheets()[0]
    #定位到身份证列
    cols = table.col_values(8)
    return cols
if __name__ == '__main__':

    
    cols = readExcel('学生信息管理.xls')
    ages = []
    for i in range(1,len(cols)):
       ages.append(getAge(cols[i]))
    print(len(ages))
    cnt = Counter(ages)
    print(cnt)
    x = []
    y = []
    for each in cnt.items():
        (a,b) = each
        x.append(a)
        y.append(b)
    fig = plt.figure()  
    plt.bar(x,y,0.8,color="green")  
    plt.xlabel("X-axis")  
    plt.ylabel("Y-axis")  
    plt.title("bar chart")  
    x_label=[0,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85]
    plt.xticks(x, x_label, rotation=0)  
    plt.show()    
    plt.savefig("barChart.jpg")