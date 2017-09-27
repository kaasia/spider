#读取文件生成词云
# encoding=utf-8
from os import path
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud,ImageColorGenerator


d = path.dirname(__file__)
alice_coloring = np.array(Image.open(path.join(d, "3.png")))

text_from_file_with_apath = open('result.txt',encoding='utf-8').read()
wc = WordCloud(background_color = 'white', max_words=2000, mask=alice_coloring, max_font_size=70, random_state=42)
wc.generate(text_from_file_with_apath)

image_colors = ImageColorGenerator(alice_coloring)
# show
plt.figure()  
# 以下代码显示图片  
plt.imshow(wc)  
plt.axis("off")  
plt.show()  
# 绘制词云 
# 保存图片  
wc.to_file(path.join(d, "名称.png")) 