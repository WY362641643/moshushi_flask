"""
与用户相关的路由和视图
"""
from . import users
from ..models import *
from flask import request, render_template, session, make_response, redirect


@users.route("/login",methods=['GET','POST'])
def login_views():
    if request.method == 'GET':
        resp = make_response(render_template('login.html'))
        # 获取请求源地址,将地址保存进cookies
        url = request.headers.get('Referer','/')
        resp.set_cookie('url',url)
        return resp
    else:
        # 1.接收提交过来的用户名和密码
        username = request.form['username']
        password = request.form['password']
        # 2.验证用户名和密码的有效性
        user = User.query.filter_by(loginname=username,upwd=password).first()
        # 3.给出响应
        if user:
            # 登录成功
            # 1.先将登录信息保存进session
            session['id'] = user.ID
            session['loginname'] = user.loginname
            # 2.从哪来回哪去(从cookie中获取请求源地址)
            url = request.cookies.get('url')
            return redirect(url)
        else:
            #登录失败
            return render_template('login.html')

@users.route("/register")
def register_views():
    return "欢迎来到注册页面"

@users.route("/logout")
def logout_views():
    # 获取请求源地址
    url = request.headers.get('Referer','/')
    # 判断session中是否有登录信息,如果有则删除
    if 'id' in session and 'loginname' in session:
        del session['id']
        del session['loginname']
    # 重定向到源地址
    return redirect(url)








