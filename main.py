# imports from flask
import json
import os
import shutil
from urllib.parse import urljoin, urlparse
from flask import abort, redirect, render_template, request, send_from_directory, url_for, jsonify, current_app
from flask_login import current_user, login_user, logout_user, login_required
from flask.cli import AppGroup
from werkzeug.security import generate_password_hash

# Flask app setup
from __init__ import app, db, login_manager

# CORS for frontend running on a different port
from flask_cors import CORS
CORS(app, supports_credentials=True, origins=["http://127.0.0.1:4504"])

# API imports (teammate + yours)
from api.user import user_api
from api.pfp import pfp_api
from api.nestImg import nestImg_api
from api.post import post_api
from api.channel import channel_api
from api.group import group_api
from api.section import section_api
from api.student import student_api
from api.nestPost import nestPost_api
from api.messages_api import messages_api
from api.questions import questions_api
from api.scoreboard import scoreboard_api
from api.vote import vote_api
from api.resource import resource_api
from api.illumina import illumina_api
from api.dna_sequencing import dna_api
from api.chatbot import chatbot_api
from api.dnabot import dnabot_api
from api.college import college_api  # <-- added line

# Register all blueprints
app.register_blueprint(user_api)
app.register_blueprint(pfp_api)
app.register_blueprint(nestImg_api)
app.register_blueprint(post_api)
app.register_blueprint(channel_api)
app.register_blueprint(group_api)
app.register_blueprint(section_api)
app.register_blueprint(student_api)
app.register_blueprint(nestPost_api)
app.register_blueprint(messages_api)
app.register_blueprint(questions_api)
app.register_blueprint(scoreboard_api)
app.register_blueprint(vote_api)
app.register_blueprint(resource_api)
app.register_blueprint(illumina_api)
app.register_blueprint(dna_api)
app.register_blueprint(chatbot_api)
app.register_blueprint(dnabot_api)
app.register_blueprint(college_api)  # <-- added line

# Login Manager
login_manager.login_view = "login"

@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect(url_for('login', next=request.path))

@login_manager.user_loader
def load_user(user_id):
    from model.user import User
    return User.query.get(int(user_id))

@app.context_processor
def inject_user():
    return dict(current_user=current_user)

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc

@app.route('/login', methods=['GET', 'POST'])
def login():
    from model.user import User
    error = None
    next_page = request.args.get('next', '') or request.form.get('next', '')
    if request.method == 'POST':
        user = User.query.filter_by(_uid=request.form['username']).first()
        if user and user.is_password(request.form['password']):
            login_user(user)
            if not is_safe_url(next_page):
                return abort(400)
            return redirect(next_page or url_for('index'))
        else:
            error = 'Invalid username or password.'
    return render_template("login.html", error=error, next=next_page)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/')
def index():
    print("Home:", current_user)
    return render_template("index.html")

@app.route('/users/table')
@login_required
def utable():
    from model.user import User
    users = User.query.all()
    return render_template("utable.html", user_data=users)

@app.route('/users/table2')
@login_required
def u2table():
    from model.user import User
    users = User.query.all()
    return render_template("u2table.html", user_data=users)

@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)

@app.route('/users/delete/<int:user_id>', methods=['DELETE'])
@login_required
def delete_user(user_id):
    from model.user import User
    user = User.query.get(user_id)
    if user:
        user.delete()
        return jsonify({'message': 'User deleted successfully'}), 200
    return jsonify({'error': 'User not found'}), 404

@app.route('/users/reset_password/<int:user_id>', methods=['POST'])
@login_required
def reset_password(user_id):
    from model.user import User
    if current_user.role != 'Admin':
        return jsonify({'error': 'Unauthorized'}), 403
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    if user.update({"password": app.config['DEFAULT_PASSWORD']}):
        return jsonify({'message': 'Password reset successfully'}), 200
    return jsonify({'error': 'Password reset failed'}), 500

# CLI Setup
custom_cli = AppGroup('custom', help='Custom commands')

@custom_cli.command('generate_data')
def generate_data():
    from model.user import initUsers
    from model.section import initSections
    from model.group import initGroups
    from model.channel import initChannels
    from model.post import initPosts
    from model.nestPost import initNestPosts
    from model.vote import initVotes
    initUsers()
    initSections()
    initGroups()
    initChannels()
    initPosts()
    initNestPosts()
    initVotes()

@custom_cli.command('backup_data')
def backup_data():
    data = extract_data()
    save_data_to_json(data)
    backup_database(app.config['SQLALCHEMY_DATABASE_URI'], app.config['SQLALCHEMY_BACKUP_URI'])

@custom_cli.command('restore_data')
def restore_data_command():
    data = load_data_from_json()
    restore_data(data)

app.cli.add_command(custom_cli)

# DB helpers
def extract_data():
    from model.user import User
    from model.section import Section
    from model.group import Group
    from model.channel import Channel
    from model.post import Post
    data = {}
    with app.app_context():
        data['users'] = [user.read() for user in User.query.all()]
        data['sections'] = [section.read() for section in Section.query.all()]
        data['groups'] = [group.read() for group in Group.query.all()]
        data['channels'] = [channel.read() for channel in Channel.query.all()]
        data['posts'] = [post.read() for post in Post.query.all()]
    return data

def save_data_to_json(data, directory='backup'):
    if not os.path.exists(directory):
        os.makedirs(directory)
    for table, records in data.items():
        with open(os.path.join(directory, f'{table}.json'), 'w') as f:
            json.dump(records, f)
    print(f"Data backed up to {directory} directory.")

def load_data_from_json(directory='backup'):
    data = {}
    for table in ['users', 'sections', 'groups', 'channels']:
        with open(os.path.join(directory, f'{table}.json'), 'r') as f:
            data[table] = json.load(f)
    return data

def restore_data(data):
    from model.user import User
    from model.section import Section
    from model.group import Group
    from model.channel import Channel
    with app.app_context():
        users = User.restore(data['users'])
        _ = Section.restore(data['sections'])
        _ = Group.restore(data['groups'], users)
        _ = Channel.restore(data['channels'])
    print("Data restored to the new database.")

def backup_database(src_uri, backup_uri):
    if src_uri.startswith("sqlite:///") and backup_uri.startswith("sqlite:///"):
        src_path = src_uri.replace("sqlite:///", "")
        backup_path = backup_uri.replace("sqlite:///", "")
        try:
            shutil.copy2(src_path, backup_path)
            print("Database file copied successfully.")
        except Exception as e:
            print("Error backing up database file:", e)

# Run Flask on port 8504
if __name__ == "__main__":
    app.run(debug=True, port=8504)
