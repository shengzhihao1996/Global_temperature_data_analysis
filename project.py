#!/usr/bin/python3
# encoding=utf-8
# pip install matplotlib  Pillow
# import numpy as np
import matplotlib.pyplot as plt
import os
import sys
from PIL import Image, ImageFont, ImageDraw
import csv

def main():
    # 如下变量用于最后的图片合成:
    IMAGES_PATH = './'  # 图片集地址
    IMAGE_SAVE_PATH = 'analysis.jpg'  # 图片转换后的地址
    IMAGE_NAMES = ['project.jpg','Q&A.jpg']  # 获取图片集地址下的所有图片名称

    # 如下变量用于数据算法：
    avg = 7  #移动平均值
    shanghai_avg_temp = []  #上海气温平均值
    global_avg_temp = []  #全球气温平均值

    # 打开csv文件，读取数据至list：
    f_csv = csv.reader(open('results.csv'))
    for row in f_csv:
        if not row[0] == 'year':  #首行不读取
          shanghai_avg_temp.append(row[1])
          global_avg_temp.append(row[2])

    # 执行算法，计算移动平均值，赋值回原list：
    shanghai_avg_temp = cal(shanghai_avg_temp,avg)
    global_avg_temp = cal(global_avg_temp,avg)
    

    # 美化出图效果，定制横轴刻度：
    year,x_ticks_lab,x_ticks_num = layout(shanghai_avg_temp)

    # 绘图细化参数：
    plt.figure(figsize=(10,4))  #创建绘图对象，1000*400
    plt.plot(year,shanghai_avg_temp,color="red",linewidth=3,label='shanghai_avg_temp')  #在当前绘图对象绘图（X轴，Y轴，红色虚线，线宽度）
    plt.plot(year,global_avg_temp,color="blue",linewidth=3,label='global_avg_temp')  #在当前绘图对象绘图（X轴，Y轴，蓝色虚线，线宽度）
    plt.xticks(x_ticks_num,x_ticks_lab)  #应用横轴刻度
    plt.legend(loc="best")  #自适应线条说
    plt.title('Global temperature data analysis')  #图片标题
    plt.xlabel("Time(year)")  #X轴标签
    plt.ylabel("temperature(℃)")  #Y轴标签
    plt.savefig(IMAGE_NAMES[0])  #图片保存到当前目录

    # 分析气温走势，回答给出的问题，转换图片：
    # question and answer：
    text = u'''
	        Q:1、与全球平均气温相比，你所在城市平均气温是比较热还是比较冷？长期气温差异是否一致？
	        A:与全球气温相比，我所在的城市是比较热的。长期的气温差异是一致的。\n
	        Q:2、长期以来，你所在城市气温变化与全球平均气温变化相比如何？
	        A:我所在的城市气温的上升趋势比较急促，全球气温上升趋势更为平缓。\n
	        Q:3、整体趋势如何？世界越来越热还是越来越冷了？气温走向与过去几百年的走向是否一致？
	        A:整体气温呈现上升趋势。世界越来越热了，气温走向没有变化，一直在上升。"\n
          Q:4、全球气温在逐步上升，导致这些现象背后的原因是什么？
          A:能源消耗暴增导致CO2排放量迅猛增加，在加上地球植被的缩减，消费者目前极度弱势于生产者，
          所以温室效应逐年加剧，年复一年的恶性循环，最后如图所示全球变暖。\n
'''
    # 上面代码格式错开是为了出图时的排版，出的图是对齐的。
    image = Image.new("RGB", (1000, 400), (255, 255, 255))  #图片大小，两个图保持一样大，合成方便
    draw = ImageDraw.Draw(image)  #绘制空白图片
    font = ImageFont.truetype(os.path.join("simsun.ttc"), 18)  #字体，大小
    draw.text((10, 4), text, font=font, fill="#000000")  #依据text的内容，字体，大小，背景底色，将文本写入图片
    image.save(IMAGE_NAMES[1])  #图片保存到当前目录

    # 执行图片合成函数：
    image_compose(IMAGES_PATH,IMAGE_SAVE_PATH,IMAGE_NAMES)  

# 移动平均值算法：
def cal(data,avg):
    i = avg-1  #要从第七个数值开始循环
    data_list = []  #定义空list存放最终返回值
    while i < len(data):  #获取传入列表长度
        j = i - avg + 1  #i - j = avg - 1
        reason = 0.00  #定义空浮点变量，准备计算平均值
        while j <= i:  
            reason+=float(data[j])  # 累加
            j+=1
        data_list.append(float('%.2f' % (reason / avg)))  #求平均值，追加list
        i+=1
    return data_list  # 返回list

# 横轴布局：
def layout(datalist):
    i=0
    year=[]
    j=1850 
    x_ticks_num=[]  # 刻度
    x_ticks_lab=[]  # 刻度所显示的标签
    while i < len(datalist):
        year.append(i)
        i+=1

    # 刻度间隔十,标签间隔十年
    i=0
    while i < len(datalist):
        x_ticks_num.append(i)
        x_ticks_lab.append(str(j))
        i+=10
        j+=10

    return year,x_ticks_lab,x_ticks_num

def image_compose(IMAGES_PATH,IMAGE_SAVE_PATH,IMAGE_NAMES):
    to_image = Image.new('RGB', (2048, 2048)) #创建一个新图
    # 循环遍历，把每张图片按顺序粘贴到对应位置上
    for y in range(1, 3):
        for x in range(1, 2):
            from_image = Image.open(IMAGES_PATH + IMAGE_NAMES[1 * (y - 1) + x - 1]).resize(
                (2048, 1024),Image.ANTIALIAS)
            to_image.paste(from_image, ((x - 1) * 2048, (y - 1) * 1024))
    to_image.save(IMAGE_SAVE_PATH)
    to_image.show()

main()