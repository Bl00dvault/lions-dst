from blueprints.models import db, User
from flask import Blueprint, request, render_template, json, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user


users_blueprint = Blueprint('user', __name__)

@users_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user is None or not user.check_password(password):
            return "Invalid username or password"

        login_user(user)  # Log in the user
        return redirect(url_for('home'))

    else:
        return render_template('login.html')

@users_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('user.login'))

@users_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        is_admin = 'is_admin' in request.form

        if is_admin:
            if not current_user.is_admin:
                return "Unauthorized", 403
            else:
                user = User(username=username)
                user.set_password(password)
                user.is_admin = is_admin

                db.session.add(user)
                db.session.commit()
        else:
            user = User(username=username)
            user.set_password(password)

            db.session.add(user)
            db.session.commit()

        return redirect(url_for('user.login'))
    else:
        return render_template('register.html')

@users_blueprint.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    if request.method == 'POST':
        current_password = request.form['current_password']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']

        if not current_user.check_password(current_password):
            return "Incorrect current password"

        if new_password != confirm_password:
            return "New password and confirmation password do not match"

        current_user.set_password(new_password)
        db.session.commit()
        
        return redirect(url_for('home'))

    else:
        return render_template('change_password.html')

@users_blueprint.route('/user_management', methods=['GET', 'POST'])
@login_required
def user_management():
    if not current_user.is_admin:
        return "Unauthorized", 403

    if request.method == 'POST':
        if 'delete_user_id' in request.form:
            delete_user_id = request.form['delete_user_id']
            # prevent deleting own account
            if str(current_user.id) == delete_user_id:
                return "Error: You can't delete your own account", 400
            # prevent deleting 'admin' account
            elif delete_user_id == "1":
                return "Error: You can't delete the 'admin' account", 400
            else:
                User.query.filter_by(id=delete_user_id).delete()
                db.session.commit()

        elif 'make_admin_id' in request.form:
            make_admin_id = request.form['make_admin_id']
            user = User.query.get(make_admin_id)
            user.is_admin = True
            db.session.commit()

        else:
            user_id = request.form['user_id']
            new_password = request.form['new_password']
            user = User.query.get(user_id)
            user.set_password(new_password)
            db.session.commit()
            
    users = User.query.all()
    return render_template('user_management.html', users=users)

