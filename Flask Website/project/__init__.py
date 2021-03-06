from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_cors import CORS
app = Flask(__name__)

app.secret_key = 'nucleotic'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["PROPAGATE_EXCEPTIONS"] = True

db = SQLAlchemy(app)
Migrate(app, db)
login = LoginManager(app)
cors = CORS(app)

@app.before_first_request
def create_tables():
    db.create_all()


from project.students.views import student_bp
from project.examiners.views import examiner_bp
from project.restapi.admin_resources import admin_bp
from project.categories.views import category_bp
from project.assessment.views import assessment_bp
from project.leaderboard.views import leaderboard_bp


app.register_blueprint(examiner_bp, url_prefix='/examiner')
app.register_blueprint(student_bp, url_prefix='/student')
app.register_blueprint(category_bp, url_prefix='/category')
app.register_blueprint(leaderboard_bp, url_prefix='/leaderboard')
app.register_blueprint(assessment_bp, url_prefix='/assessment')
app.register_blueprint(admin_bp, url_prefix='/api/admin')