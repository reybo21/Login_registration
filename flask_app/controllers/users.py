from flask import Flask, render_template, request, redirect, session
# import the class from user.py
from flask_app.models.user import User
from flask_app import app
from flask_bcrypt import Bcrypt
from flask import flash

bcrypt = Bcrypt(app)
# we are creating an object called bcrypt, 
# which is made by invoking the function Bcrypt with our app as an argument

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/user')
def user_home_page():
    return render_template("user_page.html", name_on_template = session['user_first_name'])

@app.route('/login/process', methods=['POST'])
def login():
    data = { "email" : request.form["email"] }
    user_in_db = User.get_by_email(data)
    # user is not registered in the db
    if not user_in_db:
        flash("Invalid Email/Password")
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        # if we get False after checking the password
        flash("Invalid Email/Password")
        return redirect('/')
    # if the passwords matched, we set the user_id into session
    session['user_first_name'] = user_in_db.first_name
    print (session['user_first_name'])
    # never render on a post!!!
    return redirect("/user")

@app.route('/create_user/process', methods=['POST'])
def create_user():
    print(request.form['email'])
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        "first_name": request.form['first_name'],
        "last_name" : request.form['last_name'],
        "email" : request.form['email'],
        "password" : pw_hash
    }
    if not User.validate_user(data):
         return redirect('/')
    user_id = User.save(data)
    print (User.get_username(user_id)[0]['first_name'])
    session['user_first_name'] = User.get_username(user_id)[0]['first_name']
    print (session['user_first_name'])
    return redirect("/user")

@app.route('/destroy_session', methods=['POST'])
def destroy_session():
    session.clear()
    return redirect('/')
