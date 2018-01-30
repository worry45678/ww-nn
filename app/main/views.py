import json
from flask import render_template, session, redirect, url_for, request, send_from_directory, jsonify, flash
from flask_login import current_user, login_required
from . import main, PUKE
from datetime import datetime, timedelta
from .. import db
from ..models import tblUser, Permission, Room, Paiju
from ..decorators import admin_required, permission_required
import itertools, random, json

def createid():
    id = random.randint(0,1000000)
    if Room.query.filter_by(id=id).first() is not None:
        createid()
    else:
        return id

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

@main.route('/room')
def room():
    return render_template('room.html')

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
    room = Room(id=createid(), user1_id=current_user.id)
    db.session.add(room)
    db.session.commit()
    session['room_id'] = room.id
    return 'createroom'

@main.route('/joinroom', methods=['GET', 'POST'])
@login_required
def joinroom():
    if request.method == 'GET':
        if Room.query.filter_by(id=request.args.get('id')).first():
            room = Room.query.filter_by(id=request.args.get('id')).first()
            if room.userpos(current_user) == 0:
                if room.user2_id is None:
                    room.user2_id = current_user.id
                    db.session.add(room)
                    db.session.commit()
                    session['room_id'] = room.id
                    return 'join 2#'
                elif room.user3_id is None:
                    room.user3_id = current_user.id
                    db.session.add(room)
                    db.session.commit()
                    session['room_id'] = room.id
                    return 'join 3#'
                elif room.user4_id is None:
                    room.user4_id = current_user.id
                    db.session.add(room)
                    db.session.commit()
                    session['room_id'] = room.id
                    return 'join 4#'
                elif room.user5_id is None:
                    room.user5_id = current_user.id
                    db.session.add(room)
                    db.session.commit()
                    session['room_id'] = room.id
                    return 'join 5#'
            else:
                session['room_id'] = room.id
                return jsonify(room.userpos(current_user))
        else: 'no room'
    return 'joinroom'

@main.route('/confirmroom')
@login_required
def confirmroom():
    if Room.query.filter_by(id=session['room_id']).first():
        room = Room.query.filter_by(id=session['room_id']).first()
        room.confirm = room.confirm | room.userpos(current_user)
        db.session.add(room)
        db.session.commit()
    return 'confirmroom'

@main.route('/start')
@login_required
def start():
    if Room.query.filter_by(id=session['room_id']).first():
        room = Room.query.filter_by(id=session['room_id']).first()
        if room.confirm == 2**(room.count())-1:
            new_puke = PUKE.copy()
            for i in range(20):
                random.shuffle(new_puke)
                new_paiju = Paiju(room_id=room.id, paixu=json.dumps(new_puke))
                db.session.add(new_paiju)
                db.session.commit()
            return jsonify(new_puke)
        else:
            return 'somebody not ready'
    return 'start'

@main.route('/play')
@login_required
def play():
    import math
    paixu = json.loads(Paiju.query.filter_by(room_id=session['room_id']).filter_by(done=0).first().paixu)
    room = Room.query.filter_by(id=session['room_id']).first()
    pos = int(math.log(room.userpos(current_user))/math.log(2) + 1)
    print(pos*5-5,pos*5)
    print(paixu[5:10])
    return jsonify(paixu[pos*5-5:pos*5],pos)