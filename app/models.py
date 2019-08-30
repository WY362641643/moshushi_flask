# 根据数据库编写所有的实体类

from werkzeug.security import check_password_hash
# 导入 db 到db.py
from . import db

import datetime

# 通过db创建实体类

# 管理员工号
class User_admin(db.Model):
    __tablename__ = 'user_admin'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(16),nullable=False)  # 用户名
    password = db.Column(db.String(128),nullable=False)  # 密码
    fullname = db.Column(db.String(32),nullable=False)  # 真实性名
    email = db.Column(db.String(32))  # 邮箱
    phone = db.Column(db.Integer)  # 电话
    info_time = db.Column(db.DateTime)  # 登陆时间
    author = db.Column(db.Integer,default=1)  # 权限等级

    def verify_password(self, raw_password):
        return check_password_hash(self.password, raw_password)


# 声明模型类,创建账户表
class Users(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Integer,nullable=False, unique=True)  # 账户/电话
    upwd = db.Column(db.String(16),nullable=False)           # 用户密码
    email = db.Column(db.String(16),nullable=True)   # 邮箱
    register = db.Column(db.DateTime, nullable=False) # 注册时间
    times = db.Column(db.DateTime,nullable=False,)  # 最近上线时间
    # 关联属性-IsActivate_code
    isActivates = db.relationship("IsActivate_code", backref="users", lazy="dynamic")
    # 关联属性- Expense
    expenses = db.relationship("Expense", backref="users", lazy="dynamic")

    def verify_password(self, raw_password):
        return check_password_hash(self.upwd, raw_password)


# 声明模型类,储存激活码/充值卡
class IsActivate_code(db.Model):
    __tablename__='isActivate_code'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(32),primary_key=True, unique=True,nullable=False) # 激活码
    price = db.Column(db.Float,nullable=False) # 价格
    setmeal = db.Column(db.String(128),nullable=False)   # 套餐名称
    isActivate = db.Column(db.Boolean,default=False) # 是否已激活
    # 一(User)对多(IsActivate_code)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    # 做与User_balance类之间的一对一的关联属性和反向引用关系属性
    user_balance = db.relationship("User_balance",backref="isActivate_codes",uselist=False)


# 声明模型类 储存用户(激活码)在各个网站的剩余积分
class User_balance(db.Model):
    __tablename__ = 'user_balance'
    id = db.Column(db.Integer, primary_key=True)
    nitu = db.Column(db.Integer,nullable=False,) #'昵图网'
    shetu = db.Column(db.Integer,nullable=False, ) # '摄图网'
    qiantu = db.Column(db.Integer,nullable=False, ) # e'千图网'
    baotu = db.Column(db.Integer,nullable=False, ) # '包图网'
    miyuansu = db.Column(db.Integer,nullable=False) # 觅元素
    fengyun = db.Column(db.Integer,nullable=False,) # me'风云办公
    huaban = db.Column(db.Integer,nullable=False, ) # e'花瓣网'
    qianku = db.Column(db.Integer,nullable=False, ) # e'千库网'
    liutu = db.Column(db.Integer,nullable=False, ) # '六图网'
    jiuling = db.Column(db.Integer,nullable=False,) # me'90设计
    wotu = db.Column(db.Integer,nullable=False, ) #'我图网'
    xiongmao = db.Column(db.Integer,nullable=False) # am='熊猫办')
    baidu = db.Column(db.Integer,nullable=False, ) # =百度文库'
    dangtu = db.Column(db.Integer,nullable=False, ) # e'当图网'
    data = db.Column(db.DateTime,default='1970-01-01 00:00:00',) # '到期时间'

    # 一(IsActivate_code)对一(User_balance)
    isActivate_code_id = db.Column(db.Integer, db.ForeignKey('isActivate_code.id'), unique=True)

    # 关联属性-User_info
    isActivate = db.relationship("User_info", backref="user_balances", lazy="dynamic")


# 声明模型类,用户(激活码)单个网站对应的信息
class User_info(db.Model):
    __tablename__ = 'user_info'
    id = db.Column(db.Integer, primary_key=True)
    wangzhanname = db.Column(db.String(16), nullable=False, ) # '网站名称'
    dengji = db.Column(db.SmallInteger, nullable=False,) # '等级'
    shangxian = db.Column(db.SmallInteger,)  # '上限'
    xiaxian = db.Column(db.SmallInteger, )  # 下限'
    daoqi = db.Column(db.DateTime, nullable=False,)  # '到期时间'
    zhuangtai = db.Column(db.Boolean,nullable=False,default=False)  # '状态'
    beizhu = db.Column(db.String(200) )  # '备注'

    # 一(User_balance)对多(User_info)
    user_id = db.Column(db.Integer, db.ForeignKey('user_balance.id'))


