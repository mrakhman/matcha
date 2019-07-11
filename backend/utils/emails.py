from flask import session, g, abort, jsonify

from models.user import User
from flask_mail import Message
from mail import mail

# from app import app
from itsdangerous import URLSafeTimedSerializer

LOCAL_URL = "http://localhost:8080"


def send_email(to_email, subject, message):
    msg = Message(subject=subject, sender="matcha@coffeebreak42.cf", recipients=[to_email])
    msg.body = message
    mail.send(msg)
    return True


def send_activation_email(to, token):
    subject = "Matcha - confirm your email"
    message = "Welcome to Matcha! Click the link to verify your email: " \
              + LOCAL_URL + "/activation/" + token
    if send_email(to, subject, message):
        return jsonify({"ok": True})
    return jsonify({"ok": False})


def send_passreset_email(to, token):
    subject = "Matcha - forgot password"
    message = "Click the link to reset your password: " \
              + LOCAL_URL + "/reset_password/" + token
    if send_email(to, subject, message):
        return jsonify({"ok": True})
    return jsonify({"ok": False})


def send_newemail_email(to, token):
    subject = "Matcha - change your email"
    message = "Click the link to change your email: " \
              + LOCAL_URL + "/new_email/" + token
    if send_email(to, subject, message):
        return jsonify({"ok": True})
    return jsonify({"ok": False})


# TODO: app.config import
# salt=app.config['SECURITY_SALT']
# app.config['SECRET_KEY']


def generate_activation_token(email):
    serializer = URLSafeTimedSerializer('secret-key')
    return serializer.dumps(email, salt='salt')


def confirm_token(token, expiration=3600*2):
    serializer = URLSafeTimedSerializer('secret-key')
    try:
        email = serializer.loads(token, salt='salt', max_age=expiration)
    except:
        return False
    return email