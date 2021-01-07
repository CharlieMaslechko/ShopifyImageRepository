from flask import Flask, render_template, request, Response, url_for, flash, redirect
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
            return redirect(url_for('home'))

    #Return get request
    return render_template("registration.html", title="Registration", form=registration_form)

@app.route('/login')
def login():
    #Create instance of form
    login_form = LoginForm()
    return render_template("registration.html", title="Login", form=login_form)


