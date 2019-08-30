"""
只处理与主题相关的路由和视图
"""
from peewee import MySQLDatabase, Model, CharField, BooleanField, IntegerField
from flask import render_template, redirect, request, url_for, flash
from flask import Flask,session
from flask_login import login_user, logout_user, login_required
from sqlalchemy import func
from .forms import LoginForm
from ..models import User_admin as User
from . import main

from .. import db
from ..models import *
import datetime


import random
import os

app = Flask(__name__)


@main.route('/admin', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
    # if True:
    #     try:
            username = form.username.data
            password = form.password.data
            User_admin = User.query.filter_by(username=username).first()
            if User_admin.verify_password(password):
                session['id'] = User_admin.id
                session['password'] = User_admin.password
                client_num = db.session.query(func.count(Users.id)).all()[0][0]
                material_num = db.session.query(func.count(Files.id)).all()[0][0]
                return render_template('admin/index.html',user=User_admin,client_num=client_num,material_num=material_num)
            else:

                flash('用户名或密码错误')
        # except:
        #     flash('用户名或密码错误')
    return render_template('admin/login.html', form=form)

@main.route('/admin/usercle',methods=['GET', 'POST'])
def user():
    if not db.session.query(id=session['id']).filter():
        form = LoginForm()
        return render_template('admin/login.html', form=form)
    if request.method == 'GET':
        pass


# 通用列表查询
def common_list(DynamicModel, view):
    # 接收参数
    action = request.args.get('action')
    id = request.args.get('id')
    page = int(request.args.get('page')) if request.args.get('page') else 1
    length = int(request.args.get('length')) if request.args.get('length') else cfg.ITEMS_PER_PAGE

    # 删除操作
    if action == 'del' and id:
        try:
            DynamicModel.get(DynamicModel.id == id).delete_instance()
            flash('删除成功')
        except:
            flash('删除失败')

    # 查询列表
    query = DynamicModel.select()
    total_count = query.count()

    # 处理分页
    if page: query = query.paginate(page, length)

    dict = {'content': utils.query_to_list(query), 'total_count': total_count,
            'total_page': math.ceil(total_count / length), 'page': page, 'length': length}
    return render_template(view, form=dict, current_user=current_user)


# 通用单模型查询&新增&修改
def common_edit(DynamicModel, form, view):
    id = request.args.get('id', '')
    if id:
        # 查询
        model = DynamicModel.get(DynamicModel.id == id)
        if request.method == 'GET':
            utils.model_to_form(model, form)
        # 修改
        if request.method == 'POST':
            if form.validate_on_submit():
                utils.form_to_model(form, model)
                model.save()
                flash('修改成功')
            else:
                utils.flash_errors(form)
    else:
        # 新增
        if form.validate_on_submit():
            model = DynamicModel()
            utils.form_to_model(form, model)
            model.save()
            flash('保存成功')
        else:
            utils.flash_errors(form)
    return render_template(view, form=form, current_user=current_user)


# 根目录跳转
# @main.route('/admin', methods=['GET'])
# @login_required
# def root():
#     return redirect(url_for('main.admin/index'))


# 首页
@main.route('/admin/index', methods=['GET'])
@login_required
def index(user):
    return render_template('admin/index.html', user=user)


# 通知方式查询
@main.route('/admin/notifylist', methods=['GET', 'POST'])
@login_required
def notifylist():
    return common_list(CfgNotify, 'admin/notifylist.html')


# 通知方式配置
@main.route('/admin/notifyedit', methods=['GET', 'POST'])
@login_required
def notifyedit():
    return common_edit(CfgNotify, CfgNotifyForm(), 'admin/notifyedit.html')


# 验证登录界面账户是否存在
def checkuname_views(request):
    '''
    session接收请求的函数,验证数据是否存在
    :return:
    '''
    # 1.接收参数
    uname = request.GET.get('uname', default='')
    # print('打印uname', uname)
    # 2.验证数据是否存在
    price = DB.lookinfo(uname)
    # print("回调返回:", price)
    # 3.根据结果给出返回值
    if price:
        # print('返回1')
        jsonStr = {'price': 1}
        # 表示用户名称已存在
    else:
        # print('返回0')
        jsonStr = {'price': 0}
        # 表示用户名称不存在
    return HttpResponse(json.dumps(jsonStr), content_type="application/json")


@app.route('/',methods=['GET','POST'])
def index_views(request):
    # 获取ip来源
    if 'HTTP_X_FORWARDED_FOR' in request.META:
        ips = request.META['HTTP_X_FORWARDED_FOR'] + str(random.random())
    else:
        ips = request.META['REMOTE_ADDR']+ str(random.random())
    ips=ips.replace('.','')
    # print(ips)
    if 'sname' in request.session:
        # 获取sename值
        print("获取session值")
        sname = request.session['sname']
        id = request.session['id']
        users = DB.session_judge(sname, id)
        if users:
            # print('打印ｌｏｃａｌｓ：', locals())
            return render_template(request, 'interface.html', locals())  # 从哪来,回哪去
        else:
            # session&cookie 密码错误
            # print("session&cookie 密码错误")
            del request.session['sname']
            del request.session['id']
            return render(request, 'login.html')  # 返回登录页面
    else:
        # 没有session, 判断cookie
        # print("获取cookie")
        if 'cname' in request.COOKIES and 'cpwd' in request.COOKIES:
            # 取值cookie
            # print("取值cookie")
            cname = request.COOKIES['cname']
            cpwd = request.COOKIES['cpwd']
            users = DB.lookinfo(cname, cpwd)
            if users:
                # cookie密码正确,保存进session
                # cname, id = DB.id_look(cname)
                request.session['sname'] = cname
                request.session['id'] = users.id
                # users = DB.lookinfo(cname)
                # print('打印用户信息', users)
                # print('打印ｌｏｃａｌｓ：', locals())
                return render(request, 'interface.html', locals())
            else:
                # cookie 密码错误

                resp = render(request, 'login.html')
                resp.delete_cookie('cname')
                resp.delete_cookie('cwd')
                return resp  # 返回登录页面
        else:
            # print("什么都没有,准备登录"
            print(locals())
            return render(request, 'login.html',locals())  # 返回登录页面


# 用户登录
def login(request):
    # print('用户登录')
    if request.method == 'GET':
        url = request.META.get('HTTP_REFERER', '/')
        if 'sname' in request.session:
            # 获取sename值
            # print("获取session值")
            sname = request.session['sname']
            id = request.session['id']
            vcode = request.session['vcode']
            # 调用数据库查找用户是否是否存在
            # if vcode
            users = DB.session_judge(sname, id)
            if users:
                # print('通过session登录')
                return render(request, 'interface.html', locals())
            else:
                # print("session 密码错误")
                del request.session['sname']
                del request.session['id']
        # print('session错误')
        if 'HTTP_X_FORWARDED_FOR' in request.META:
            ips = request.META['HTTP_X_FORWARDED_FOR'] + str(random.random())
        else:
            ips = request.META['REMOTE_ADDR'] + str(random.random())
        ips = ips.replace('.', '')
        return render(request, 'login.html',locals())  # 返回登录页面
    else:
        # post上传的数
        # print('接收到数据')
        # 判断用户密码是否正确
        username = request.POST['loginname']  # 接收用户名
        password = request.POST['loginpwd']  # 接收密码
        value=request.POST['vcode']
        print('获取输入的验证码值:',type(value),value)
        ips = request.POST['ips']
        if value!=str(request.session[ips]):
            if 'HTTP_X_FORWARDED_FOR' in request.META:
                ips = request.META['HTTP_X_FORWARDED_FOR'] + str(random.random())
            else:
                ips = request.META['REMOTE_ADDR'] + str(random.random())
            ips = ips.replace('.', '')
            pop = '验证码错误'
            return render(request, 'login.html', locals())
        users = DB.lookinfo(username, password)
        # print('打印users', users)
        if users:
            # 正确
            # print('用户名称%s,用户密码%s' % (username, password))
            request.session['sname'] = username
            request.session['id'] = users.id
            # 添加cookie
            resp = render(request, 'interface.html', locals())
            # print('用户名称%s == 用户密码%s' % (username, password))
            resp.set_cookie('cname', username, 60 * 60 * 24)
            resp.set_cookie('cpwd', password, 60 * 60 * 24)
            # print(resp)
            # print("接收到账号密码登录")
            # print(users)
            return resp
        else:
            # 密码错误
            # print('密码错误,返回登录界面')
            pop = '用户名或密码错误'
            # print('打印locals',locals())
            if 'HTTP_X_FORWARDED_FOR' in request.META:
                ips = request.META['HTTP_X_FORWARDED_FOR'] + str(random.random())
            else:
                ips = request.META['REMOTE_ADDR'] + str(random.random())
            ips = ips.replace('.', '')
            return render(request, 'login.html', locals())


# 用户注册

def register(request):
    if request.method == "GET":
        return render_template()
    else:
        name = request.POST.get('uname')
        # print('打印昵称', name)
        upwd = request.POST.get('upwd')
        phone = request.POST.get('phone')
        # 添加注册个人信息,返回个人信息
        # print(name, upwd, phone)
        users = DB.request_users(name, upwd, phone)
        # 添加 session
        request.session['sname'] = users.name
        request.session['id'] = users.id
        # 添加cookie
        # print('打印locals', locals())
        resp = render(request, 'interface.html', locals())
        # print('用户名称%s == 用户密码%s' % (users.name, users.upwd))
        resp.set_cookie('cname', users.name, 60 * 60 * 24)
        resp.set_cookie('cpwd', users.upwd, 60 * 60 * 24)
        return resp



@app.route('/admin')
def hello_world(request):
    return render_template(request,'/admin')


if __name__ == '__main__':
    app.run(
        debug=True,
        host='0.0.0.0',
        port='5001'
    )


@main.route("/")
def index_views():
    # 查询Topic中前15条数据并发送到index.html做显示
    topics = Topic.query.limit(15).all()
    # 读取Category中的所有内容并发送到index.html显示
    categories = Category.query.all()
    # 判断是否有登录的用户(判断session中是否有id和loginname)
    if 'id' in session and 'loginname' in session:
        id = session['id']
        user = User.query.filter_by(ID=id).first()
    return render_template("index.html",params = locals())

@main.route("/release",methods=['GET','POST'])
def release_views():
    if request.method == 'GET':

        # 判断session,判断是否有登录用户
        if 'id' in session and 'loginname' in session:
            # 将id从session中获取出来再查询用户
            id = session['id']
            user = User.query.filter_by(ID=id).first()
            if user.is_author:
                # 1.查询Category的所有的信息
                categories = Category.query.all()
                # 2.查询BlogType的所有的信息
                blogTypes = BlogType.query.all();
                return render_template("release.html",params=locals())
        return redirect('/')
    else:
        # 创建Topic的对象
        topic = Topic()
        # 获取标题(author)为Topic.title赋值
        topic.title = request.form['author']
        # 获取文章类型(list)为Topic.blogtype_id赋值
        topic.blogtype_id = request.form['list']
        # 获取内容类型(category)为Topic.category_id赋值
        topic.category_id = request.form['category']
        # 获取内容(content)为Topic.content赋值
        topic.content = request.form['content']
        # 从session中获取id为Topic.user_id赋值
        topic.user_id = session['id']
        # 获取系统时间为Topic.pub_date赋值
        topic.pub_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # 判断是否有上传图片,处理上传图片,为Topic.images赋值
        if request.files:
            # 获取上传的文件
            f = request.files['picture']
            # 处理文件名:时间.扩展名
            ftime=datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
            ext = f.filename.split('.')[-1]
            filename=ftime+'.'+ext
            # 将文件名赋值给topic.images
            topic.images = "upload/"+filename
            # 处理上传路径: static/upload
            basedir = os.path.dirname(os.path.dirname(__file__))
            upload_path = os.path.join(basedir,'static/upload',filename)
            # 上传文件
            f.save(upload_path)
        # 将Topic的对象保存进数据库
        db.session.add(topic)
        return redirect('/')










