import json
import math
from flask import render_template, session, redirect, url_for, request, send_from_directory, jsonify, flash
from flask_login import current_user, login_required
from . import main, PUKE, HUASE_NUMBER, BEI_LV
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

def calcniuniu(pai):
    l2 = [int(i[-2:]) if int(i[-2:])<10 else 10 for i in pai]
    diansu = 0
    for i in itertools.combinations(l2,3):
        if sum(i)%10==0:
            diansu=(sum(l2)-sum(i))%10
            if diansu == 0:
                diansu = 10
    l3 = {int(i[-2:])+HUASE_NUMBER[i[0:-2]]:i for i in pai}
    return diansu,l3[max(l3.keys())],max(l3.keys())

def compare(pai1,pai2):
    """
    参数1，庄的牌，参数2，玩家的牌,庄小，返回+，庄大，返回-
    """
    if pai1[0]+pai1[2]/100 < pai2[0]+pai2[2]/100:
        return BEI_LV[pai2[0]]
    else:
        return -1 * BEI_LV[pai1[0]]

def calcmark(pai):
    paixu = json.loads(pai.paixu)
    if pai.zhuang == 1:
        zhuang = int(pai.user1_xiazhu)
        pai.user2_mark = int(pai.user2_xiazhu) * zhuang * compare(calcniuniu(paixu[0]),calcniuniu(paixu[1]))
        pai.user3_mark = int(pai.user3_xiazhu) * zhuang * compare(calcniuniu(paixu[0]),calcniuniu(paixu[2]))
        pai.user4_mark = int(pai.user4_xiazhu) * zhuang * compare(calcniuniu(paixu[0]),calcniuniu(paixu[3]))
        pai.user5_mark = int(pai.user5_xiazhu) * zhuang * compare(calcniuniu(paixu[0]),calcniuniu(paixu[4]))
        pai.user1_mark = -pai.user2_mark-pai.user3_mark-pai.user4_mark-pai.user5_mark
    elif pai.zhuang == 2:
        zhuang = int(pai.user2_xiazhu)
        pai.user1_mark = int(pai.user1_xiazhu) * zhuang * compare(calcniuniu(paixu[1]),calcniuniu(paixu[0]))
        pai.user3_mark = int(pai.user3_xiazhu) * zhuang * compare(calcniuniu(paixu[1]),calcniuniu(paixu[2]))
        pai.user4_mark = int(pai.user4_xiazhu) * zhuang * compare(calcniuniu(paixu[1]),calcniuniu(paixu[3]))
        pai.user5_mark = int(pai.user5_xiazhu) * zhuang * compare(calcniuniu(paixu[1]),calcniuniu(paixu[4]))
        pai.user2_mark = -pai.user1_mark-pai.user3_mark-pai.user4_mark-pai.user5_mark
    elif pai.zhuang == 4:
        zhuang = int(pai.user3_xiazhu)
        pai.user2_mark = int(pai.user2_xiazhu) * zhuang * compare(calcniuniu(paixu[2]),calcniuniu(paixu[1]))
        pai.user1_mark = int(pai.user1_xiazhu) * zhuang * compare(calcniuniu(paixu[2]),calcniuniu(paixu[0]))
        pai.user4_mark = int(pai.user4_xiazhu) * zhuang * compare(calcniuniu(paixu[2]),calcniuniu(paixu[3]))
        pai.user5_mark = int(pai.user5_xiazhu) * zhuang * compare(calcniuniu(paixu[2]),calcniuniu(paixu[4]))
        pai.user3_mark = -pai.user1_mark-pai.user2_mark-pai.user4_mark-pai.user5_mark
        print(type(pai.user2_mark),pai.user2_mark)
    elif pai.zhuang ==8:
        zhuang = int(pai.user4_xiazhu)
        pai.user2_mark = int(pai.user2_xiazhu) * zhuang * compare(calcniuniu(paixu[3]),calcniuniu(paixu[1]))
        pai.user3_mark = int(pai.user3_xiazhu) * zhuang * compare(calcniuniu(paixu[3]),calcniuniu(paixu[2]))
        pai.user1_mark = int(pai.user1_xiazhu) * zhuang * compare(calcniuniu(paixu[3]),calcniuniu(paixu[0]))
        pai.user5_mark = int(pai.user5_xiazhu) * zhuang * compare(calcniuniu(paixu[3]),calcniuniu(paixu[4]))
        pai.user4_mark = -pai.user1_mark-pai.user2_mark-pai.user3_mark-pai.user5_mark
    elif pai.zhuang == 16:
        zhuang = int(pai.user5_xiazhu)
        pai.user2_mark = int(pai.user2_xiazhu) * zhuang * compare(calcniuniu(paixu[4]),calcniuniu(paixu[1]))
        pai.user3_mark = int(pai.user3_xiazhu) * zhuang * compare(calcniuniu(paixu[4]),calcniuniu(paixu[2]))
        pai.user4_mark = int(pai.user4_xiazhu) * zhuang * compare(calcniuniu(paixu[4]),calcniuniu(paixu[3]))
        pai.user1_mark = int(pai.user1_xiazhu) * zhuang * compare(calcniuniu(paixu[4]),calcniuniu(paixu[0]))
        pai.user5_mark = -pai.user1_mark-pai.user2_mark-pai.user3_mark-pai.user4_mark
    return pai


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

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/phone')
def phone():
    return render_template('phone.html')

@main.route('/test')
def test():
    return render_template('test.html')

@main.route('/room')
def room():
    return render_template('room.html')

@main.route('/fapai')
def fapai():
    """
    test用，无用
    """
    new_puke = PUKE.copy()
    paixu=[]
    for i in range(20):
        paixu = paixu + [random.choice(new_puke)]
        new_puke.remove(paixu[-1])
    return jsonify(paixu)

