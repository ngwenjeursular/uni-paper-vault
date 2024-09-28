# app/routes/question.py

from flask import render_template, url_for, flash, redirect, request, Blueprint
from app import db
from app.models.question import Question
from flask_login import current_user, login_required

question_bp = Blueprint('question', __name__)




@question_bp.route('/post_question/<int:unit_id>', methods=['GET', 'POST'])
@login_required
def post_question(unit_id):
    if request.method == 'POST':
        # Handle form submission and save the question
        question_content = request.form['content']
        new_question = Question(content=question_content, unit_id=unit_id)
        db.session.add(new_question)
        db.session.commit()
        return redirect(url_for('unit_page', unit_id=unit_id))
    print(f"Unit ID: {unit_id}")


    return render_template('post_question.html', unit_id=unit_id)

