"""
the home route
"""
from flask import render_template
from flask import Blueprint, render_template


home_bp = Blueprint('home', __name__)

@home_bp.route('/')
@home_bp.route('/home')
def index():
	"""
	Handle the home route
	"""
	return render_template('home.html')

