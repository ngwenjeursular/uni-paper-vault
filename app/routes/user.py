from flask import render_template, url_for, flash, redirect, request, Blueprint
from app import db
from app.forms.login import RegistrationForm, LoginForm
from flask_login import login_user, logout_user, current_user, login_required, login_manager
from app.models import User
from werkzeug.security import  check_password_hash, generate_password_hash


user_bp = Blueprint('user', __name__)


@user_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        flash("You're logged in")
        return redirect(url_for('home.index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()

        flash('Your account has been created :), please log in')
        return redirect(url_for('user.login'))
    
    return render_template('register.html', title='Register', form=form)

@user_bp.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home.index'))

    form = LoginForm()
    if form.validate_on_submit():
        print("Form is valid!")
        user = User.query.filter_by(email=form.email.data).first()
    
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=True)
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('home.index'))
            else:
                print("Password is incorrect.")
        
    else:
        print("Form errors:", form.errors)
    
    return render_template('login.html', title='Login', form=form)


@user_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home.index'))


# @user_bp.route('/profile/<username>')
# def profile(username):
#     user = User.query.filter_by(username=username).first_or_404()
#     # Fetch saved answers, questions, etc. based on the user
#     #saved_answers = Answer.query.filter_by(user_id=user.id).all()
#     #posted_questions = Question.query.filter_by(user_id=user.id).all()
#     #return render_template('profile.html', user=user, saved_answers=saved_answers, posted_questions=posted_questions)
#     return render_template('profile.html', user=user)

def get_user_by_id(user_id):
	"""
	Retrieves a user by their ID.

	@param user_id: The ID of the user to retrieve
	@return: The User object if found, or None if not found
	"""
	return User.query.get(user_id)


@user_bp.route('/profile/<int:user_id>')
def profile(user_id):
	"""
	Renders the profile page for a specific user by their user_id.
	
	@param user_id: The ID of the user
	@return: Rendered profile page or error message
	"""
	user = get_user_by_id(user_id)  # Use the passed user_id here
	if user is None:
		return "User not found", 404
	return render_template('profile.html', user=user)


from flask import request, current_app
import os
from werkzeug.utils import secure_filename

@user_bp.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part', 400
    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        
        # Debugging logs
        print(f"Attempting to save file to: {file_path}")
        
        try:
            file.save(file_path)
            print(f"File saved at: {file_path}")
            return 'File successfully uploaded', 200
        except Exception as e:
            print(f"Error saving file: {e}")
            return 'Error saving file', 500
