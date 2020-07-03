# web-msg
一个msg wall用python写成
请修改配置文件：
config.py
```python
#数据库ip
MysqlIp = '127.0.0.1'
#数据库端口
MysqlPort = '3306'
#用户名
MysqlUsername = 'root'
#密码
MysqlPassword = 'Hu20071010+'
#数据库名
Mysqldb = 'py'
#请勿修改下面部分
mysql = 'mysql://{}:{}@{}:{}/{}?use_unicode=1&charset=utf8'.format(MysqlUsername, MysqlPassword, MysqlIp, MysqlPort, Mysqldb)
```
依赖MySQL和Redis数据库
请自行安装
Redis数据库配置请修改app.py
```python
app.config['SESSION_REDIS'] = Redis(  # redis的服务器参数
    host='127.0.0.1',  # 服务器地址
    port=6379)
```
安装依赖软件包
```python
pip install Flask
pip install bootstrap-flask
pip install flask-wtf
pip install flask_session
pip install sqlobject
pip install mysql
pip install mysqlclient
```
推荐anaconda环境,基于anaconda开发
