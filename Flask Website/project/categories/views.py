from flask import Blueprint, render_template, flash, redirect, url_for
from project import db
from .models import Category
from .forms import NewCategoryRequest


category_bp = Blueprint('categories', __name__, template_folder='templates')

@category_bp.route('/list', methods=['GET', 'POST'])
def list_courses():
    categories = Category.query.filter(Category.status == 'Active')  # Only approved categories
    return render_template('Course_List.html', categories=categories)


@category_bp.route('/request', methods=['GET', 'POST'])
def reg_course():
    form = NewCategoryRequest()

    if form.validate_on_submit():
        name = form.name.data
        desc = form.desc.data
        
        category = Category.query.filter_by(name=name).first()
        if category:
            flash('Category Already Exists')
            return redirect(url_for('categories.reg_course'))

        new_Category = Category(name, desc, 'Pending')
        db.session.add(new_Category)
        db.session.commit()
        flash('Category Submitted for review')
        return redirect(url_for('categories.reg_course'))
    
    return render_template('Request-Subject.html', form=form)
