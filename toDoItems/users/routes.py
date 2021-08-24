from flask import Blueprint, redirect, url_for, flash, render_template, request
from flask_login import current_user, login_required, logout_user, login_user
from toDoItems.users.form import RegistrationForm, LoginForm, AccountUpdateForm, RequestResetForm, ResetPasswordForm
from toDoItems.users.utils import save_pic, send_mail
from toDoItems import bcrypt, db
from toDoItems.models import User


users = Blueprint('users', __name__)




@users.route('/register/',methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).\
                    decode('utf-8')
        user = User(fullname = form.fullname.data, username=form.username.data, email=form.email.data, gender=form.gender.data, password=hashed_pw, dob=form.dob.data)
        db.session.add(user)
        db.session.commit()
        flash('You have registered successfully', 'info')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register',form = form)



@users.route('/login/', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next = request.args.get('next')
            flash('You have logged in', 'info')
            return redirect(next) if next else redirect(url_for('main.home'))
        else:
            flash('Either username or password is wrong','warning')
    return render_template('login.html', title='Login', form=form)



@users.route('/logout/')
@login_required
def logout():
    logout_user()
    flash('You have logged out', 'info')
    return redirect(url_for('main.home'))



@users.route('/account/', methods=['GET','POST'])
@login_required
def account():
    form = AccountUpdateForm()
    if form.validate_on_submit():
        if form.picture.data:
            current_user.picture = save_pic(form.picture.data)
        current_user.fullname = form.fullname.data
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account details has been updated','info')
        return redirect(url_for('users.account'))
    if request.method == "GET":
        form.fullname.data = current_user.fullname
        form.username.data = current_user.username
        form.email.data = current_user.email
    pic = url_for('static',filename='Images/'+current_user.picture)
    return render_template('account.html', title='Account', form=form, pic=pic)



@users.route('/reset_password/',methods=['GET','POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_mail(user)
            flash('An email has been sent in entered email address', 'info')
            return redirect(url_for('main.home'))
        else:
            flash('No account with the mentioned email address exist', 'warning')
    return render_template('request.html', title='Reset Password Request', form=form)



@users.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('This is either an invalid or expired url', 'warning')
        return redirect(url_for('main.home'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_pw
        db.session.commit()
        flash('Your password has been updated, now you are able to login','info')
        return redirect(url_for('users.login'))
    return render_template('resetPassword.html', title='Reset Password', form=form)