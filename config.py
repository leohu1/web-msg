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
