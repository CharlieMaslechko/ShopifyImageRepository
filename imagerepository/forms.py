from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import BooleanField, StringField, SubmitField, PasswordField, TextAreaField, MultipleFileField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from imagerepository import db
from imagerepository.models import User
from flask_login import current_user


#Form used when a user wants to sign up to the shopify image repo
class RegistrationForm(FlaskForm):

    #Username restrictions: Must be non empty between 3 and 15 characters
    username = StringField("Username", validators=[DataRequired(), Length(min=3, max=15)])
    #Email restrictions: Must be non empty and valid email
    email = StringField("Email", validators=[DataRequired(), Email()])
    #Password restrictions: Must be non empty
    password = PasswordField("Password", validators=[DataRequired()])
    #Confirm Password restrictions: Must be non empty and matches password field
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField("Sign up!")

    #Validate username is not taken
    def validate_username(self, username):
        check_user = User.query.filter_by(username=username.data).first()
        if check_user:
            raise ValidationError("That username has already been taken. Please choose a different username")

    #validate email is not taken
    def validate_email(self, email):
        check_user = User.query.filter_by(email=email.data).first()
        if check_user:
            raise ValidationError("That email already has an account registered. Please select a different email")

#Form used when a user wants to sign up to the shopify image repo
class AccountUpdateForm(FlaskForm):

    #Username restrictions: Must be non empty between 3 and 15 characters
    username = StringField("Username", validators=[DataRequired(), Length(min=3, max=15)])
    #Email restrictions: Must be non empty and valid email
    email = StringField("Email", validators=[DataRequired(), Email()])
    #Profile picture restrictions: Must be png or jpg
    profile_picture = FileField("Update Profile Picture", validators=[FileAllowed(["png", "jpeg"])])
    submit = SubmitField("Update account")

    #Validate username is not taken
    def validate_username(self, username):
        #Perform check only if changed
        if current_user.username != username.data:
            check_user = User.query.filter_by(username=username.data).first()
            if check_user:
                raise ValidationError("That username has already been taken. Please choose a different username")

    #validate email is not taken
    def validate_email(self, email):
        #perform check only if changed
        if current_user.email != email.data:
            check_user = User.query.filter_by(email=email.data).first()
            if check_user:
                raise ValidationError("That email already has an account registered. Please select a different email")


#Form used when a user wants to login with an existing account
class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    #Use cookie to store
    remember = BooleanField("Remember me next time")
    submit = SubmitField("Login")


class NewPostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    images = MultipleFileField("Upload Photo", validators=[FileAllowed(["png", "jpeg"])])
    description = TextAreaField("Photo Description", validators=[DataRequired()])
    photo_tag = SelectField("Tags", choices=["Nature", "Family", "Business", "Travel", "Adventure", "Education", "Art", "Food"])

    public_private = BooleanField("Private")

    submit = SubmitField("Post")






