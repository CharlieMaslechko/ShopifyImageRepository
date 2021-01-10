from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length, Email, EqualTo


#Form used when a user wants to sign up to the shopify image repo
class RegistrationForm(FlaskForm):

    #Username is field in HTML
    #Username restrictions: Must be non empty between 3 and 15 characters
    username = StringField("Username", validators=[DataRequired(), Length(min=3, max=15)])
    #Email restrictions: Must be non empty and valid email
    email = StringField("Email", validators=[DataRequired(), Email()])
    #Password restrictions: Must be non empty
    password = PasswordField("Password", validators=[DataRequired()])
    #Confirm Password restrictions: Must be non empty and matches password field
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField("Sign up!")

#Form used when a user wants to login with an existing account
class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    #Use cookie to store
    remember = BooleanField("Remember me next time")
    submit = SubmitField("Login")





