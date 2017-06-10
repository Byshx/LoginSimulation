# LoginSimulation
a python script for loginning Yangtze University and grabing accounts whose password isn't change.<br>
#### 利用此脚本可以模拟登陆长江大学教务处网站，亦可通过它来获取教务处数据库中使用初始密码的学生信息。<br>
* 系统环境和准备工具<br>
1、使用`Linux`或`Windows`系统（需要自行更改脚本中的路径）<br>
2、配置`python2.7`环境<br>
3、下载安装`opencv3.1.0`<br>
4、下载安装`TensorFlow`机器学习框架<br>
5、下载安装科学计算模块`Numpy`<br>
6、使用支持python的IDE（`eclipse`/`pycharm`）<br>
7、下载安装`MySQL`数据库（其他数据库需要自行更改脚本中的代码以支持）<br>
* 使用说明<br>
1、`TestPicture`和`TrainPicture`分别为下载并处理好的验证码图片<br>
2、`module`中是已经训练好的模型<br>
3、`logs`中存储最近训练的日志<br>
4、`CheckCode`为主脚本程序。如果搜索完一届学生，换下一届时，请：<br>
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
5、`identity_code`为TensorFlow训练模型脚本<br>
6、`deal_code`为验证码图片处理脚本<br>
7、`input_data`为验证码数据标注脚本<br>

* →请使用校园网以外的IP进行搜索。╮(╯▽╰)╭<br>
* →如有问题，请发`issue`，不定期维护<br>
* →右上角点`Star`<br>

### 由于是用于交流学习，所以，，
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
### 任何因使用此脚本闹出的是非，我表示
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
![image](https://github.com/Byshx/ImageCache/raw/master/Image/emoji_1.jpg)

