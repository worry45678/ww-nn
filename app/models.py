from . import db
from sqlalchemy import or_, and_
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, AnonymousUserMixin
from . import login_manger
from datetime import datetime
import math

class tblUser(UserMixin, db.Model):
    __tablename__ = "tblUser"

    id = db.Column('ID', db.Integer, primary_key=True, autoincrement=True)
    name = db.Column('Name', db.String(8))
    password_hash = db.Column('password', db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.ID'))
    money = db.Column('money', db.Integer)
    photo = db.Column('photo', db.String(128))
    openid = db.Column('openid', db.String(20))
    room1s = db.relationship('Room', backref='user1', lazy='dynamic', primaryjoin='(tblUser.id==Room.user1_id)')
    room2s = db.relationship('Room', backref='user2', lazy='dynamic', primaryjoin='(tblUser.id==Room.user2_id)')
    room3s = db.relationship('Room', backref='user3', lazy='dynamic', primaryjoin='(tblUser.id==Room.user3_id)')
    room4s = db.relationship('Room', backref='user4', lazy='dynamic', primaryjoin='(tblUser.id==Room.user4_id)')
    room5s = db.relationship('Room', backref='user5', lazy='dynamic', primaryjoin='(tblUser.id==Room.user5_id)')

    def __init__(self, **kwargs):
        super(tblUser, self).__init__(**kwargs)
        if self.role_id is None: # 如果名称为admin，则设为管理员
            if self.name == 'admin':
                self.role_id = tblRole.query.filter_by(permissions=0xff).first().id
            if self.role_id is None:
                self.role_id = tblRole.query.filter_by(default=True).first().id
    def __repr__(self):
        return '''{"id":"%d","name":"%s"}''' %(self.id,self.name)
    
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

    def rooms(self):
        return self.room1s.all() + self.room2s.all() + self.room3s.all() + self.room4s.all() +self.room5s.all()


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
    paijus = db.relationship('Paiju', backref='roomname', lazy='dynamic')

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
    
    def __repr__(self):
        user1 = self.user1.name if self.user1 else None
        user2 = self.user2.name if self.user2 else None
        user3 = self.user3.name if self.user3 else None
        user4 = self.user4.name if self.user4 else None
        user5 = self.user5.name if self.user5 else None
        return '''{"id": "%s","createtime":"%s","confirm":"%s","user1":"%s","user2":"%s","user3":"%s","user4":"%s","user5":"%s","end":"%s"}''' \
               %(self.id,self.createtime,self.confirm, user1, user2, user3, user4, user5, self.end) 

    def status(self):
        user1 = self.user1.name if self.user1 else None
        user2 = self.user2.name if self.user2 else None
        user3 = self.user3.name if self.user3 else None
        user4 = self.user4.name if self.user4 else None
        user5 = self.user5.name if self.user5 else None
        if self.paijus.filter_by(finish=0).first():
            running_paiju = self.paijus.filter_by(finish=0).first()
            if running_paiju.ready == 2**self.count()-1:
                zhuang = math.log(running_paiju.zhuang)/math.log(2)
            else :
                zhuang = -1 # 没有准备好，返回-1
        else:
            zhuang = -2 # 没有牌局，返回-2

        return '''{"id": %d,"createtime":"%s","confirm":%d,"users":["%s","%s","%s","%s","%s"],"end":"%s","count":%d,"zhuang":%d}''' \
                %(self.id,self.createtime,self.confirm, user1, user2, user3, user4, user5, self.end, self.count(), zhuang) 

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
    
    def marks(self):
        return '''{"id":%d,"marks":["%d","%d","%d","%d","%d"]}'''\
                %(self.id, self.user1_mark, self.user2_mark, self.user3_mark, self.user4_mark, self.user5_mark)

login_manger.anonymous_user = AnonymousUser


@login_manger.user_loader
def load_user(user_id):
    """
    加载用户，存在则返回用户对象，不存在则返回None。
    """
    return tblUser.query.get(int(user_id))