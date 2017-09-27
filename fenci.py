#利用Jieba进行分词
# encoding=utf-8
import jieba
import json


f = open('test.json','r',encoding='utf-8')
result = open('result.txt','w+',encoding='utf-8')
jokes = json.load(f)
for joke in jokes:
    words = jieba.cut(joke['joke'], cut_all=True)
    for w in words:
        if(len(w)!=0):
            print(w.strip())
            result.write(str(w.strip())+'\n') #写入txt文档  




