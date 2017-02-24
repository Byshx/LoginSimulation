# -*-coding:utf-8 -*-

import cv2
import tensorflow as tf
import numpy as np
import re
from deal_code import dealcode
import os
import random

'''TensorFlow模型训练工具'''

# checkpoint路径
protoname = 'model.ckpt'
protopath = '/home/luochong/PycharmProjects/LoginSimulation/proto/'
# 训练样本路径
path = '/home/luochong/PycharmProjects/LoginSimulation/TrainPicture/'
# 检测样本路径
testpath = '/home/luochong/PycharmProjects/LoginSimulation/TestPicture/'
# 暂存验证码路径
tmppath = '/home/luochong/PycharmProjects/LoginSimulation/tmpPicture/'
# 日志路径
logpath = '/home/luochong/PycharmProjects/LoginSimulation/logs/'

# 分割后的图片大小
pixels2d = 13 * 13
# 样本种类数 26个英文字母（大写）+ 10个数字（0-9）
label_classes = 36

sess = tf.InteractiveSession()

x = tf.placeholder(tf.float32, [None, pixels2d], name='x-input')
W = tf.Variable(tf.zeros([pixels2d, label_classes]), name='weights')
b = tf.Variable(tf.zeros([label_classes], name='bias'))
y_ = tf.placeholder(tf.float32, [None, label_classes], name='y-input')

with tf.name_scope('Wx_b'):
    y = tf.nn.softmax(tf.matmul(x, W) + b)

# Add summary ops to collect data
_ = tf.histogram_summary('weights', W)
_ = tf.histogram_summary('biases', b)
_ = tf.histogram_summary('y', y)

with tf.name_scope('xent'):
    cross_entropy = -tf.reduce_sum(
        y_ * tf.log(tf.clip_by_value(y, 1e-10, 1.0)))  # y --> tf.clip_by_value(y, 1e-10, 1.0)
    _ = tf.scalar_summary('cross entropy', cross_entropy)
with tf.name_scope('train'):
    train_step = tf.train.GradientDescentOptimizer(0.01).minimize(cross_entropy)

with tf.name_scope('test'):
    correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
    _ = tf.scalar_summary('accuracy', accuracy)

# Merge all the summaries and write them out to /tmp/mnist_logs
merged = tf.merge_all_summaries()
writer = tf.train.SummaryWriter(logpath, sess.graph)

sess.run(tf.initialize_all_variables())

# 最大checkpoint文件数为5
saver = tf.train.Saver(max_to_keep=5)

# 实例化图像处理类
dc = dealcode()


# 数据提取函数
def _get_data_(num, pic_dict=path):
    # 初始化样本数据
    imgdata = []
    labeldata = []
    # 检验样本数
    checkcount = 50
    nowcount = 0

    # 自定义异常用于跳出循环
    class Getoutofloop(Exception):
        pass

    try:
        while True:
            for root, dirs, files in os.walk(pic_dict):
                for dir in dirs:
                    for img in os.walk(os.path.join(root, dir)):
                        for imagename in img[2]:
                            if random.randint(0, 80) < 2:
                                image = cv2.imread(str(img[0]) + '/' + str(imagename), cv2.IMREAD_GRAYSCALE)
                                image = image.astype(np.float32)
                                image = np.multiply(image, 1.0 / 255.0)
                                imgdata.append(np.ravel(image))
                                tmplabel = img[0]
                                tmplabel = tmplabel[len(tmplabel) - 1]
                                labeldata.append(tmplabel)
                                nowcount += 1
                                if nowcount == checkcount:
                                    raise Getoutofloop()
                            else:
                                continue
    except Getoutofloop:
        pass
    imgdata = np.array(imgdata)
    labeldata = dc._one_hot_(np.array(labeldata))
    return imgdata, labeldata


# TensorFlow预测函数
def _tensorflow_predict_(feed_dict=None):
    if not feed_dict:
        print '没有输入数据集'
    else:
        predict = []
        results_sets = sess.run([y], feed_dict=feed_dict)
        results_y = results_sets[0]
        for i in results_y:
            loc = np.array([i])
            loc = np.where(loc == np.max(loc))
            loc = int(loc[1])
            if loc < 10:
                loc = loc + 48
            else:
                loc = loc + 65 - 10
            predict.append(chr(loc))
    return predict  # 训练事先处理好的样本


nextstep = raw_input('是否写入日志？(y/n):')
if nextstep == 'y':
    nextstep = raw_input('训练次数：')
    trainnum = int(nextstep)
    nextstep = raw_input('每次训练样本数：')
    count = int(nextstep)
    for i in range(trainnum):
        imgdata, labeldata = _get_data_(count)
        feed = {x: imgdata, y_: labeldata}
        sess.run(train_step, feed_dict=feed)
        imgdata, labeldata = _get_data_(100, pic_dict=testpath)
        feed = {x: imgdata, y_: labeldata}
        checkresult = sess.run([merged, accuracy], feed_dict=feed)
        summary_str = checkresult[0]
        acc = checkresult[1]
        writer.add_summary(summary_str, i)
        print '已训练%s个样本,准确率%s' % (count * (i + 1), acc)
else:
    nextstep = raw_input('训练次数：')
    trainnum = int(nextstep)
    nextstep = raw_input('每次训练样本数：')
    count = int(nextstep)
    for i in range(trainnum):
        imgdata, labeldata = _get_data_(count)
        feed = {x: imgdata, y_: labeldata}
        sess.run(train_step, feed_dict=feed)
    print '已训练%s个样本' % (count * trainnum)

stop = False
step = count * trainnum
# 还原模型
# saver.restore(sess, protopath + 'model.ckpt-' + str(step - 1))

while not stop:
    nextstep = raw_input('自定义检测？(y/n):')
    if nextstep == 'y':
        if dc._generate_image_():
            img, results = dc._deal_image_()
        # 根据显示图片，输入验证码字符
        while True:
            labelinput = raw_input('输入：\n')
            check = re.search('[0-9a-zA-Z]{4}', labelinput)
            if check is not None:
                print '输入验证码成功'
                labelinput = list(labelinput)
                break
            else:
                print '输入错误'
        labeldata = dc._one_hot_(np.array(labelinput))
        # 获取验证码数据集(4个图片)
        imgdata = dc._get_image_(results)
        feed = {x: imgdata, y_: labeldata}
        print '计算机预测结果：', ''.join(_tensorflow_predict_(feed_dict={x: imgdata}))
        print '训练%s后，识别准确率为%s' % (step, accuracy.eval(feed))
    else:
        nextstep = raw_input('检测数量：')
        num = int(nextstep)
        print '进行自动检测...'
        imgdata, labeldata = _get_data_(num, pic_dict=testpath)
        feed = {x: imgdata, y_: labeldata}
        # 检测模型
        print '检测%s样本后，计算识别准确率为%s' % (num, accuracy.eval(feed))

    nextstep = raw_input('退出保存？(y/n):')
    if nextstep == 'y':
        save_path = saver.save(sess, protopath + protoname, global_step=step)
        break
    else:
        continue

sess.close()
