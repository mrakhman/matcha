import smtplib

from flask_mail import Message

from modules import mail


def send_email(to_email, subject, message):
    msg = Message(subject=subject, recipients=[to_email])
    msg.body = message
    try:
        mail.send(msg)
    except smtplib.SMTPException:
        return False
    return True


def send_token_email(front_url, token_type, to, token):
    data = {
        'activate_user': {
            'subject': 'Matcha - confirm your email',
            'message': f'Welcome to Matcha! Click the link to verify your email: {front_url}/activation/{token}'
        },
        'activate_email': {
            'subject': 'Matcha - change your email',
            'message': f'Click the link to change your email: {front_url}/activate_email/{token}'
        },
        'reset_pwd': {
            'subject': 'Matcha - forgot password',
            'message': f'Click the link to reset your password: {front_url}/reset_password/{token}'
        }
    }
    return send_email(to, **data[token_type])
