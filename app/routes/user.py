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
            #print("User found!")
            if check_password_hash(user.password, form.password.data):
                #print("Password is correct!")
                login_user(user, remember=True)
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('home.index'))
            else:
                print("Password is incorrect.")
        """
        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=True)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('user.home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
        """
        
    else:
        print("Form errors:", form.errors)
    
    return render_template('login.html', title='Login', form=form)


@user_bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home.index'))

@user_bp.route('/profile')
@login_required
def profile():
    return render_template('profile.html', title='My Profile')

