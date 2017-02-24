#!-*-coding:utf-8-*-

import cv2
import numpy as np
import urllib as ub
import urllib2 as ub2
import random
import os, uuid

'''训练数据处理工具'''

# 长江大学教务处登录页

url = 'http://jwc2.yangtzeu.edu.cn:8080/'

# 验证码保存路径
pic = 'TrainPicture'
lab = 'Labels'
localPath = '/home/luochong/PycharmProjects/LoginSimulation/'

# 验证码上字距、下字距
top = 7
bottom = 10


class dealcode(object):
    def __init__(self, filepath=localPath + pic, filename='checkPic_YU.jpeg'):
        self.filepath = filepath
        self.filename = filename
        self.totalpath = filepath + '/' + filename

    def _create_file_with_filename_(self):
        file = open(self.totalpath, 'a+')
        file.close()

    def _generate_image_(self):
        try:
            ub.urlretrieve(url + '/verifycode.aspx', self.totalpath)
            return True
        except:
            return False

    def _remove_line_(self, img):
        # 去掉上下空白
        newimg = np.zeros(img.shape, np.uint8)
        newimg = cv2.resize(newimg, (img.shape[1], img.shape[0] - top - bottom), interpolation=cv2.INTER_CUBIC)
        for i in range(7, 20):
            for j in range(img.shape[1]):
                newimg[i - top, j] = img[i, j]
        # 记录直线所在行
        line = []
        for i in range(newimg.shape[0]):
            hasline = False
            if newimg[i, 0] < 100:
                line.append(i)
                hasline = True
            for j in range(newimg.shape[1]):
                if hasline:
                    newimg[i, j] = 0
                else:
                    if newimg[i, j] < 100:
                        newimg[i, j] = 255
                    else:
                        newimg[i, j] = 0
        # top 7 left 7-10 bottom 10
        return newimg

    def _split_word_(self, newimg):
        result = []
        left, right = 0, 1
        for j in range(newimg.shape[1]):
            countBlack = 0
            for i in range(newimg.shape[0]):
                if newimg[i, j] == 255:
                    if left < right:
                        left = j
                        break
                # countWhite到12时还未找到黑色像素，即此列都为白色
                elif left > right and countBlack == 12:
                    right = j
                    labelimg = cv2.resize(np.array([[0] * 13] * 13, dtype=newimg.dtype), (13, 13),
                                          interpolation=cv2.INTER_CUBIC)
                    try:
                        for m in range(13):
                            index = 0
                            for n in range(left, right):
                                labelimg[m, index] = newimg[m, n]
                                index += 1
                        result.append(labelimg)
                    except IndexError:
                        print '字符切割失败，重新获取验证码'
                        return []
                else:
                    countBlack += 1
        return result

    def _deal_image_(self):
        img = cv2.imread(self.totalpath, cv2.IMREAD_GRAYSCALE)
        img = self._remove_line_(img)
        result = self._split_word_(img)
        # 如果出现分割越界，则递归重新获取数据
        if len(result) == 0:
            print '验证码重新获取...'
            while len(result) == 0:
                if self._generate_image_():
                    img, result = self._deal_image_()
            print '验证码重新获取成功'
        return img, result

    @staticmethod
    # 0-9 10个数字 加上 26 个英文字母
    def _one_hot_(label, num_classes=36):

        num_labels = label.shape[0]
        index_offset = np.arange(num_labels) * num_classes
        labels_one_hot = np.zeros((num_labels, num_classes))
        labelNum = []
        # 将数字1写在对应位置上
        for i in label:
            # 为数字
            if ord(i) <= 57:
                chrvalue = ord(i) - 48
            else:
                # 为字母，先将其转为大写，前面有10个数字，要加10
                chrvalue = ord(str(i).upper()) - 65 + 10
            labelNum.append(chrvalue)
        newlabel = np.array(labelNum)
        labels_one_hot = labels_one_hot.astype(np.float32)
        labels_one_hot.flat[index_offset + newlabel.ravel()] = 1.
        return labels_one_hot

    @staticmethod
    # 返回一维图像
    def _get_image_(img2d, gblur=True):
        newimg = []
        for i in img2d:
            if gblur:
                i = cv2.GaussianBlur(i, (3, 3), 1.5)
            i.astype(np.float32)
            i = np.multiply(i, 1.0 / 255.0)
            newimg.append(np.ravel(i))
        return np.array(newimg)


if __name__ == '__main__':
    d = dealcode()
    img, result = d._deal_image_()
        # cv2.imshow('img', img)
        # cv2.imshow('1', result[0])
        # cv2.imshow('1', result[1])
        # cv2.imshow('1', result[2])
        # cv2.imshow('1', result[3])
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
