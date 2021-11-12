from base import *
from threading import Thread

def send_password_reset_email(user, token):
    msg = Message()
    msg.subject = "Flask App Password Reset"
    msg.sender = app.config['MAIL_USERNAME']
    msg.recipients = [user.email]
    msg.html = render_template('email/reset_password_email.html',
                                user=user, 
                                link=url_for('reset_password_token', token=token, _external=True))
    mail.send(msg)