# 声明模型, 存储自定义的套餐
class Setmeals(db.Model):
    __tablename__ = 'setmeals'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False, ) # '套餐名称'
    VIP = db.Column(db.SmallInteger,nullable=False, ) # VIP等级')
    data = db.Column(db.SmallInteger,nullable=False, ) # '使用时间/天')
    nitu = db.Column(db.SmallInteger,nullable=False, ) # '昵图网')
    shetu = db.Column(db.SmallInteger,nullable=False,) #  '摄图网')
    qiantu = db.Column(db.SmallInteger,nullable=False) # , '千图网')
    baotu = db.Column(db.SmallInteger,nullable=False,) #  '包图网')
    miyuansu = db.Column(db.SmallInteger,nullable=False) # se, '觅元素')
    fengyun = db.Column(db.SmallInteger,nullable=False) # e, '风云办公')
    huaban = db.Column(db.SmallInteger,nullable=False) # , '花瓣网')
    qianku = db.Column(db.SmallInteger,nullable=False) # , '千库网')
    liutu = db.Column(db.SmallInteger,nullable=False,) #  '六图网')
    jiuling = db.Column(db.SmallInteger,nullable=False) # e, '90设计')
    wotu = db.Column(db.SmallInteger,nullable=False, ) # '我图网')
    xiongmao = db.Column(db.SmallInteger,nullable=False) # se, '熊猫办公')
    baidu = db.Column(db.SmallInteger,nullable=False,) #  '百度文库')
    dangtu = db.Column(db.SmallInteger,nullable=False) # , '当图网')

    # 关联属性-Setmeals_info
    setmeals_infos = db.relationship("Setmeals_info", backref="setmeals_infos", lazy="dynamic")


# 声明模型类,单个自定义套餐的各个网站的信息
class Setmeals_info(db.Model):
    __tablename__ = 'setmeals_info'
    id = db.Column(db.Integer, primary_key=True)
    wangzhanname = db.Column(db.String(16), nullable=False, )  # '网站名称'
    dengji = db.Column(db.SmallInteger, nullable=False, )  # '等级'
    shangxian = db.Column(db.SmallInteger, )  # '上限'
    xiaxian = db.Column(db.SmallInteger, )  # 下限'
    daoqi = db.Column(db.DateTime, nullable=False, )  # '到期时间'
    zhuangtai = db.Column(db.Boolean, nullable=False, default=False)  # '状态'
    beizhu = db.Column(db.String(128))  # '备注'

    # 一(Setmeals)对多(Setmeals_info)
    setmeals_id = db.Column(db.Integer, db.ForeignKey('setmeals.id'))


# 声明模型类,存储下载记录
class Expense(db.Model):
    __tablename__ = 'expense'
    id = db.Column(db.Integer, primary_key=True)
    wangzhanname = db.Column(db.String(16), nullable=False, ) # '网站名称
    title = db.Column(db.String(64), nullable=False, ) # '下载标题
    link = db.Column(db.String(128),nullable=False, ) # '下载链接
    deduct = db.Column(db.SmallInteger, nullable=False, ) # '扣除
    DT = db.Column(db.DateTime,nullable=False,)  # 记录时间

    # 一(User)对多(Expense)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


# 声明模型类,存储登陆网页的账号
class Website(db.Model):
    __tablename__ = 'website'
    id = db.Column(db.Integer, primary_key=True)
    website = db.Column(db.String(8), index=True, nullable=False, )  # '网站(简拼)')
    type = db.Column(db.String(8) )  # '类型')
    accout = db.Column(db.String(32), nullable=False)  # '账号'
    password = db.Column(db.String(32), nullable=False,)  # '密码'
    sum = db.Column(db.Integer,nullable=False)  # '剩余积分/次  余额


# 声明模型类,存储下载的文件
class Files(db.Model):
    __tablename__ = 'files'
    id = db.Column(db.Integer, primary_key=True)
    file_link =db.Column(db.String(32),nullable=False,unique=True,index=True)  # 文件链接, ha加密
    file_add = db.Column(db.String(32),nullable=False,unique=True)


# 验证session在会员中是否正确
def session_judge(uname, id):
    '''
    此函数用于验证session是否正确
    :param uname: 用户名
    :param id: 用户ID
    :return: False True
    '''
    # global option
    options = Users.objects.filter(name=uname, id=id)
    if options:
        for ch in options:
            option = ch
    else:
        option = None
    return option


# 根据电话查找会员
def phonelook(phone):
    option = Users.objects.filter(phone=phone)
    for o in option:
        option = o
    return option


# 添加会员
def request_users(name, upwd, email=None, isActivate=None):
    '''
    添加账户
    :param name:
    :param upwd:
    :param phone:
    :return: 返回个人信息
    '''
    users = Users.objects.create(
        name=name,
        upwd=upwd,
        email=email,
        register=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        isActivate=isActivate,
        times=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )

    return users


# 添加下载记录
def set_expense(users, wzname, title, link, deduct):
    '''

    :param user: 消费者个人信息
    :param phones: 消费者发送的电话列表
    :return:
    '''
    expense = Expense()
    expense.wangzhanname = wzname
    expense.user_id = users.id
    expense.title = title
    expense.link = link
    expense.DT = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    expense.save()


# 消费者查询消费记录
def get_expens(user):
    '''

    :param user: 消费者个人信息
    :return: 返回消费记录
    '''
    expense = Expense.objects.filter(user_id=user.id)
    # print('expense:', expense)
    return expense


# 获取前n条账户
def getaccout(lens):
    accout = []
    pwd = []
    # print('打印leng长度：',lens)
    obj_list = Website.objects.all()[:lens]
    print(obj_list)
    for obj in obj_list:
        accout.append(obj.accout)
        pwd.append(obj.password)
    return accout, pwd


# 刷新账户余额
def resetaccout(accout, sum):
    myphone = Website.objects.get(accout=accout)
    myphone.sum = sum
    myphone.save()
    # print(accout,'的信息刷新成功')


# 建表
def create_table():
    db.connect()
    db.create_tables([CfgNotify, User])


if __name__ == '__main__':
    create_table()
