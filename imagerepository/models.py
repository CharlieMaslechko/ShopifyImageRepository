from imagerepository import db
from datetime import datetime

#Tables in database representd by models

#Users can have many posts, posts can have one author 1 -> Many
#User table
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    #Profile picture
    image_file = db.Column(db.String(20), nullable=False, default="default.jpg")

    #Lazy will load all posts from single user in one go
    posts = db.relationship("Post", backref="author", lazy=True)

    #User object print formatting
    def __repr__(self):
        format = "User (username: " + str(self.username) + ", email: " + str(self.email) + ", profile picture: " + str(self.image_file) + ")"
        return format

#Post table
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    is_private = db.Column(db.Boolean, nullable=False)

    #id in user model acts as foreign key in post model
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    #Post object print formatting
    def __repr__(self):
        format = "Post (title: " + str(self.title) + ", date: " + str(self.date_posted)
        return format