from datetime import datetime
from flask import render_template, flash, redirect, url_for, request
from flask_login import logout_user, login_required, current_user, login_user
from werkzeug.urls import url_parse
from chat import app, db, socketio
from chat.forms import ResetPasswordRequestForm, ResetPasswordForm, LoginForm, RegistrationForm, MessageSubmitForm
from chat.models import User, Message
from chat.email import send_password_reset_email
import sqlalchemy as sa

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@app.route('/')
@app.route('/index')
@login_required
def index():
    if current_user.is_authenticated:
        return redirect(url_for('chat'))
    else:
        return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('chat'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))

        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('chat')
        return redirect(next_page)

    return render_template('login.html', title='Sign In', form=form)


@app.route('/chat', methods=['GET', 'POST'])
def chat():
    query = sa.select([
        User,
    ]
    ).select_from(
        sa.join(
            User, Message,
            User.id == Message.user_id
        )
    ).where(
        Message.deleted == False
    ).group_by(
        User.id
    ).order_by(
        sa.func.count(Message.id).desc()
    ).limit(5).alias(
        'inner'
    )
    active5users = db.session.query(query)
    messages = Message.query.filter(Message.deleted==False)
    form = MessageSubmitForm()
    return render_template('chat.html',
                           title='Chat',
                           form=form,
                           active5users=active5users,
                           messages=messages
                           )


@app.route('/message/<id>')
def message_delete(id):
    message_to_delete = Message.query.get(id)
    message_to_delete.delete()
    db.session.commit()
    return redirect('chat')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@socketio.on('register')
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():

    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check your email for the instructions to reset your password')
        return redirect(url_for('login'))
    return render_template('reset_password_request.html',
                           title='Reset Password', form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)


def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')


@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    if json.get('message') is not None:
        message = Message(
            text=json.get('message'),
            user_id=current_user.id
        )
        message = message.validate()
        json.update({'username': current_user.username})
        db.session.add(message)
        db.session.commit()
    print('received my event: ' + str(json))
    socketio.emit('my response', json, callback=messageReceived)


@socketio.on('user joined')
def user_joined():
    if current_user.is_authenticated:

        socketio.emit('enter chat',
                      {'message': '{0} has joined'.format(current_user.username)},
                      broadcast=True)

    else:
        return False
