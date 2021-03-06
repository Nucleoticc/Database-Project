from project import db

class Assessments(db.Model):
    __tablename__ = 'assessments'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(40))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    category = db.relationship('Category', backref='categories')
    avg_rating = db.Column(db.Float)
    total_num_rating = db.Column(db.Integer)
    difficulty = db.Column(db.Text)
    status = db.Column(db.String(10))
    examiner_id = db.Column(db.Integer, db.ForeignKey('examiners.id'))
    examiner = db.relationship('Examiner', backref='examiners') 

    def __init__(self, name, category_id, rating, difficulty, status, examiner_id):
        self.name = name
        self.category_id = category_id
        self.avg_rating = rating
        self.difficulty = difficulty
        self.total_num_rating = 0
        self.status = status
        self.examiner_id = examiner_id


class Questions(db.Model):
    __tablename__ = 'questions'

    id = db.Column(db.Integer)
    text = db.Column(db.String(256))
    assessment_id = db.Column(db.Integer, db.ForeignKey('assessments.id'))
    assessment = db.relationship('Assessments', backref = 'assessments', lazy=True)
    op1 = db.Column(db.String(256))
    op2 = db.Column(db.String(256))
    op3 = db.Column(db.String(256))
    op4 = db.Column(db.String(256))
    correct_op = db.Column(db.String(10))

    __table_args__ = (
        db.PrimaryKeyConstraint(
            assessment_id, id   
        ),
    )

    def __init__(self, id, assessment_id, text, op1, op2, op3, op4, correct_op):
        self.id = id
        self.text = text
        self.assessment_id = assessment_id
        self.op1 = op1
        self.op2 = op2
        self.op3 = op3
        self.op4 = op4
        self.correct_op = correct_op


class Solved_Assessment(db.Model):
    __tablename__ = 'solved_assessment'

    student_id = db.Column(db.Integer, db.ForeignKey('students.id'))
    student = db.relationship('Student', backref='solvestudents', lazy=True)
    assessment_id = db.Column(db.Integer, db.ForeignKey('assessments.id'))
    assessment = db.relationship('Assessments', backref = 'solveassessments', lazy=True)
    marks = db.Column(db.Integer)
    answers = db.Column(db.String(256))

    __table_args__ = (
        db.PrimaryKeyConstraint(
            student_id, assessment_id,
        ),
    )

    def __init__(self, student_id, assessment_id, marks, answers):
        self.student_id = student_id
        self.assessment_id = assessment_id
        self.marks = marks
        self.answers = answers


class Rate_Assessment(db.Model):
    __tablename__ = 'rate_assessment'

    rating_id = db.Column(db.Integer)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'))
    student = db.relationship('Student', backref='ratestudents', lazy=True)
    assessment_id = db.Column(db.Integer, db.ForeignKey('assessments.id'))
    assessment = db.relationship('Assessments', backref = 'rateassessments', lazy=True)
    rating = db.Column(db.Integer)

    __table_args__ = (
        db.PrimaryKeyConstraint(
            rating_id, student_id, assessment_id,
        ),
    )

    def __init__(self, rating_id, student_id, assessment_id, rating):
        self.rating_id = rating_id
        self.student_id = student_id
        self.assessment_id = assessment_id
        self.rating = rating