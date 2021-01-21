from flask import render_template, request, Response, url_for, flash, redirect
from imagerepository import app, bcrypt, db
from imagerepository.models import User, Post, Photo
#Custom flask forms imported for html conversion
from imagerepository.forms import RegistrationForm, LoginForm, AccountUpdateForm, NewPostForm
from flask_login import login_user, current_user, logout_user, login_required
import os
import secrets
from PIL import Image


tags = ["Nature", "Family", "Business", "Travel", "Adventure", "Education", "Art", "Food"]



@app.route('/')
def index():
    return render_template('home.html')

@app.route('/home')
def home():
    #get all public posts
    posts = Post.query.filter(Post.is_private == 0).all()

    #each public post has a list of images
    photos = []
    for single_post in posts:
        photos.append(Photo.query.filter(Photo.post_id == single_post.id).all())

    master_list = list()
    for post_set in photos:
        temp_list = list()
        for single_image in post_set:
            path = "imagedata/postphotos/" + single_image.image_file
            picture_path = url_for('static', filename=path)
            temp_list.append(picture_path)
        master_list.append(temp_list)


    return render_template('home.html', posts=posts, photos=master_list, title="Image Viewer")

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

@login_required
@app.route("/privatelibrary/<post_id>")
def moreinfo(post_id):
    print("POSTID")
    post = Post.query.filter(Post.id==post_id).first()
    photos_to_post = Photo.query.filter(Photo.post_id == post.id).all()

    photos = []
    for photo in photos_to_post:
        path = "imagedata/postphotos/" + photo.image_file
        picture_path = url_for("static", filename=path)
        photos.append(picture_path)

    return render_template("moreinfo.html", title="More Info", images=photos, post=post)



@login_required
@app.route("/privatelibrary")
def privatelibrary():
    default = os.path.join(app.config['UPLOAD_FOLDER'], "250x250.png")
    logo = os.path.join(app.config['UPLOAD_FOLDER'], "PrivateImageRepoLogo.png")

    tags_set = set()


    #get all the posts that user has posted
    posts = Post.query.filter(Post.is_private == 1, Post.user_id == current_user.id).all()


    tag_photo_post = []
    for i in range(len(posts)):
        current_post = posts[i]
        current_tag = current_post.tag
        tags_set.add(current_tag)

        #private_photos contains a list of lists where each list contains a set of photos pertaining to that post
        photos_to_post = Photo.query.filter(Photo.post_id == current_post.id).all()
        for photo in photos_to_post:
            path = "imagedata/postphotos/" + photo.image_file
            picture_path = url_for("static", filename=path)
            tag_photo_post.append((picture_path, current_tag, photo, current_post))

    print(tags_set)
    return render_template("private.html", title="Private", defaultpic=default, logo=logo, data=tag_photo_post, tags_set=tags_set)



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

        #Resize
        output_image_size = (250, 250)
        image = Image.open(form_picture)
        image.thumbnail(output_image_size)

        #Save resized
        image.save(post_picture_path)
        print("IMAGE SIZE: " + str(image.size))

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
    if request.method == "POST":
        if new_post_form.validate_on_submit():

            post = Post(title=new_post_form.title.data, content=new_post_form.description.data, is_private=new_post_form.public_private.data, tag=new_post_form.photo_tag.data, photos_contained=len(new_post_form.images.data), author=current_user)
            db.session.add(post)
            db.session.commit()
            #add all photos to database commit
            order_count = 1
            for single_photo in new_post_form.images.data:
                file_name = save_picture(single_photo, "post")
                new_image = Photo(image_file=file_name, photo_order=order_count, parent=post)
                db.session.add(new_image)
                db.session.commit()
                order_count += 1

            flash("Your post has been created", "success")
            return redirect(url_for("home"))

    return render_template("new_post.html", title="New Post", form=new_post_form)