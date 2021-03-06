from project import socketio, db
from flask import Blueprint, render_template, request
import datetime
from project.chatroom.models import ChatRoomMessages, ChatRoom
from flask_socketio import join_room
from flask_login import login_required

chat_room_bp = Blueprint('chatroom', __name__, template_folder='templates')


@chat_room_bp.route('/<room_id>/messages/')
@login_required
def get_older_messages(room_id):
    room = ChatRoom.query.filter_by(id=room_id).first()
    if room:
        page = int(request.args.get('page', 0))
        messages = ChatRoomMessages.query.filter_by(chatroom_id=room_id).paginate(page, 10, False)
        return messages


@socketio.on('send_message')
def handle_send_message_event(data):
    data['created_at'] = datetime.now().strftime("%d %b, %H:%M")
    new_message = ChatRoomMessages(data['room'], data['message'], data['username'])
    db.session.add(new_message)
    db.session.commit()
    socketio.emit('receive_message', data, room=data['room'])


@socketio.on('join_room')
def handle_join_room_event(data):
    join_room(data['room'])
    socketio.emit('join_room_announcement', data, room=data['room'])