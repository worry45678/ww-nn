from flask import Blueprint

auth = Blueprint('auth', __name__)  # 参数说明 蓝本名字， 蓝本所在的包或模块

from . import views # 写在后面，避免循环引用
