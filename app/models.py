from . import db
from sqlalchemy import or_, and_
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, AnonymousUserMixin
from . import login_manger
from datetime import datetime

class tblUser(UserMixin, db.Model):
    __tablename__ = "tblUser"

    id = db.Column('ID', db.Integer, primary_key=True, autoincrement=True)
    name = db.Column('Name', db.String(8))
    password_hash = db.Column('password', db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.ID'))
    money = db.Column('money', db.Integer)
    photo = db.Column('photo', db.String(128))
    openid = db.Column('openid', db.String(20))

    def __init__(self, **kwargs):
        super(tblUser, self).__init__(**kwargs)
        if self.role_id is None: # 如果名称为admin，则设为管理员
            if self.name == 'admin':
                self.role_id = tblRole.query.filter_by(permissions=0xff).first().id
            if self.role_id is None:
                self.role_id = tblRole.query.filter_by(default=True).first().id
    
    def can(self, permissions): # 判断角色是否包含所有请求权限，包含则返回True
        return self.role_id is not None and (self.rolename.permissions & permissions) == permissions
    
    def is_administrator(self):
        return self.can(Permission.ADMINISTER)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def verify_password(self, password):
        return  check_password_hash(self.password_hash, password)


class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False
    
    def is_administrator(self):
        return False

class tblRole(db.Model):
    __tablename__ = 'roles'

    id = db.Column('ID', db.Integer, primary_key=True, autoincrement=True)
    name = db.Column('Name', db.String(16))
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column('Permission', db.Integer)
    users = db.relationship('tblUser', backref='rolename', lazy='dynamic')

    @staticmethod
    def insert_roles():
        roles = {
            'User': (Permission.FOLLOW | Permission.COMMENT | Permission.WRITE_ARTICLES, True),
            'Moderator': (Permission.FOLLOW | Permission.COMMENT | Permission.WRITE_ARTICLES | Permission.MODERATE_COMMENTS,False),
            'Administrator':(0xff, False)
        }
        for r in roles:
            role = tblRole.query.filter_by(name=r).first()
            if role is None:
                role = tblRole(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()


class Permission:
    FOLLOW = 0x01
    COMMENT = 0x02
    WRITE_ARTICLES = 0x04
    MODERATE_COMMENTS = 0x08
    ADMINISTER = 0x80

class Room(db.Model):
    __tablename__ = 'room'
    id = db.Column('ID', db.Integer, primary_key=True, autoincrement=True)
    createtime = db.Column(db.DateTime(), default=datetime.utcnow)
    confirm = db.Column('confirm', db.Integer, default=0)
    user1_id = db.Column(db.Integer, db.ForeignKey('tblUser.ID'))
    user2_id = db.Column(db.Integer, db.ForeignKey('tblUser.ID'))
    user3_id = db.Column(db.Integer, db.ForeignKey('tblUser.ID'))
    user4_id = db.Column(db.Integer, db.ForeignKey('tblUser.ID'))
    user5_id = db.Column(db.Integer, db.ForeignKey('tblUser.ID'))
    end = db.Column('end', db.Boolean, default=False)
    paujus = db.relationship('Paiju', backref='roomname', lazy='dynamic')

    def userpos(self, user):
        if self.user1_id == user.id:
            return 1
        elif user.id == self.user2_id:
            return 2
        elif user.id == self.user3_id:
            return 4
        elif user.id == self.user4_id:
            return 8
        elif user.id == self.user5_id:
            return 16
        else:
            return 0

    def count(self):
        if self.user2_id is None:
            return 1
        elif self.user3_id is None:
            return 2
        elif self.user4_id is None:
            return 3
        elif self.user5_id is None:
            return 4
        else:
            return 5



class Paiju(db.Model):
    __table__name = 'paiju'
    id = db.Column('ID', db.Integer, primary_key=True, autoincrement=True)
    room_id = db.Column(db.Integer, db.ForeignKey('room.ID'))
    paixu = db.Column('paixu', db.String(700))
    createtime = db.Column(db.DateTime(), default=datetime.utcnow)
    ready = db.Column('ready', db.Integer, default=0)
    zhuang = db.Column('zhuang', db.Integer, default=0)
    done = db.Column('done', db.Integer, default=0)
    finish = db.Column('finish', db.Boolean, default=False)
    user1_xiazhu = db.Column(db.Integer, default=0)
    user2_xiazhu = db.Column(db.Integer, default=0)
    user3_xiazhu = db.Column(db.Integer, default=0)
    user4_xiazhu = db.Column(db.Integer, default=0)
    user5_xiazhu = db.Column(db.Integer, default=0)
    xiazhudone = db.Column('xiazhudone', db.Integer, default=0)
    user1_mark = db.Column(db.Integer, default=0)
    user2_mark = db.Column(db.Integer, default=0)
    user3_mark = db.Column(db.Integer, default=0)
    user4_mark = db.Column(db.Integer, default=0)
    user5_mark = db.Column(db.Integer, default=0)
    

login_manger.anonymous_user = AnonymousUser


@login_manger.user_loader
def load_user(user_id):
    """
    加载用户，存在则返回用户对象，不存在则返回None。
    """
    return tblUser.query.get(int(user_id))