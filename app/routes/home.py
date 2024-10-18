"""
the home route
"""
from app.models.comment import Comment
from app.models.answer import Answer
from app.models.user import User
from flask_login import current_user
import os
from flask import render_template
from flask import Blueprint, render_template
from app.models.unit import Unit
from flask import request, redirect, url_for, flash
from app.models import Question
from app import db
from flask_login import current_user, login_required
from sqlalchemy.orm import joinedload
from datetime import datetime, timedelta
import re
from app.utils import parse_tags
from flask import make_response
from werkzeug.utils import secure_filename
from flask import current_app, flash




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


# @home_bp.route('/year/<int:year_id>/semester/<int:sem_id>/unit/<int:unit_id>/<string:unit_name>', methods=['GET', 'POST'])
# def unit_page(year_id, sem_id, unit_id, unit_name):
#     """
#     Display the unit page where users can upload files or post questions
#     """
#     print(
#         f"Accessed unit page: {unit_name} (ID: {unit_id}) for Year {year_id}, Semester {sem_id}")

#     question_text = None

#     if request.method == 'POST':
#         question_text = request.form.get('question')

#         if question_text:
#             # modified
#             new_question = Question(content=question_text, unit_id=unit_id, user_id=current_user.id)
#             print(f"New Question: {new_question.to_dict()}")

#             try:
#                 db.session.add(new_question)
#                 db.session.commit()
#             except Exception as e:
#                 db.session.rollback()
#                 print(f"Error saving question: {e}")

#             print(f"New question posted: {question_text}")

#             return redirect(url_for('home.unit_page', year_id=year_id, sem_id=sem_id, unit_id=unit_id, unit_name=unit_name))

#     questions = Question.query.filter_by(unit_id=unit_id).all()
#     print(f"Questions for unit {unit_id}: {[q.content for q in questions]}")
#     print(f"Rendering unit page with questions: {questions}")

#     return render_template('unit_page.html', year_id=year_id, sem_id=sem_id, unit_id=unit_id, unit_name=unit_name, questions=questions)

from flask import current_app, flash
from flask import send_from_directory

from app.models import UploadedFile

@home_bp.route('/year/<int:year_id>/semester/<int:sem_id>/unit/<int:unit_id>/<string:unit_name>', methods=['GET', 'POST'])
def unit_page(year_id, sem_id, unit_id, unit_name):
    """
    Display the unit page where users can upload files or post questions.
    """
    if request.method == 'POST':
        question_text = request.form.get('question')
        file = request.files.get('file')

        if file:
            filename = secure_filename(file.filename)

            # Debug: Print the filename and file type
            print(f"File received: {filename}, Content type: {file.content_type}")

            if filename != '':
                file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                try:
                    file.save(file_path)
                    print(f"File saved at: {file_path}")

                    # Save file metadata in the database
                    new_file = UploadedFile(filename=filename, filepath=file_path, unit_id=unit_id)
                    db.session.add(new_file)
                    db.session.commit()

                except Exception as e:
                    print(f"Error saving file: {e}")
                    flash("Error saving file. Please try again.", "danger")
            else:
                print("No filename provided.")
                flash("No filename provided.", "warning")

        if question_text:
            new_question = Question(content=question_text, unit_id=unit_id, user_id=current_user.id)

            try:
                db.session.add(new_question)
                db.session.commit()
                print(f"New question posted: {question_text}")
            except Exception as e:
                db.session.rollback()
                print(f"Error saving question: {e}")

        return redirect(url_for('home.unit_page', year_id=year_id, sem_id=sem_id, unit_id=unit_id, unit_name=unit_name))

    questions = Question.query.filter_by(unit_id=unit_id).all()
    uploaded_files = UploadedFile.query.filter_by(unit_id=unit_id).all()
    return render_template('unit_page.html', year_id=year_id, sem_id=sem_id, unit_id=unit_id, unit_name=unit_name, questions=questions, files=uploaded_files)

@home_bp.route('/uploads/<filename>')
def uploaded_file(filename):
    """
    Serve the uploaded file from the uploads directory.
    """
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)


def get_user_by_id(user_id):
	"""
	Retrieves a user by their ID.

	@param user_id: The ID of the user to retrieve
	@return: The User object if found, or None if not found
	"""
	return User.query.get(user_id)

