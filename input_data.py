# -*-coding:utf-8-*-

import cv2
import numpy as np
import os
import re
from deal_code import dealcode

'''训练数据获取及标注工具'''
dc = dealcode()

path = '/home/luochong/PycharmProjects/LoginSimulation/TrainPicture/'

while True:
    if dc._generate_image_():
        img, results = dc._deal_image_()
    while True:
        labelinput = raw_input('输入：\n')
        # 正则表达式
        check = re.search('[0-9a-zA-Z]{4}', labelinput)
        if check is not None:
            print '输入验证码成功'
            labelinput = list(labelinput)
            break
        else:
            print '输入错误'
    # result下标
    index = 0
    for i in labelinput:
        if ord(i) >= 65:
            i = str(i).upper()
        if not os.path.exists(path + str(i)):
            os.mkdir(path + str(i))
        # 统计目录下文件个数
        count = 0
        for root, dirs, files in os.walk(path + str(i)):
            for j in files:
                count += 1
        cv2.imwrite(path + str(i) + '/' + str(count + 1) + '.jpg', cv2.GaussianBlur(results[index], (3, 3), 1.5))
        index += 1
    nextstep = raw_input('是否退出？(y/n)')
    if nextstep == 'y':
        break
