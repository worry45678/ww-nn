import os
from pyecharts import Style
BASEDIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    """
    app配置类
    包含：SECRET_KEY;SQLALCHEMY_COMMIT_ON_TEARDOWN = True;SQLALCHEMY_TRACK_MODIFICATIONS = True;
    """
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        """
        初始化app配置
        """
        pass


class DefaultConfig(Config):
    """
    服务器配置
    """
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:water@localhost/rx?charset=utf8'


class DevelopmentConfig(Config):
    """
    办公室电脑开发者配置
    """
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'

class TestConfig(Config):
    """
    测试配置
    """
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'


config = {'develop': DevelopmentConfig, 'default': DefaultConfig, 'test': TestConfig}  # 配置名称
