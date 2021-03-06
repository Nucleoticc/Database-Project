from project.students.models import Student
from project import db
import json
from flask import Blueprint, render_template, redirect, url_for, session
from wtforms import validators
from wtforms.fields.core import IntegerField, RadioField, StringField
from wtforms.fields.simple import TextAreaField
from project.assessment.models import Questions, Assessments, Rate_Assessment, Solved_Assessment
from project.assessment.forms import Delete_Assessment, New_Assessment_Detail, Rate_Assessment_Form, Submit_Assessment
from flask_login import login_required
from flask_login.utils import current_user
from sqlalchemy import and_


assessment_bp = Blueprint('assessment', __name__, template_folder='templates')


@assessment_bp.route('/new', methods=['GET', 'POST'])
@login_required
def new_assessment_detail():
    if not current_user.is_authenticated:
        return redirect(url_for('index'))
    if not session['user'] == 'Examiner':
        return redirect(url_for('index'))
    
    name = session['assess_name']
    difficulty = session['difficulty']
    category = session['category']
    num_questions = session['num_questions']
    

    total_questions = []
    for q in range(int(num_questions)):
        question = []
        setattr(New_Assessment_Detail, 'question'+str(q+1), TextAreaField([validators.InputRequired()]))
        setattr(New_Assessment_Detail, 'ch'+str(q+1)+'1', StringField([validators.InputRequired()]))
        setattr(New_Assessment_Detail, 'ch'+str(q+1)+'2', StringField([validators.InputRequired()]))
        setattr(New_Assessment_Detail, 'ch'+str(q+1)+'3', StringField([validators.InputRequired()]))
        setattr(New_Assessment_Detail, 'ch'+str(q+1)+'4', StringField([validators.InputRequired()]))
        setattr(New_Assessment_Detail, 'ans'+str(q+1), IntegerField([validators.InputRequired()]))
        question.append('question'+str(q+1))
        question.append('ch'+str(q+1)+'1')
        question.append('ch'+str(q+1)+'2')
        question.append('ch'+str(q+1)+'3')
        question.append('ch'+str(q+1)+'4')
        question.append('ans'+str(q+1))
        total_questions.append(question)
    

    form = New_Assessment_Detail()
    if form.validate_on_submit():
        new_assessment = Assessments(name, category, 0, difficulty, 'Active', current_user.__getattr__('id'))
        db.session.add(new_assessment)
        db.session.commit()
        for q in range(int(num_questions)):
            question = []
            question.append(int(q+1))
            question.append(new_assessment.id)
            question.append(getattr(form, 'question'+str(q+1)).data)
            question.append(getattr(form, 'ch'+str(q+1)+'1').data)
            question.append(getattr(form, 'ch'+str(q+1)+'2').data)
            question.append(getattr(form, 'ch'+str(q+1)+'3').data)
            question.append(getattr(form, 'ch'+str(q+1)+'4').data)
            question.append(getattr(form, 'ans'+str(q+1)).data)
            new_question = Questions(question[0], question[1], question[2], question[3], question[4], 
                                    question[5], question[6], question[7])
            db.session.add(new_question)
            db.session.commit()
            question = []
        session.pop('assess_name')
        session.pop('difficulty')
        session.pop('category')
        session.pop('num_questions')
        return redirect(url_for('examiner.list_assessment'))
    return render_template('Examiner-Assess.html', form=form, total_questions=total_questions, aname=name)


@assessment_bp.route('/detail/<assessment_id>', methods=['GET', 'POST'])
@login_required
def assessment_detail(assessment_id):
    if not current_user.is_authenticated:
        return redirect(url_for('index'))
    if not session['user'] == 'Examiner':
        return redirect(url_for('index'))

    questions = Questions.query.filter_by(assessment_id=assessment_id).all()
    assessment = Assessments.query.filter_by(id=assessment_id).first()
    category = assessment.category.name

    total_marks = 1
    total_questions = 0
    for _ in questions:
        total_questions += 1

    if questions[0].assessment.difficulty == 'Easy':
        total_marks = 3*total_questions
    elif questions[0].assessment.difficulty == 'Medium':
        total_marks = 5*total_questions
    elif questions[0].assessment.difficulty == 'Hard':
        total_marks = 7*total_questions

    form = Delete_Assessment()
    if form.validate_on_submit():
        for question in Questions.query.filter_by(assessment_id=assessment_id).all():
            db.session.delete(question)
            db.session.commit()
        
        db.session.delete(assessment)
        db.session.commit()

        return redirect(url_for('examiner.list_assessment'))
    return render_template('Examiner-Assess-Details.html', form=form, 
                          total_marks=total_marks, assessment=assessment, category=category, 
                          questions=questions)


@assessment_bp.route('/list/<category_id>')
@login_required
def list_assessment(category_id):
    if not current_user.is_authenticated:
        return redirect(url_for('index'))
    if not session['user'] == 'Student':
        return redirect(url_for('index'))

    assessments = Assessments.query.filter_by(category_id=category_id).filter(Assessments.status == 'Active').all()

    return render_template("Assess-List.html", assessments=assessments)


