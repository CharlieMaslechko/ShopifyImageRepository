from flask import Flask, render_template, request, Response, url_for, flash, redirect
import os
#Custom flask forms imported for html conversion
from forms import RegistrationForm, LoginForm

app = Flask(__name__, template_folder='htmltemplates')

#Create a secret key
#Need to make this environment variable
app.config['SECRET_KEY'] = "3E4F4BC7CCE783E799A9628BBCD39"

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

imageFolder = os.path.join("static", "imagedata")
app.config['UPLOAD_FOLDER'] = imageFolder

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/home')
def home():
    return render_template('home.html', posts=posts, title="Image Viewer")

@app.route('/registration', methods=['POST','GET'])
def registration():
    #Create instance of form
    registration_form = RegistrationForm()
    if request.method == "POST":
        if registration_form.validate_on_submit() == True:
            flash("Succesfully created account for " + str(registration_form.username.data), "success")
            return redirect(url_for("home"))

    #Return GET request
    return render_template("registration.html", title="Registration", form=registration_form)

@app.route('/login', methods=['POST','GET'])
def login():
    logo = os.path.join(app.config['UPLOAD_FOLDER'], "ImageRepoLogin.png")
    #Create instance of form
    login_form = LoginForm()
    if request.method == "POST":
        if login_form.validate_on_submit() == True:
            if login_form.email.data == "admin@test.com" and login_form.password.data == "pass":
                flash("You have been succesfully logged in!", "success")
                return redirect(url_for("home"))
            else:
                flash("Failed login attempt. Please make sure username and password are correct", "danger")

    #return GET request
    return render_template("login.html", title="Login", form=login_form, image=logo)






