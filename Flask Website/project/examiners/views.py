from project.examiners.pic_handler import add_profile_pic
from flask import Blueprint,render_template, redirect, url_for, flash, request, session
from flask_login.utils import login_required, login_user, logout_user, current_user
from werkzeug.urls import url_parse
from project import db, login
from project.examiners.models import Examiner
from project.students.models import Student
from project.assessment.models import Assessments
from project.categories.models import Category
from sqlalchemy import func
from project.examiners.forms import (SignUp, LogIn, 
                    ChangeBasic, ChangeDP, ChangePassword, Deactivate,
                    NewAssessment)

examiner_bp = Blueprint('examiner', __name__, template_folder='templates')

@login.user_loader
def load_user(user_id):
    if session['user'] == 'Student':
        return Student.query.get(int(user_id))
    elif session['user'] == 'Examiner':
        return Examiner.query.get(int(user_id))
    else:
        return None

@examiner_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = SignUp()

    if form.validate_on_submit():
        fname = form.fname.data
        lname = form.lname.data
        uname = form.uname.data
        email = form.email.data
        password = form.password.data
        user_exists = bool(Student.query.filter_by(email=email).first() or Examiner.query.filter_by(email=email).first())
        username_exists = bool(Student.query.filter_by(uname=uname).first() or Examiner.query.filter_by(uname=uname).first())
        if user_exists:
            flash('User Already Exists')
            return redirect(url_for('examiner.register'))
        if username_exists:
            flash('Username is not available')
            return redirect(url_for('student.register'))
        examiner = Examiner(fname, lname, uname, email, password, '')
        db.session.add(examiner)
        db.session.commit()
        return redirect(url_for('examiner.login'))
    
    return render_template('ExaminerRegistration.html', form=form)


@examiner_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LogIn()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        examiner = Examiner.query.filter_by(email=email).first()
        if examiner is None or not examiner.check_password(password):
            flash('Invalid username or password')
            return redirect(url_for('examiner.login'))
        login_user(examiner)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        session['user'] = examiner.role
        return redirect(next_page)
    
    return render_template('ExaminerLogin.html', form=form)


@examiner_bp.route('/logout')
def logout():
    logout_user()
    session.pop('user')
    return redirect(url_for('index'))

@login_required
@examiner_bp.route('/profile', methods=['GET', 'POST'])
def profile():
    if not current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if not session['user'] == 'Examiner':
        return redirect(url_for('index'))
    form = ChangeBasic()

    email = current_user.__getattr__('email')
    examiner = Examiner.query.filter_by(email = email).first()

    if form.validate_on_submit():
        form_fname = form.firstname.data
        form_lname = form.lastname.data
        form_bio = form.bio.data
        if form_fname != '':
            examiner.fname = form_fname
        if form_lname != '':
            examiner.lname = form_lname
        if form_bio != '':
            examiner.bio = form_bio
        
        db.session.add(examiner)
        db.session.commit()
        form.firstname.data = ''
        form.lastname.data = ''
        form.bio.data = ''
        return redirect(url_for('examiner.profile'))

    return render_template('Examiner-Settings-Basic.html', form=form, fname=examiner.fname, lname=examiner.lname, uname=examiner.uname, email=examiner.email)


@examiner_bp.route('/profilepic', methods=['GET', 'POST'])
@login_required
def profilepic():
    if not current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if not session['user'] == 'Examiner':
        return redirect(url_for('index'))
    form = ChangeDP()
    email = current_user.__getattr__('email')
    examiner = Examiner.query.filter_by(email = email).first()
    if form.validate_on_submit():
        pic_data = form.picture.data
        pic = add_profile_pic(pic_data, examiner.uname)
        current_user.profile_img = pic
        db.session.commit()
    profile_image = url_for('static', filename='student/'+current_user.profile_img)
    return render_template('Examiner-Settings-DP.html', form=form, fname=examiner.fname, profile_image=profile_image, lname=examiner.lname, uname=examiner.uname, email=examiner.email)


@examiner_bp.route('/security', methods=['GET', 'POST'])
@login_required
def security():
    if not current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if not session['user'] == 'Examiner':
        return redirect(url_for('index'))
    form = ChangePassword()

    email = current_user.__getattr__('email')
    examiner = Examiner.query.filter_by(email = email).first()

    if form.validate_on_submit():
        old_pwd = form.oldpassword.data
        new_pwd = form.newpassword.data
        cnfrm_pwd = form.confirmpassword.data

        if examiner.check_password(old_pwd):
            if new_pwd == cnfrm_pwd:
                examiner.set_password(new_pwd)
                db.session.add(examiner)
                db.session.commit()
                flash("Password Updated Successfully")
                flash(redirect(url_for('examiner.security')))
            else:
                flash("Passwords Dont Match")
                return redirect(url_for('examiner.security'))
        else:
            flash("Invalid Password provided")
            return redirect(url_for('examiner.security'))

    return render_template('Examiner-Settings-Security.html', form=form, fname=examiner.fname, lname=examiner.lname, uname=examiner.uname, email=examiner.email)


@examiner_bp.route('/deactivate', methods=['GET', 'POST'])
@login_required
def deactivate():
    if not current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if not session['user'] == 'Examiner':
        return redirect(url_for('index'))
    form = Deactivate()

    email = current_user.__getattr__('email')
    examiner = Examiner.query.filter_by(email = email).first()

    if form.validate_on_submit():
        pwd = form.confirmpassword.data
        if examiner.check_password(pwd):
            db.session.delete(examiner)
            db.session.commit()
        else:
            flash("Invalid Password provided")
            return redirect(url_for('examiner.security'))

    return render_template('Examiner-Settings-Deactivate.html', form=form, fname=examiner.fname, lname=examiner.lname, uname=examiner.uname, email=examiner.email)


@examiner_bp.route('/newAssessment', methods=['GET', 'POST'])
@login_required
def new_assessment():
    if not current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if not session['user'] == 'Examiner':
        return redirect(url_for('index'))

    form = NewAssessment()
    categories = Category.query.filter(Category.status == 'Active')
    form.category_name.choices =[(category.id, category.name) for category in categories]

    if form.validate_on_submit():
        name = form.name.data
        difficulty = form.difficulty.data
        num_questions = form.num_questions.data
        category = form.category_name.data

        exist_assessment = Assessments.query.filter(func.lower(Assessments.name) == func.lower(name)).first()
        if exist_assessment:
            flash('Assessment Already Exists')
            return redirect(url_for('examiner.new_assessment'))
        session['assess_name'] = name
        session['difficulty'] = difficulty
        session['num_questions'] = num_questions
        session['category'] = category
        return redirect(url_for('assessment.new_assessment_detail'))
    return render_template('ExaminerDashBoardNew.html', form=form, uname=current_user.__getattr__('uname'))


@examiner_bp.route('/listAssessment', methods=['GET', 'POST'])
@login_required
def list_assessment():
    if not current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if not session['user'] == 'Examiner':
        return redirect(url_for('index'))
    
    my_assessments = Assessments.query.filter_by(examiner_id=current_user.__getattr__('id'))

    return render_template('ExaminerDashBoardDeployed.html', my_assessments=my_assessments, uname=current_user.__getattr__('uname'))


@examiner_bp.route('/chatroom', methods=['GET', 'POST'])
@login_required
def chatroom():
    if not current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if not session['user'] == 'Examiner':
        return redirect(url_for('index'))

    return render_template('ExaminerChatRoom.html', uname=current_user.__getattr__('uname'))