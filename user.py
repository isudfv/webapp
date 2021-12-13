from flask_login import UserMixin, login_manager
import psycopg2.extras
import hashlib
from postgres import *

conn = psycopg2.connect("dbname=shop port=32532 host=159.75.122.61 user=postgres password=FSDfSdcsdfs2134AD")

salt = b'abcdef01'

cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)


class User(UserMixin):
    def __init__(self, username):
        user = getUserDict(username)
        self.name, self.passwd = user['name'], user['passwd']

    @staticmethod
    def get(username):
        return User(username)

    def get_id(self):
        return self.name


# def hashedPwd(password):
#     hasher = hashlib.sha256(salt)
#     hasher.update(password.encode('utf-8'))
#     return hasher.hexdigest()


def findUser(username):
    cursor.execute(f"SELECT COUNT(1) FROM users WHERE name = '{username}'")
    return cursor.fetchall()[0][0]


def getUserDict(username):
    cursor.execute(f"select name, passwd from users where name = '{username}'")
    ans = cursor.fetchall()
    return dict(ans[0])


# def modifyUser(usr):
#     cursor.execute(
#         f"update users set username = '{usr['username']}', password = '{usr['password']}' where uid = {usr['uid']}")
#     conn.commit()


def addUser(username, password):
    # hasher.update(password.encode('utf-8'))

    # get smallest unused uid
    cursor.execute(f"insert into users values('{username}', '{password}')")

    conn.commit()
    # conn.close()

# def getUserInfoDict(uid):
#     cursor.execute(f'''select userinfo.*, users.username from userinfo, users
#                                 where users.uid = userinfo.uid and users.uid = {uid}''')
#
#     ans = cursor.fetchall()
#     if ans:
#         return dict(ans[0])
#     return {}


# def getUserInfoDict(uid=None, username=None):
#     if uid:
#         cursor.execute(f'''select userinfo.*, users.username from userinfo, users
#                                     where users.uid = {uid}''')  # foreign key
#     elif username:
#         cursor.execute(f'''select userinfo.*, users.username from userinfo, users
#                                     where userinfo.uid = (select users.uid from users where username = '{username}')''')
#     else:
#         raise TypeError("至少指定一个参数")
#     ans = cursor.fetchall()
#     if ans:
#         return dict(ans[0])
#     return {}


# def modifyUserInfo(uid, changes):
#     str = 'update userinfo set '
#     for key, value in changes.items():
#         print(key)
#         print(value)
#         str += f"{key} = '{value}', "
#     str = str.removesuffix(", ")
#     str += f" where uid = {uid}"
#     print(str)
#     cursor.execute(str)
#     conn.commit()