@assessment_bp.route('/attempted/<assessment_id>')
@login_required
def already_attempted(assessment_id):
    if not current_user.is_authenticated:
        return redirect(url_for('index'))
    if not session['user'] == 'Student':
        return redirect(url_for('index'))

    solved_assessment_data = Solved_Assessment.query.filter(
        and_(
            Solved_Assessment.student_id == current_user.__getattr__('id'),
            Solved_Assessment.assessment_id == assessment_id
        )
    ).first()
    rate_assessment = Rate_Assessment.query.filter(
        and_(
            Rate_Assessment.student_id == current_user.__getattr__('id'),
            Rate_Assessment.assessment_id == assessment_id
        )
    ).first()
    questions = Questions.query.filter_by(assessment_id=assessment_id).all()
    total_marks = 1
    total_questions = 0
    for _ in questions:
        total_questions += 1
    if questions[0].assessment.difficulty == 'Easy':
        total_marks = 3*total_questions
    elif questions[0].assessment.difficulty == 'Medium':
        total_marks = 5*total_questions
    elif questions[0].assessment.difficulty == 'Hard':
        total_marks = 7*total_questions
    answers = json.loads(solved_assessment_data.answers)
    answers = answers['answers']
    omarks = solved_assessment_data.marks

    return render_template("Student-Assess-Details.html", answers=answers, omarks=omarks, 
                           questions=questions, rate_assessment=rate_assessment, total_marks=total_marks)



@assessment_bp.route('/solve/<assessment_id>', methods=['GET', 'POST'])
@login_required
def solve_assessment(assessment_id):
    if not current_user.is_authenticated:
        return redirect(url_for('index'))
    if not session['user'] == 'Student':
        return redirect(url_for('index'))

    previously_solved = Solved_Assessment.query.filter(
                            and_(
                                Solved_Assessment.student_id == current_user.__getattr__('id'),
                                Solved_Assessment.assessment_id == assessment_id
                            )
        ).first()
    if previously_solved:
        return redirect(url_for('assessment.already_attempted', assessment_id=assessment_id))

    questions = Questions.query.filter_by(assessment_id=assessment_id)

    choices = []
    total_questions = 0
    for idx, question in enumerate(questions):
        choice = RadioField([validators.InputRequired()], 
                            choices=[('1', question.op1), ('2', question.op2), ('3', question.op3),
                                     ('4', question.op4)])
        setattr(Submit_Assessment, 'choices'+str(idx+1), choice)
        choices.append('choices'+str(idx+1))
        total_questions += 1
    
    total_marks = 1
    if questions[0].assessment.difficulty == 'Easy':
        total_marks = 3*total_questions
    elif questions[0].assessment.difficulty == 'Medium':
        total_marks = 5*total_questions
    elif questions[0].assessment.difficulty == 'Hard':
        total_marks = 7*total_questions

    form = Submit_Assessment()

    if form.validate_on_submit():
        earned_marks = 0
        marks = total_marks/total_questions
        answers = list()
        for idx, question in enumerate(questions):
            student_answer = getattr(form, choices[idx]).data
            answers.append(student_answer)
            if student_answer == question.correct_op:
                earned_marks += marks
        answers = json.dumps({'answers':answers})
        if questions[0].assessment.difficulty == 'Easy':
            total_marks = 3*total_questions
        elif questions[0].assessment.difficulty == 'Medium':
            total_marks = 5*total_questions
        elif questions[0].assessment.difficulty == 'Hard':
            total_marks = 7*total_questions

        
        student = Student.query.filter_by(id=current_user.__getattr__('id')).first()
        student.attempted += 1
        if earned_marks >= total_marks*0.50:
            student.solved += 1
        student.score += earned_marks
        solved_assessment = Solved_Assessment(current_user.__getattr__('id'), int(assessment_id), earned_marks, answers)
        db.session.add(solved_assessment)
        db.session.commit()
        db.session.add(student)
        db.session.commit()
        return redirect(url_for('assessment.review_assessment', assessment_id=assessment_id))
    return render_template("Student-Solve-Assess.html", form=form, questions=questions, total_marks=total_marks, choices=choices)


@assessment_bp.route('/review/<assessment_id>', methods=['GET', 'POST'])
@login_required
def review_assessment(assessment_id):
    if not current_user.is_authenticated:
        return redirect(url_for('index'))
    if not session['user'] == 'Student':
        return redirect(url_for('index'))

    review = Rate_Assessment.query.filter(
        and_( Rate_Assessment.student_id == current_user.__getattr__('id'),
              Rate_Assessment.assessment_id == int(assessment_id) )
    ).first()
    
    if review:
        return redirect(url_for('student.completed_assessment'))

    solved_assessment = Solved_Assessment.query.filter(
        and_( Solved_Assessment.student_id == current_user.__getattr__('id'),
              Solved_Assessment.assessment_id == int(assessment_id) )
    ).first()
    
    form = Rate_Assessment_Form()

    if form.validate_on_submit():
        rating = form.rating.data
        rating_id = Rate_Assessment.query.count()
        new_rating = Rate_Assessment(rating_id+1, current_user.__getattr__('id'), assessment_id, rating)
        db.session.add(new_rating)
        db.session.commit()

        assessment = Assessments.query.filter_by(id=assessment_id).first()
        if assessment.total_num_rating == 0:
            assessment.avg_rating = rating
        else:
            assessment.avg_rating = (assessment.avg_rating + rating)/(assessment.total_num_rating + 1)
        assessment.total_num_rating += 1

        db.session.add(assessment)
        db.session.commit()

        return redirect(url_for('student.completed_assessment'))
    return render_template('Assess-Review.html', form=form, solved_assessment=solved_assessment)