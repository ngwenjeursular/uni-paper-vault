"""
the home route
"""
import os
from flask import render_template
from flask import Blueprint, render_template
from app.models.unit import Unit
from flask import request, redirect, url_for, flash
from app.models import Question 
from app import db
from flask_login import current_user, login_required


home_bp = Blueprint('home', __name__)

@home_bp.route('/')
@home_bp.route('/home')
def index():
	"""
	Handle the home route
	"""
	units = Unit.query.all()
	years = [1, 2, 3, 4]  # List of years
	return render_template('home.html', years=years, units=units)


@home_bp.route('/year/<int:year_id>')
def select_year(year_id):
	"""
	Handle the year selection route
	"""
	return render_template('year.html', year_id=year_id)

@home_bp.route('/year/<int:year_id>/semester/<int:sem_id>')
def select_semester(year_id, sem_id):
	"""
	Handle the semester selection route
	"""
	units = get_units_for_semester(year_id, sem_id)
	print(units)
    
	# Debugging output: Print each unit's attributes
	print(f"Units for Year {year_id}, Semester {sem_id}:")
	for unit in units:
		print(f"Unit ID: {unit.id}, Unit Name: {unit.unit_name}")
            
	return render_template('semester.html', year_id=year_id, sem_id=sem_id, units=units)



def get_units_for_semester(year_id, sem_id):
    """
    Retrieve units based on year and semester.
    """
    return Unit.query.filter_by(year_id=year_id, semester_id=sem_id).all()


@home_bp.route('/year/<int:year_id>/semester/<int:sem_id>/units')
def units(year_id, sem_id):
	"""
	Display units for the selected year and semester
	"""
	units = get_units_for_semester(year_id, sem_id)
	return render_template('units.html', units=units, year_id=year_id, sem_id=sem_id)



@home_bp.route('/year/<int:year_id>/semester/<int:sem_id>/unit/<int:unit_id>/<string:unit_name>', methods=['GET', 'POST'])
@login_required
def unit_page(year_id, sem_id, unit_id, unit_name):
    """
    Display the unit page where users can upload files or post questions
    """
    print(f"Accessed unit page: {unit_name} (ID: {unit_id}) for Year {year_id}, Semester {sem_id}")

    question_text = None

    if request.method == 'POST':
        question_text = request.form.get('question')

        if question_text:
            new_question = Question(content=question_text, unit_id=unit_id)
            print(f"New Question: {new_question.to_dict()}")

            try:
                db.session.add(new_question)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                print(f"Error saving question: {e}")

            print(f"New question posted: {question_text}")

            return redirect(url_for('home.unit_page', year_id=year_id, sem_id=sem_id, unit_id=unit_id, unit_name=unit_name))

    questions = Question.query.filter_by(unit_id=unit_id).all()
    print(f"Questions for unit {unit_id}: {[q.content for q in questions]}")
    print(f"Rendering unit page with questions: {questions}")

    return render_template('unit_page.html', year_id=year_id, sem_id=sem_id, unit_id=unit_id, unit_name=unit_name, questions=questions)


from flask import request, redirect, url_for, flash
from flask_login import current_user
from app.models.user import User
from app.models.answer import Answer
from app.models.comment import Comment

@home_bp.route('/question/<int:question_id>', methods=['GET', 'POST'])
def question_page(question_id):
    """
    Display the full question with answer input and comment section
    """
    question = Question.query.get_or_404(question_id)

    if request.method == 'POST':
        answer_content = request.form.get('answer')
        if answer_content:
            answer = Answer(content=answer_content, question_id=question_id, user_id=current_user.id)
            db.session.add(answer)
            db.session.commit()
            flash('Your answer has been submitted!', 'success')
            return redirect(url_for('home.question_page', question_id=question_id))

    answers = Answer.query.filter_by(question_id=question_id).all()

    return render_template('question_page.html', question=question, answers=answers)


# added
@home_bp.route('/comment/<int:answer_id>', methods=['POST'])
@login_required
def add_comment(answer_id):
    """
    Add a comment to an answer
    """
    print("Comment route accessed")
    from app.models.user import User  # Defer import until function execution
    print(User)

    comment_content = request.form.get('comment')
    if comment_content:

        print(f"Comment content: {comment_content}")
        print(f"Answer ID: {answer_id}")
        print(f"User ID: {current_user.id}")

        comment = Comment(content=comment_content, answer_id=answer_id, user_id=current_user.id)
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been posted!', 'success')
    
    return redirect(url_for('home.question_page', question_id=Answer.query.get_or_404(answer_id).question_id))



