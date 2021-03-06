from project import db


class ChatRoom(db.Model):
    __tablename__ = 'chatroom'

    id = db.Column(db.Integer, primary_key=True)
    examiner_id = db.Column(db.Integer, db.ForeignKey('examiners.id'))
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'))
    student = db.relationship('Student', backref = 'chatstudent', lazy=True)
    examiner = db.relationship('Examiner', backref = 'chatexaminer', lazy=True)

    __table_args__ = (
        db.PrimaryKeyConstraint(
            id, examiner_id,
        ),
    )

    def __init__(self, examiner):
        self.examiner_id = examiner


class ChatRoomMessages(db.Model):
    __tablename__='chatroommessages'
    
    message_id = db.Column(db.Integer, primary_key=True)
    chatroom_id = db.Column(db.Integer, db.ForeignKey('chatroom.id'))
    chatroom = db.relationship('ChatRoom', backref = 'chatroom', lazy=True)
    message_text = db.Column(db.String(1024))
    sender_id = db.Column(db.Integer)
    
    __table_args__ = (
        db.PrimaryKeyConstraint(
            id, chatroom_id,
        ),
    )

    def __init__(self, chat_id, text, sender):
        self.chatroom_id = chat_id
        self.message_text = text
        self.sender_id = sender
