from project import db
from project.categories.models import Category
from project.examiners.models import Examiner
from project.assessment.models import Assessments, Questions
from project.restapi.admin_model import Admin

new_course = Category('Software Development and Analysis', 'Place holder', 'Active')
db.session.add(new_course)

new_course = Category('Algorithms and Design', 'Place holder', 'Active')
db.session.add(new_course)

new_course = Category('Parallel and Distributed Computing', 'Place holder', 'Active')
db.session.add(new_course)

new_course = Category('Data Structures', 'Place holder', 'Active')
db.session.add(new_course)

new_course = Category('Object Oriented Programming', 'Place holder', 'Active')
db.session.add(new_course)

new_course = Category('Programmming Fundamentals', 'Place holder', 'Active')
db.session.add(new_course)
db.session.commit()

new_Examiner = Examiner('First', 'Last', 'examiner1', 'examiner1@test.com', 'zxcasd', '')
db.session.add(new_Examiner)

new_Examiner = Examiner('First', 'Last', 'examiner2', 'examiner2@test.com', 'zxcasd', '')
db.session.add(new_Examiner)

db.session.commit()

new_assignment = Assessments('Programming', 6, 0, 'Hard', 'Active', 1)
db.session.add(new_assignment)

new_assignment = Assessments('OpenMP' , 3, 0 , 'Hard', 'Active', 1)
db.session.add(new_assignment)

new_assignment = Assessments('Flask Practice' , 1 , 0 , 'Hard', 'Active', 2)
db.session.add(new_assignment)

new_assignment = Assessments('Nodejs',  1, 0 , 'Hard', 'Active', 1)
db.session.add(new_assignment)

db.session.commit()

for x in range(1, 5):
    new_Questions = Questions(x,1,f'PlaceHolder Q{x}', 'PlaceHolder A1', 'PlaceHolder A2', 'PlaceHolder A3', 'PlaceHolder A4', '1')
    db.session.add(new_Questions)

    new_Questions = Questions(x,2,f'PlaceHolder Q{x}', 'PlaceHolder A1', 'PlaceHolder A2', 'PlaceHolder A3', 'PlaceHolder A4', '4')
    db.session.add(new_Questions)

    new_Questions = Questions(x,3,f'PlaceHolder Q{x}', 'PlaceHolder A1', 'PlaceHolder A2', 'PlaceHolder A3' , 'PlaceHolder A4','2')
    db.session.add(new_Questions)

    new_Questions = Questions(x,4,f'PlaceHolder Q{x}', 'PlaceHolder A1', 'PlaceHolder A2', 'PlaceHolder A3', 'PlaceHolder A4','3')
    db.session.add(new_Questions)
db.session.commit()

new_admin = Admin('Nuc', 'leotic', 'Mz', 'test@test.com', '12345')
db.session.add(new_admin)
db.session.commit()
