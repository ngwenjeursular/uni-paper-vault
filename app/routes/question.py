# app/routes/question.py

from flask import render_template, url_for, flash, redirect, request, Blueprint
from app import db
from app.models.question import Question
from flask_login import current_user, login_required

question_bp = Blueprint('question', __name__)

@question_bp.route("/post_question", methods=['GET', 'POST'])
@login_required
def post_question():
	if request.method == 'POST':
		question_text = request.form.get('question')
		if question_text:
			question = Question(question=question_text, user_id=current_user.id)
			db.session.add(question)
			db.session.commit()
			flash('Your question has been posted!', 'success')
			return redirect(url_for('home'))
	return render_template('post_question.html', title='Post Question')
