from flask import render_template, Blueprint
from project import db
from project.students.models import Student


leaderboard_bp = Blueprint('leaderboard', __name__, template_folder='templates')

@leaderboard_bp.route('/')
def leaderboard():
    students = Student.query.order_by(Student.score.desc()).filter(Student.score > 0).limit(20)
            # SELECT * FROM Student 
            # ORDER BY Student.Score DESC 
            # WHERE Student.score > 0 


    return render_template('Leaderboard.html', students=students)
