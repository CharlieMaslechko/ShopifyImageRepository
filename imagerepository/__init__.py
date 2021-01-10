from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_bcrypt import Bcrypt

app = Flask(__name__, template_folder='htmltemplates')

imageFolder = os.path.join("static", "imagedata")

#Create a secret key
#Need to make this environment variable
app.config['SECRET_KEY'] = "3E4F4BC7CCE783E799A9628BBCD39"
#SQLITE
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///site.db"
app.config['UPLOAD_FOLDER'] = imageFolder

#create database
db = SQLAlchemy(app)

bcrypt = Bcrypt(app)

#routes.py is importing app variable import at EOF to avoid circular import
from imagerepository import routes