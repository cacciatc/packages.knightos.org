from flask import Blueprint, render_template, abort, request, redirect, session, url_for
from flask.ext.login import current_user, login_user, logout_user
from sqlalchemy import desc
from packages.objects import *
from packages.common import *
from packages.config import _cfg
from packages.email import send_confirmation

import binascii
import os
import zipfile
import urllib
import re

html = Blueprint('html', __name__, template_folder='../../templates')

@html.route("/")
def index():
    return render_template("index.html")

@html.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    else:
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        errors = dict()
        if not email:
            errors['email'] = 'Email is required.'
        else:
            if not re.match(r"^[^@]+@[^@]+\.[^@]+$", email):
                errors['email'] = 'Please use a valid email address.'
            if User.query.filter(User.username.ilike(username)).first():
                errors['username'] = 'This username is already in use.'
        if not username:
            errors['username'] = 'Username is required.'
        else:
            if not re.match(r"^[A-Za-z0-9_]+$", username):
                errors['username'] = 'Letters, numbers, underscores only.'
            if len(username) < 3 or len(username) > 24:
                errors['username'] = 'Must be between 3 and 24 characters.'
            if User.query.filter(User.username.ilike(username)).first():
                errors['username'] = 'This username is already in use.'
        if not password:
            errors['password'] = 'Password is required.'
        else:
            if len(password) < 5 or len(password) > 256:
                errors['password'] = 'Must be between 5 and 256 characters.'
        if errors != dict():
            return render_template("register.html", username=username, email=email, errors=errors)
        # All good, create an account for them
        user = User(username, email, password)
        user.confirmation = binascii.b2a_hex(os.urandom(20)).decode("utf-8")
        db.add(user)
        db.commit()
        send_confirmation(user)
        return redirect("/pending")

@html.route("/confirm/<confirmation>")
def confirm(confirmation):
    user = User.query.filter(User.confirmation == confirmation).first()
    if not user:
        return render_template("confirm.html", **{ 'success': False, 'user': user })
    else:
        user.confirmation = None
        login_user(user)
        db.commit()
        return render_template("confirm.html", **{ 'success': True, 'user': user })

@html.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if current_user:
            return redirect("/")
        reset = request.args.get('reset') == '1'
        return render_template("login.html", **{ 'return_to': request.args.get('return_to'), 'reset': reset })
    else:
        username = request.form['username']
        password = request.form['password']
        remember = request.form.get('remember-me')
        if remember == "on":
            remember = True
        else:
            remember = False
        user = User.query.filter(User.username.ilike(username)).first()
        if not user:
            return render_template("login.html", **{ "username": username, "errors": 'Your username or password is incorrect.' })
        if user.confirmation != '' and user.confirmation != None:
            return redirect("/pending")
        if not bcrypt.checkpw(password, user.password):
            return render_template("login.html", **{ "username": username, "errors": 'Your username or password is incorrect.' })
        login_user(user, remember=remember)
        if 'return_to' in request.form and request.form['return_to']:
            return redirect(urllib.parse.unquote(request.form.get('return_to')))
        return redirect("/")

@html.route("/logout")
@loginrequired
def logout():
    logout_user()
    return redirect("/")

@html.route("/pending")
def pending():
    return render_template("pending.html")

@html.route("/help")
def help():
    return render_template("help.html")