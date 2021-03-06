from flask import request, Blueprint
from project.examiners.models import Examiner
from project.students.models import Student
from project.categories.models import Category
from .admin_model import Admin, AdminSchema, StudentSchema, CategorySchema, ExaminerSchema
from project import db
# 
#  This part will run with AJAX requests(POSTMAN, Vue, React, etc).
#  A vue app which works with this component is also attached in admin panel folder
# 

admin_bp = Blueprint('adminapi', __name__, template_folder='templates')

admin_schema = AdminSchema()
student_schema = StudentSchema()
examiner_schema = ExaminerSchema()
category_schema = CategorySchema()

@admin_bp.route('/login', methods=['GET', 'POST'])
def login_post():
    data = admin_schema.load(request.get_json())
    admin = Admin.query.filter_by(email=data['email']).first()

    if admin is None or not admin.check_password(data['password']):
        return {'message': 'Wrong Credentials'}, 404

    return {'userId': '1', 'token':'placeholdertoken'}


@admin_bp.route('/student', methods=['GET'])
def get_students():
    students = Student.query.all()
    student_list = []
    for student in students:
        student_list.append(student_schema.dump(student))
    return {'students':student_list}, 200


@admin_bp.route('/examiner', methods=['GET'])
def get_examiners():
    examiners = Examiner.query.all()
    examiner_list = []
    for examiner in examiners:
        examiner_list.append(examiner_schema.dump(examiner))
    return {'examiners':examiner_list}, 200


@admin_bp.route('/categories', methods=['GET'])
def get_categories():
    categories = Category.query.all()
    category_list = []
    for category in categories:
        category_list.append(category_schema.dump(category))
    return {'categories':category_list}, 200


@admin_bp.route('/categories', methods=['PUT'])
def enable_category():
    category_id = request.get_json()
    category_id = category_id['category_id']

    category = Category.query.filter_by(id=category_id).first()

    if category.status == 'Pending':
        category.status = 'Active'
        db.session.add(category)
        db.session.commit()
        return {'message':'Category Activated'}, 200
    
    return {'message':'Category Not Found or it is already active'}, 404
