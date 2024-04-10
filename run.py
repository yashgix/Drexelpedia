from flask import (Flask, g, jsonify, redirect, render_template, request, session)
from passlib.hash import pbkdf2_sha256
import datetime
import json
import subprocess

from db import Database

DATABASE_PATH = 'drexelpedia.db'

app = Flask(__name__)
app.secret_key = b'drexelpedia-secret'


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = Database(DATABASE_PATH)
    return db


@app.teardown_appcontext
def close_db(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route('/')
def home():
    return render_template('article_list.html', title="Recently updated", route="get_recent")


@app.route('/api/get_recent', methods=['GET'])
def api_get_recent():
    return get_db().get_recent()


@app.route('/api/get_contributor_info/<int:article_id>', methods=['GET'])
def api_get_contributor_info(article_id):
    return get_db().get_contributor_info(article_id)


@app.route('/api/search/<string:term>')
def api_search(term):
    return get_db().get_article(1)


@app.route('/search/<string:term>', methods=['GET'])
def search(term):
    return render_template('article_list.html', title=f'Search results for term "{term}"', route=f'/api/search/{term}')


@app.route('/api/upvote/<int:article_id>', methods=['POST'])
def api_upvote(article_id):
    if 'user' in session:
        get_db().apply_vote(article_id, +1)
        return jsonify(success=True)
    else:
        return jsonify(success=False)


@app.route('/api/downvote/<int:article_id>', methods=['POST'])
def api_downvote(article_id):
    if 'user' in session:
        get_db().apply_vote(article_id, -1)
        return jsonify(success=True)
    else:
        return jsonify(success=False)


@app.route('/create_article', methods=['GET', 'POST'])
def create_article():
    return edit_article(0)


@app.route('/edit_article/<int:article_id>', methods=['GET', 'POST'])
def edit_article(article_id):
    if article_id == 0:
        article = {'title': '', 'content': ''}
    else:
        article = get_db().get_raw(article_id)
    return render_template('edit_article.html', title='Edit article', article_title=article['title'], content=json.dumps(article['content'])[1:-1])


def hyperlink_profile(username):
    return f'<a href="/profile/{username}">{username}</a>'


def link_contributor_modal(contributors, article_id):
    return f'<a href="#" onclick="showContributorModal({article_id});">{len(contributors) - 1} other contributors</a>'


@app.route('/article/<int:article_id>')
def article(article_id):
    contributor_info = get_db().get_contributor_info(article_id)
    contributor_info_message = f'By {hyperlink_profile(contributor_info[0]["modifying_username"])}'
    if len(contributor_info) == 2:
        contributor_info_message += f' and {hyperlink_profile(contributor_info[1]["modifying_username"])}'
    elif len(contributor_info) > 2:
        contributor_info_message += ' and ' + link_contributor_modal(contributor_info, article_id)
    return render_template('article.html', **get_db().get_article(article_id), contributor_info_message=contributor_info_message)


@app.route('/api/articles_by/<string:username>')
def api_articles_by(username):
    return get_db().get_articles_by(username)


@app.route('/profile/<string:username>')
def profile(username):
    if username == "":
        return profile(session['user']['username'])
    return render_template('article_list.html', title=f"Articles modified by {username}", route='/articles_by/' + username)


@app.route('/random')
def random():
    return article(get_db().get_num_articles())


@app.route('/welcome')
def welcome():
    return render_template("welcome.html")


"""
@app.route('/api/my_goats', methods=['GET'])
def api_my_goats():
    if 'user' in session:
        return generate_my_goats_response(request.args)
    else:
        return jsonify('Error: User not authenticated')
"""


@app.route('/writearticle', methods=['POST'])
def writearticle():
    subprocess.run("dev/examplewrite.sh")
    return jsonify(success=True)


@app.route('/create_user', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        username = request.form.get('username')
        # email = request.form.get('email')
        typed_password = request.form.get('password')
        if username and typed_password:
            encrypted_password = pbkdf2_sha256.hash(typed_password)
            get_db().create_user(username, encrypted_password)
            return redirect('/login')
    return render_template('create_user.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    message = None
    if request.method == 'POST':
        username = request.form.get('username')
        typed_password = request.form.get('password')
        if username and typed_password:
            user = get_db().get_user(username)
            if user:
                if pbkdf2_sha256.verify(typed_password, user['encrypted_password']):
                    session['user'] = user
                    return redirect('/')
                else:
                    message = "Incorrect password, please try again"
            else:
                message = "Unknown user, please try again"
        elif username and not typed_password:
            message = "Missing password, please try again"
        elif not username and typed_password:
            message = "Missing username, please try again"
    return render_template('login.html', message=message)


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')


if __name__ == '__main__':
    app.run(host='192.168.1.194', port=8080, debug=True)