@home_bp.route('/question/<int:question_id>', methods=['GET', 'POST'])
def question_page(question_id):
    """
    Display the full question with answer input and comment section
    """
    question = Question.query.options(joinedload(Question.user)).get(question_id)
    #question = Question.query.get_or_404(question_id)

    if not question:
        flash('Question not found or has been deleted.', 'warning')
        return redirect(url_for('home.unit_page', year_id=year_id, sem_id=sem_id, unit_id=unit_id, unit_name=unit_name))  # Adjust as necessary for unit_name


    user_id = question.user_id  # or whatever function retrieves the user

    user = get_user_by_id(user_id)  # Now user_id is defined
    if user is None:
        return "User not found", 404

    answers = Answer.query.filter_by(question_id=question_id).all()

    for answer in answers:
        answer.comments = Comment.query.filter_by(answer_id=answer.id).all()
        for comment in answer.comments:
            comment.content = re.sub(
                r'@(\w+)',
                lambda match: f'<a href="{url_for("user.profile", user_id=user.id)}">@{match.group(1)}</a>',
                comment.content
            )
            # Add time formatting here (assuming `comment.created_at` exists)
            comment.time_display = comment.created_at.strftime('%Y-%m-%d %H:%M:%S')

    if request.method == 'POST':
        answer_content = request.form.get('answer')
        if answer_content:
            answer = Answer(content=answer_content,
                            question_id=question_id, user_id=current_user.id)
            db.session.add(answer)
            db.session.commit()
            flash('Your answer has been submitted!', 'success')
            return redirect(url_for('home.question_page', question_id=question_id, user=user))

    answers = Answer.query.filter_by(question_id=question_id).all()

    return render_template('question_page.html', question=question, answers=answers, user=user)
    response = make_response(render_template('question_page.html', question=question, answers=answers, user=user))
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    return response


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

        comment = Comment(content=comment_content,
                          answer_id=answer_id, user_id=current_user.id)
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been posted!', 'success')

    return redirect(url_for('home.question_page', question_id=Answer.query.get_or_404(answer_id).question_id))

@home_bp.route('/comment/<int:question_id>', methods=['POST'])
@login_required
def comments():
    comments = Comment.query.all()

    # Parse tags for each comment's content
    for comment in comments:
        comment.content = parse_tags(comment.content)

    return render_template('comments.html', comments=comments)





@home_bp.route('/delete_question/<int:question_id>', methods=['POST'])
def delete_question(question_id):
    # Fetch the question from the database
    question = Question.query.get(question_id)

    if question is None:
        flash("Question not found")
        return redirect(url_for('home.index'))

    unit = Unit.query.get(question.unit_id)

    if unit is None:
        flash("Associated unit not found", "warning")
        return redirect(url_for('home.index'))

    unit_id = unit.id
    year_id = unit.year_id
    sem_id = unit.semester_id
    unit_name = unit.unit_name
     

    # Delete the question (which will cascade to delete answers and comments)
    db.session.delete(question)
    db.session.commit()

    flash("Question deleted successfully")
    return redirect(url_for('home.unit_page', year_id=year_id, sem_id=sem_id, unit_id=unit_id, unit_name=unit_name))  # Adjust as necessary for unit_name




@home_bp.route('/delete_answer/<int:answer_id>', methods=['POST'])
@login_required
def delete_answer(answer_id):
	"""
	Delete an answer
	"""
	answer = Answer.query.get_or_404(answer_id)

	if answer.user_id != current_user.id:
		flash('You are not authorized to delete this answer', 'danger')
		return redirect(url_for('home.question_page', question_id=answer.question_id))

	db.session.delete(answer)
	db.session.commit()
	flash('Your answer has been deleted', 'success')
	return redirect(url_for('home.question_page', question_id=answer.question_id))


@home_bp.route('/delete_comment/<int:comment_id>', methods=['POST'])
@login_required
def delete_comment(comment_id):
    """
    Delete a comment
    """
    comment = Comment.query.get_or_404(comment_id)
    answer = comment.answer

    if comment.user_id != current_user.id:
        flash('You are not authorized to delete this comment', 'danger')
        return redirect(url_for('home.question_page', question_id=comment.answer.question_id))

    db.session.delete(comment)
    db.session.commit()
    flash('Your comment has been deleted', 'success')
    return redirect(url_for('home.question_page', question_id=comment.answer.question_id))


