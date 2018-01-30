import json
from flask import render_template, session, redirect, url_for, request, send_from_directory, jsonify, flash
from flask_login import current_user, login_required
from . import main, PUKE
from datetime import datetime, timedelta
from .. import db
from ..models import tblUser, Permission, Room, Paiju
from ..decorators import admin_required, permission_required
import itertools, random, json


@main.route('/admin')
@login_required
@admin_required
def for_admins_only():
    """
    admin管理员页面
    """
    return "For Administrator!"


@main.route('/moderator')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def for_moderators_only():
    return "For comment moderators!"


@main.route('/test')
def test():
    return render_template('test.html')

@main.route('/fapai')
def fapai():
    new_puke = PUKE.copy()
    paixu=[]
    for i in range(20):
        paixu = paixu + [random.choice(new_puke)]
        new_puke.remove(paixu[-1])
    return jsonify(paixu)

@main.route('/createroom')
@login_required
def createroom():
    room = Room(id=random.randint(0,1000000), user1_id=current_user.id)
    db.session.add(room)
    db.session.commit()
    return 'createromm'

@main.route('/joinroom', methods=['GET', 'POST'])
@login_required
def joinroom():
    if request.methods == 'POST':
        if Room.query.filter_by(id=request.form.get('id')).last():
            room = Room.fiter_by(id=request.form.get('id')).last()
            r
    return 'joinroom'