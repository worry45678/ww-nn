from flask import Blueprint
from ..models import Permission

main = Blueprint('main', __name__)  # 参数说明 蓝本名字， 蓝本所在的包或模块

PUKE = ['fangp01', 'fangp02', 'fangp03', 'fangp04', 'fangp05', 'fangp06', 'fangp07', 'fangp08', 'fangp09', 'fangp10',
 'fangp11', 'fangp12', 'fangp13', 'hongt01', 'hongt02', 'hongt03', 'hongt04', 'hongt05', 'hongt06', 'hongt07', 'hongt08',
 'hongt09', 'hongt10', 'hongt11', 'hongt12', 'hongt13', 'heit01', 'heit02', 'heit03', 'heit04', 'heit05', 'heit06', 'heit07',
 'heit08', 'heit09', 'heit10', 'heit11', 'heit12', 'heit13', 'meih01', 'meih02', 'meih03', 'meih04', 'meih05', 'meih06',
 'meih07', 'meih08', 'meih09', 'meih10', 'meih11', 'meih12', 'meih13']

from . import views # 写在后面，避免循环引用

# 用于模板中调用Permission
@main.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)


