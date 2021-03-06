from project.students.pic_handler import add_profile_pic
from project.categories.models import Category
from project.assessment.models import Assessments, Solved_Assessment
from flask import Blueprint,render_template, redirect, url_for, flash, request, session
from flask_login.utils import login_required, login_user, logout_user, current_user
from werkzeug.urls import url_parse
from project import db, login
from project.students.models import Student
from project.examiners.models import Examiner
from project.students.forms import SignUp, LogIn, ChangeBasic, ChangeDP, ChangePassword, Deactivate
import random

student_bp = Blueprint('student', __name__, template_folder='templates')

@login.user_loader
def load_user(user_id):
    if session['user'] == 'Student':
        return Student.query.get(int(user_id))
    elif session['user'] == 'Examiner':
        return Examiner.query.get(int(user_id))
    else:
        return None

@login.unauthorized_handler
def unauthorized_callback():
    return redirect('/student/login')


@student_bp.route('/register', methods=['GET', 'POST'])
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
        # (SELECT * FROM Student WHERE Student.email = email) or (SELECT * FROM Examiners WHERE Student.email = email)
        username_exists = bool(Student.query.filter_by(uname=uname).first() or Examiner.query.filter_by(uname=uname).first())
        # (SELECT * FROM Student WHERE Student.uname = uname) or (SELECT * FROM Examiners WHERE Student.uname = uname)
        if user_exists:
            flash('User Already Exists')
            return redirect(url_for('student.register'))
        if username_exists:
            flash('Username is not available')
            return redirect(url_for('student.register'))
        student = Student(fname, lname, uname, email, password, 0, 0, 0, '')
        db.session.add(student)
        db.session.commit()
        return redirect(url_for('student.login'))
    
    return render_template('StudentRegistration.html', form=form)


@student_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LogIn()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        student = Student.query.filter_by(email=email).first()
        if student is None or not student.check_password(password):
            flash('Invalid username or password')
            return redirect(url_for('student.login'))
        login_user(student)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        session['user'] = student.role
        return redirect(next_page)
    return render_template('StudentLogin.html', form=form)


@student_bp.route('/logout')
@login_required
def logout():
    logout_user()
    session.pop('user')
    return redirect(url_for('index'))


@login_required
@student_bp.route('/profile', methods=['GET', 'POST'])
def profile():
    if not current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if not session['user'] == 'Student':
        return redirect(url_for('index'))
    form = ChangeBasic()

    email = current_user.__getattr__('email')
    student = Student.query.filter_by(email = email).first()

    if form.validate_on_submit():
        form_fname = form.firstname.data
        form_lname = form.lastname.data
        form_bio = form.bio.data
        if form_fname != '':
            student.fname = form_fname
        if form_lname != '':
            student.lname = form_lname
        if form_bio != '':
            student.bio = form_bio
        
        db.session.add(student)
        db.session.commit()
        form.firstname.data = ''
        form.lastname.data = ''
        form.bio.data = ''
        return redirect(url_for('student.profile'))

    return render_template('Student-Settings-Basic.html', form=form, fname=student.fname, lname=student.lname, uname=student.uname, email=student.email)


@student_bp.route('/profilepic', methods=['GET', 'POST'])
@login_required
def profilepic():
    if not current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if not session['user'] == 'Student':
        return redirect(url_for('index'))
    form = ChangeDP()
    email = current_user.__getattr__('email')
    student = Student.query.filter_by(email = email).first()
    if form.validate_on_submit():
        pic_data = form.picture.data
        pic = add_profile_pic(pic_data, student.uname)
        current_user.profile_img = pic
        db.session.commit()
    profile_image = url_for('static', filename='student/'+current_user.profile_img)
    return render_template('Student-Settings-DP.html', form=form, fname=student.fname, profile_image=profile_image, lname=student.lname, uname=student.uname, email=student.email)


@student_bp.route('/security', methods=['GET', 'POST'])
@login_required
def security():
    if not current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if not session['user'] == 'Student':
        return redirect(url_for('index'))
    form = ChangePassword()

    email = current_user.__getattr__('email')
    student = Student.query.filter_by(email = email).first()

    if form.validate_on_submit():
        old_pwd = form.oldpassword.data
        new_pwd = form.newpassword.data
        cnfrm_pwd = form.confirmpassword.data

        if student.check_password(old_pwd):
            if new_pwd == cnfrm_pwd:
                student.set_password(new_pwd)
                db.session.add(student)
                db.session.commit()
                flash("Password Updated Successfully")
                flash(redirect(url_for('student.security')))
            else:
                flash("Passwords Dont Match")
                return redirect(url_for('student.security'))
        else:
            flash("Invalid Password provided")
            return redirect(url_for('student.security'))

    return render_template('Student-Settings-Security.html', form=form, fname=student.fname, lname=student.lname, uname=student.uname, email=student.email)


@student_bp.route('/deactivate', methods=['GET', 'POST'])
@login_required
def deactivate():
    if not current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if not session['user'] == 'Student':
        return redirect(url_for('index'))
    form = Deactivate()

    email = current_user.__getattr__('email')
    student = Student.query.filter_by(email = email).first()

    if form.validate_on_submit():
        pwd = form.confirmpassword.data
        if student.check_password(pwd): 
            logout_user()
            session.pop('user')
            db.session.delete(student)
            db.session.commit()
        else:
            flash("Invalid Password provided")
            return redirect(url_for('student.security'))

    return render_template('Student-Settings-Deactivate.html', form=form, fname=student.fname, lname=student.lname, uname=student.uname, email=student.email)


@student_bp.route('/completed')
@login_required
def completed_assessment():
    if not current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if not session['user'] == 'Student':
        return redirect(url_for('index'))

    completed_list = Solved_Assessment.query.filter_by(student_id=current_user.__getattr__('id')).all()

    return render_template('StudentDashBoardComplete.html', completed_list=completed_list, uname=current_user.__getattr__('uname'))


@student_bp.route('/recommended')
@login_required
def recommended_assessment():
    if not current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if not session['user'] == 'Student':
        return redirect(url_for('index'))

    user_attempted_list = Solved_Assessment.query.filter_by(student_id=current_user.__getattr__('id')).all()

    categories = []
    for assessment in user_attempted_list:
        categories.append(assessment.assessment.category_id)
    
    recommended_assessment = []
    for category in categories:
        assessments = Assessments.query.filter_by(category_id=category).limit(10)
        random1, random2, random3 = random.randint(0, 9), random.randint(0, 9), random.randint(0, 9)
        try:
            recommended_assessment.append(assessments[random1])
        except IndexError:
            pass
        try:
            recommended_assessment.append(assessments[random2])
        except IndexError:
            pass
        try:
            recommended_assessment.append(assessments[random3])
        except IndexError:
            pass

    return render_template('StudentDashBoardRecommended.html', recommended_assessment=recommended_assessment, uname=current_user.__getattr__('uname'))


@student_bp.route('/new')
@login_required
def new_assessment():
    if not current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if not session['user'] == 'Student':
        return redirect(url_for('index'))
    
    categories = Category.query.filter(Category.status == 'Active')

    return render_template('StudentDashBoardNew.html', categories=categories, uname=current_user.__getattr__('uname'))