@main.route('/createroom')
def createroom():
    room = Room(id=createid(), user1_id=current_user.id)
    db.session.add(room)
    db.session.commit()
    session['room_id'] = room.id
    return jsonify(room.id)

@main.route('/joinroom', methods=['GET', 'POST'])
def joinroom():
    if request.method == 'GET':
        if Room.query.filter_by(id=request.args.get('roomid')).first():
            room = Room.query.filter_by(id=request.args.get('roomid')).first()
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
def confirmroom():
    if Room.query.filter_by(id=session['room_id']).first():
        room = Room.query.filter_by(id=session['room_id']).first()
        room.confirm = room.confirm | room.userpos(current_user)
        db.session.add(room)
        db.session.commit()
    return 'confirmroom'

@main.route('/start')
def start():
    """
    生成本房间的所有牌，开始游戏
    """
    if Room.query.filter_by(id=session['room_id']).first():
        room = Room.query.filter_by(id=session['room_id']).first()
        if room.confirm == 2**(room.count())-1:
            new_puke = PUKE.copy()
            for i in range(20):
                random.shuffle(new_puke)
                r = [new_puke[0:5],new_puke[5:10],new_puke[10:15],new_puke[15:20],new_puke[20:25]]
                new_paiju = Paiju(room_id=room.id, paixu=json.dumps(r))
                db.session.add(new_paiju)
                db.session.commit()
            return jsonify(r)
        else:
            return 'somebody not ready'
    return 'start'

@main.route('/play')
def play():
    """
    准备结束，各玩家获取牌组,待修改，只返回本玩家的前4张牌，亮牌时再全部返回
    """
    player = tblUser.query.filter_by(id=request.args.get('playerid')).first()
    room = Room.query.filter_by(id=session['room_id']).first()
    pai = Paiju.query.filter_by(room_id=session['room_id']).filter_by(finish=0).first()
    pai0 = Paiju.query.filter_by(room_id=session['room_id']).first()
    paixu = json.loads(pai.paixu)
    return jsonify(paixu,pai.id-pai0.id+1)

@main.route('/qiangzhuang')
def qiangzhuang():
    player = tblUser.query.filter_by(id=request.args.get('playerid')).first()
    room = Room.query.filter_by(id=session['room_id']).first()
    userpos = room.userpos(player)
    # pos = int(math.log(userpos)/math.log(2) + 1)
    pai = Paiju.query.filter_by(room_id=session['room_id']).filter_by(finish=0).first()
    pai.ready = pai.ready | userpos
    if pai.ready == 2**room.count()-1:#判断是否所有人都已抢庄，返回抢庄成功的
        y = [i for i in [pai.zhuang & int(2**(i)) for i in range(5)] if i>0]
        pai.zhuang = random.choice(y)
        db.session.add(pai)
        db.session.commit()
        return jsonify(pai.zhuang)
    elif request.args.get('qiangzhuang')=='1': #判断该玩家是否抢庄
        pai.zhuang = pai.zhuang | userpos
        db.session.add(pai)
        db.session.commit()
        return '%s qiangzhuang' %userpos
    db.session.add(pai)
    db.session.commit()
    return 'no qiangzhuang'

@main.route('/xiazhu')
def xiazhu():
    """
    下注，庄先确定倍数，前端获取到庄的倍数后，其他玩家才可以下注
    """
    player = tblUser.query.filter_by(id=request.args.get('playerid')).first()
    room = Room.query.filter_by(id=session['room_id']).first()
    userpos = room.userpos(player)
    pai = Paiju.query.filter_by(room_id=session['room_id']).filter_by(finish=0).first()
    pai.xiazhudone = pai.xiazhudone | userpos
    if userpos == 1:
        pai.user1_xiazhu = request.args.get('xiazhu')
    elif userpos == 2:
        pai.user2_xiazhu = request.args.get('xiazhu')
    elif userpos == 4:
        pai.user3_xiazhu = request.args.get('xiazhu')
    elif userpos == 8:
        pai.user4_xiazhu = request.args.get('xiazhu')
    elif userpos == 16:
        pai.user5_xiazhu = request.args.get('xiazhu')
    else:
        return '无该玩家'
    if pai.xiazhudone == 2**room.count()-1:#  下注结束，计算得分
        calcmark(pai)
    db.session.add(pai)
    db.session.commit()
    return '下注成功'

@main.route('/show')
def show():
    """
    各玩家亮牌，本局结束，算分，Paiju 中finish字段标记结束
    """
    player = tblUser.query.filter_by(id=request.args.get('playerid')).first()
    room = Room.query.filter_by(id=session['room_id']).first()
    pai = Paiju.query.filter_by(room_id=session['room_id']).filter_by(finish=0).first()
    pai.done= pai.done | room.userpos(player)
    if pai.done == 2**room.count()-1:
        pai.finish = True
    db.session.add(pai)
    db.session.commit()
    if room.userpos(player) == 1:
        return pai.marks()
    elif room.userpos(player) ==2:
        return pai.marks()
    elif room.userpos(player) == 4:
        return pai.marks()
    elif room.userpos(player) == 8:
        return pai.marks()
    elif room.userpos(player) == 16:
        return pai.marks()
    return '亮牌，本局结束'

@main.route('/status')
def status():
    """
    返回房间状态，接受roomid，userid为参数
    """
    player = tblUser.query.filter_by(id=request.args.get('playerid')).first()
    room = Room.query.filter_by(id=request.args.get('roomid')).first()
    pos = math.log(room.userpos(player))/math.log(2)
    return jsonify(room.status(),pos)