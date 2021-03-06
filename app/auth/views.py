from flask import render_template, redirect, request, url_for, flash,jsonify
from . import auth
from flask_login import login_user, logout_user, login_required, current_user #flask_login 中管理用户登陆的函数
from ..models import tblUser
from .. import db


@auth.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        user = tblUser.query.filter_by(name=request.form.get('username')).first()
        if user is not None and user.verify_password(request.form.get('password')):
            login_user(user)
            return jsonify(user.id)
        print(user)
    return render_template('login.html')

@auth.route('/loginmobile',methods=['GET','POST'])
def loginmobile():
    if request.method=='POST':
        user = tblUser.query.filter_by(name=request.form.get('username')).first()
        if user is not None and user.verify_password(request.form.get('password')):
            login_user(user)
            return jsonify(str(user))
        else:
            return 'error'
    return render_template('loginMobile.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.test'))
