from sqlobject import *
import time
import base64
from config import mysql
import json

sqlhub.processConnection = connectionForURI(mysql)


class GetMsg(SQLObject):
    class sqlmeta:
        table = 'py_msg'

    name = StringCol(length=30, notNone=True)
    msg = StringCol(length=600, notNone=True)
    date = StringCol(length=100, notNone=True)


class login(SQLObject):
    class sqlmeta:
        table = 'py_login'

    user = StringCol(length=30, notNone=True)
    password = StringCol(length=50, notNone=True)


# login.createTable()
# GetMsg.createTable()


def add(name, msg):
    # 添加一条数据
    # GetMsg.createTable()
    add = GetMsg(name=name, msg=msg, date=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    fid = open('./data.json', 'r')
    rid = json.loads(fid.read())
    fid.close()
    rid['id'] = str(int(rid['id']) + 1)
    print(json.dumps(rid))
    fid = open('./data.json', 'w')
    fid.write(json.dumps(rid))
    fid.close()


def get():
    # 获取id和数据库的值
    Smsg = {}
    fid = open('./data.json', 'r')
    rid = json.loads(fid.read())
    lid = int(rid['id'])
    fid.close()
    c = 1

    while c <= lid:
        try:
            getnew = GetMsg.get(c)
        except:
            pass
        else:
            Smsg[c] = getnew
        c += 1
    # 返回数据库的值
    return Smsg


def delet(id):
    # 删除值
    dele = GetMsg.get(id)
    dele.destroySelf()


def AddUser(username, password):
    fid = open('./data.json', 'r')
    rid = json.loads(fid.read())
    fid.close()
    rid['user'] = str(int(rid['user']) + 1)
    print(json.dumps(rid))
    fid = open('./data.json', 'w')
    fid.write(json.dumps(rid))
    fid.close()
    try:
        login.selectBy(user=username).user
    except:
        password64 = base64.b64encode(password.encode(encoding='utf-8'))
        adduser = login(user=username, password=password64.decode())
        return True
    else:
        return 'have same user'


def check(username, password):
    user = login.selectBy(user=username)
    try:
        getpass = user[0].password
    except:
        pass
    else:
        if getpass == base64.b64encode(password.encode()).decode():
            return True
        else:
            return False


def userad(adu):
    fid = open('./data.json', 'r')
    rid = json.loads(fid.read())
    fid.close()
    lid = rid['admin']
    send = False
    for admin in lid:
        if adu == admin:
            send = send ^ True
        else:
            send = send ^ False
    return send


def alluers():
    Smsg = {}
    fid = open('./data.json', 'r')
    rid = json.loads(fid.read())
    lid = rid['id']
    fid.close()
    c = 1

    while c <= lid:
        try:
            getnew = login.get(c)
        except:
            pass
        else:
            Smsg[c] = getnew
        c += 1
    # 返回数据库的值
    return Smsg


def delet_user(id):
    dele = login.get(id)
    dele.destroySelf()

