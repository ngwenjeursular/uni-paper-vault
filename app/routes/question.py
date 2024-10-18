# app/routes/question.py

from flask import render_template, url_for, flash, redirect, request, Blueprint
from app import db
from app.models.question import Question
from flask_login import current_user, login_required

question_bp = Blueprint('question', __name__)


@question_bp.route('/post_question', methods=['POST'])
@login_required
def post_question():
    title = request.form.get('title')
    content = request.form.get('content')
    new_question = Question(title=title, content=content, user_id=current_user.id)
    db.session.add(new_question)
    db.session.commit()
    return redirect(url_for('home.unit_page', unit_id=new_question.unit_id))
