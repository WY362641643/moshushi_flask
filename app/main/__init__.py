"""
main包为管理员包
包含与主题相关的所有的业务逻辑的处理(发表,查看,删除,修改)
通过蓝图(Blueprint)将自己与app关联到一起
"""
from flask import Blueprint
# 声明好蓝图之后,main就拥有着与app相同的角色
# 创建路由的话则可以使用@main.route('/xxx')
main = Blueprint("main",__name__)
from . import views