from flask import session
from flask_socketio import emit, join_room, leave_room
from flask_login import current_user
from .. import socketio


@socketio.on('joined', namespace='/game')
def joined(message):
    """Sent by clients when they enter a room.
    A status message is broadcast to all people in the room."""
    room = session.get('room_id')
    join_room(room)
    emit('status', {'msg': current_user.name + ' has entered the room.'}, room=room)



@socketio.on('text', namespace='/game')
def text(message):
    """Sent by a client when the user entered a new message.
    The message is sent to all people in the room."""
    room = session.get('room_id')
    emit('message', {'msg': current_user.name + ':' + message['msg']}, room=room)


@socketio.on('ww', namespace='/game')
def test(message):
    """Sent by a client when the user entered a new message.
    The message is sent to all people in the room."""
    room = session.get('room_id')
    print('my message',message['msg'])
    print(room)
    emit('message', {'msg': current_user.name + ':' + message['msg']})


@socketio.on('left', namespace='/game')
def left(message):
    """Sent by clients when they leave a room.
    A status message is broadcast to all people in the room."""
    room = session.get('room_id')
    leave_room(room)
    emit('status', {'msg': current_user.name + ' has left the room.'}, room=room)

