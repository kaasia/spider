# -*- coding: utf-8 -*-
'''
删除目录下面男性的图片
'''
import os 
def test():
    g = os.walk("D:\workspaces\python\all-my-spider")
    for path,d,filelist in g:  
        for filename in filelist:
            if filename.endswith('jpg'):
                print (os.path.join(path, filename))


if __name__ == '__main__':
    test()
