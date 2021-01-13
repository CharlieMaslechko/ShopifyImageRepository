from flask import render_template, request, Response, url_for, flash, redirect
from imagerepository import app, bcrypt, db
from imagerepository.models import User, Post, Photo
#Custom flask forms imported for html conversion
from imagerepository.forms import RegistrationForm, LoginForm, AccountUpdateForm, NewPostForm
from flask_login import login_user, current_user, logout_user, login_required
import os
import secrets
from PIL import Image

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

@app.route("/about")
def about():
    return render_template("about.html", title="About")



#helper function for saving picture returns file name
def save_picture(form_picture, type):

    #encode file name as random 8 byte hex
    generate_random = secrets.token_hex(8)
    #obtain file extension user uploaded with
    file_name, file_extension = os.path.splitext(form_picture.filename)
    #concat file name
    picture_file_name = generate_random + file_extension

    if type == "profile":
        #obtain path to folder
        profile_picture_path = os.path.join(app.root_path, "static/imagedata/profilepictures", picture_file_name)

        #Resize
        output_image_size = (125, 125)
        image = Image.open(form_picture)
        image.thumbnail(output_image_size)

        #Save resized
        image.save(profile_picture_path)

    if type == "post":
        #obtain path to folder
        post_picture_path = os.path.join(app.root_path, "static/imagedata/postphotos", picture_file_name)
        image = Image.open(form_picture)
        image.save(post_picture_path)

    return picture_file_name

@app.route("/account", methods=["POST", "GET"])
#Requires login to access route
@login_required
def account():
    path = "imagedata/profilepictures/" + current_user.image_file
    profile_pic = url_for('static', filename=path)
    #Create instance of form
    update_form = AccountUpdateForm()

    if request.method == "POST":
        if update_form.validate_on_submit():
            if update_form.profile_picture.data:
                file_name = save_picture(update_form.profile_picture.data, "profile")
                current_user.image_file = file_name
                db.session.commit()
            current_user.username = update_form.username.data
            current_user.email = update_form.email.data
            db.session.commit()
            flash("Account information succesfully updated", "success")
            return redirect(url_for("account"))
    elif request.method == "GET":
        update_form.username.data = current_user.username
        update_form.email.data = current_user.email

    return render_template('account.html', title="Account", form=update_form, profile_picture=profile_pic)


@app.route("/post/new", methods=["POST", "GET"])
@login_required
def new_post():
    new_post_form = NewPostForm()
    print(request.method)
    if request.method == "POST":
        if new_post_form.validate_on_submit():
            post = Post(title=new_post_form.title.data, content=new_post_form.description.data, is_private=new_post_form.public_private.data, author=current_user)
            db.session.add(post)
            db.session.commit()
            #add all photos to database commit
            order_count = 0
            for single_photo in new_post_form.images.data:
                file_name = save_picture(single_photo, "post")
                new_image = Photo(image_file=file_name, photo_order=order_count, parent=post)
                db.session.add(new_image)
                db.session.commit()
                order_count += 1

            flash("Your post has been created", "success")
            return redirect(url_for("home"))

    return render_template("new_post.html", title="New Post", form=new_post_form)