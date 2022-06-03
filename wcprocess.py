# -*- codeing = utf-8 -*-
import MySQLdb
import jieba
from matplotlib import pyplot as plt    #绘图
from wordcloud import WordCloud         #词云
from PIL import Image                   #图片处理
import numpy as np                      #矩阵运算

def welf(data):
    lis = []
    for item in data:
        lis.append(' '.join(''.join(list(item)).split('|')))
    lis = ' '.join(lis)
    img = Image.open(r'img/sq.jpeg')
    img_array = np.array(img)
    wc = WordCloud(
        background_color='white',
        mask=img_array,
        font_path='msyh.ttc',
        collocations=False,
        width=400,
        height=300
    )
    wc.generate_from_text(lis)
    # fig = plt.figure(1)
    plt.imshow(wc)
    plt.axis('off')
    plt.savefig(r'img/welf.jpg', dpi=800)
def msg(data):
    stopwords = set()
    content = [line.strip() for line in open('templates/stopword.txt', 'r').readlines()]
    stopwords.update(content)
    text = ""
    for item in data:
        # print(item[0])
        text = text + item[0]
    cut = jieba.cut(text.replace('岗位已丢失', ''))
    string = ' '.join(cut)
    img = Image.open(r'img/sq.jpeg')
    img_array = np.array(img)
    wc = WordCloud(
        background_color='white',
        mask=img_array,
        font_path='msyh.ttc',
        collocations=False,
        width=400,
        height=300,
        stopwords=stopwords
    )
    wc.generate_from_text(string)
    # fig = plt.figure(1)
    plt.imshow(wc)
    plt.axis('off')
    plt.savefig(r'img/msg.jpg', dpi=800)