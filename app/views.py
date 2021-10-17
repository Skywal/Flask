from app import app
from flask import render_template, request, redirect, url_for, flash, make_response, session


@app.route('/')
def index():
    #return render_template('index.html', name='Jerry')
    return render_template('index.html')


@app.route('/admin/')
#@login_required # pip install flask-login 
def admin():
     return render_template('admin.html')

@app.route('/hello')
def hello():
    return 'Hello, World'

@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return f'User {escape(username)}'

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return f'Post {post_id}'

@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    # show the subpath after /path/
    return f'Subpath {escape(subpath)}'