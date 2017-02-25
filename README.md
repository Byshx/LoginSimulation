# LoginSimulation
a python script for loginning Yangtze University and grabing accounts whose password isn't change.
###利用此脚本可以模拟登陆长江大学教务处网站，亦可通过它来获取教务处数据库中使用初始密码的学生信息。
##系统环境和准备工具
1、使用Linux或Windows系统（需要自行更改脚本中的路径）
2、配置python2.7环境
3、下载安装opencv3.1.0
4、下载安装TensorFlow机器学习框架
5、下载安装科学计算模块Numpy
6、使用支持python的IDE（eclipse/pycharm）
7、下载安装MySQL数据库（其他数据库需要自行更改脚本中的代码以支持）
##使用说明
1、TestPicture和TrainPicture分别为下载并处理好的验证码图片
2、module中是已经训练好的模型
3、logs中存储最近训练的日志
4、CheckCode为主脚本程序。如果搜索完一届学生，换下一届时，请：
```Python
# 更改学生id的起点
Uid = 200904809
```
```Python
# 起点更改后，终点也要更改。
if Uid > 200909999:
    print '搜索完毕 →_→'
    break
```
```Python
# 同时别忘了更改数据库的表，表要在数据库中先创建（如果你想储存在上一张表中，就忽略此步骤）
sql = 'INSERT INTO Student_2009 VALUES(%s,%s,%s,%s)'
```
5、identity_code为TensorFlow训练模型脚本
6、deal_code为验证码图片处理脚本
7、input_data为验证码数据标注脚本

##→请使用校园网以外的IP进行搜索。╮(╯▽╰)╭
##→如有问题，请发issue，不定期维护
##→右上角点Star
