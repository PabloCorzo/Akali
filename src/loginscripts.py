from flask import Flask,render_template,request,flash, session,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from app import Users

def login(app : Flask,request,session):
    if request.method == 'Post':
        username = request.form['username']
        password = request.form['password']
        # email = request.form['email']

        user = Users.query.filter_by(username = username).first()
        if user and user.checkPassword(password):
            session['username'] = user.username
            # session['email'] = user.email
            session['id'] = user._id
            return redirect(url_for('dashboard'))
        else:
            return render_template("login.html",error = "Invalid user")
    else:
        return render_template('login.html')
    
def register(app : Flask,request,db : SQLAlchemy):
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        if email is None:
            email = ""
        user = Users.query.filter_by(username = username).first()
        if user:
            return render_template('index.html',error = 'user already registered')
        else:
            user = Users(username = username, password = password, email = email)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('dashboard'))
    return render_template('index.html')

def logout(app : Flask, request, session):
    session['id'] = None
    session['username'] = None
    return redirect(url_for('/'))