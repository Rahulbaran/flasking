import os
import secrets
from flask import url_for, current_app
from flask_mail import Message
from toDoItems import mail


# FUNCTION TO SAVE PICTURE
def save_pic(pic):
    random_hex = secrets.token_hex(8)
    _, ext = os.path.splitext(pic.filename)
    modified_pic = random_hex + ext
    path = os.path.join(current_app.root_path, 'static', 'Images', modified_pic)
    pic.save(path)
    return modified_pic


def send_mail(user):
    token = user.get_reset_token()
    msg = Message('Reset Password', recipients = [user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('users.reset_password', token=token, _external=True)}

If you did not make the request then simply ignore it , no change will be made in your account'''
    mail.send(msg)