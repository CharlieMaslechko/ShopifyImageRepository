from flask import render_template, request, Response, url_for, flash, redirect
from imagerepository import app, bcrypt, db
from imagerepository.models import User, Post
#Custom flask forms imported for html conversion
from imagerepository.forms import RegistrationForm, LoginForm
from flask_login import login_user, current_user, logout_user, login_required
import os

posts = [
    #Example 1
    {
        "author": "Jane Doe",
        "title": "Blog post 1",
        "content": "First post content",
        "date_posted": "April, 21, 2020"
    },
    #Example 2
    {
        "author": "Mark Smith",
        "title": "Blog post 2",
        "content": "Second post content",
        "date_posted": "April, 21, 2021"
    }
]


@app.route('/')
def index():
    return render_template('home.html')

@app.route('/home')
def home():
    return render_template('home.html', posts=posts, title="Image Viewer")

@app.route('/registration', methods=['POST','GET'])
def registration():
    #If user already logged in redirect to homepage
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    #Create instance of form
    registration_form = RegistrationForm()
    if request.method == "POST":
        if registration_form.validate_on_submit() == True:
            #generate hashed password
            password_hash = bcrypt.generate_password_hash(registration_form.password.data)
            #create new user model
            new_user = User(username=registration_form.username.data, email=registration_form.email.data, password=password_hash)
            db.session.add(new_user)
            db.session.commit()

            flash("Succesfully created account for " + str(registration_form.username.data), "success")
            return redirect(url_for("login"))

    #Return GET request
    return render_template("registration.html", title="Registration", form=registration_form)

@app.route('/login', methods=['POST','GET'])
def login():
    #If user already logged in redirect to homepage
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    logo = os.path.join(app.config['UPLOAD_FOLDER'], "ImageRepoLogin.png")
    #Create instance of form
    login_form = LoginForm()
    if request.method == "POST":
        if login_form.validate_on_submit() == True:
            check_user = User.query.filter_by(email=login_form.email.data).first()
            if check_user and bcrypt.check_password_hash(check_user.password, login_form.password.data):
                login_user(check_user, remember=login_form.remember.data)
                return redirect(url_for("home"))
            else:
                flash("Failed login attempt. Please make sure username and password are correct", "danger")

    #return GET request
    return render_template("login.html", title="Login", form=login_form, image=logo)

@app.route("/logout")
def logout():
    flash(str(current_user.username) + " has been logged out", "success")
    logout_user()
    return redirect((url_for("login")))

@app.route("/account")
#Requires login to access route
@login_required
def account():
    path = "imagedata/profilepictures/" + current_user.image_file
    profile_pic = url_for('static', filename=path)
    return render_template('account.html', title="Account", profile_picture=profile_pic)