# Shopify Image Repository
This is the technical portion of the application for Summer 2021 backend developer internship position at Shopify! The web-based application allows for users to share their photos with other users and also maintain a private repository for their own access. Users are able to organize their photos in their private repositories by selecting tags, upload multiple images at once and even create a customizable profile!

# Backend
The backend is powered by Flask and Python

# Frontend
The frontend utilises HTML, CSS, JS, and Bootstrap Templates

# Libraries
Many libraries were used to make this project come to life

```python
Flask
SQLAlchemy
os
flask_bcrypt
flask_login
flask_wtf
flask_wtf.file
wtforms
wtforms.validators
datetime
UserMixin
secrets
PIL
```

# Key Design Decisions

I decided to use Python as the primary language for this project for the following reasons: Python is great for building prototypes with it's abundunce of free to use frameworks and libraries, extreme flexibility, and provides amazing agility when performance and scalability are not a primary concern. To power the backend, I decided to use Flask apposed to Django this decision was primariliy made on the bias of the developer having prior experience utilising Flask however Django offers integrated ORM and data models that would have been sufficient for this project. Furthermore, heading into the project and given the quick iterations and timeline I was constantly making changes to the libraries I was using which favoured Flask's flexibility. SQLAlchemy was an easy decision to make since it allows for the simple creation of database tables by creating models similar to that of Django.

# Demonstration
*All images used in the demonstration gifs were obtained from [Pexels](https://www.pexels.com/license/) (free to use without need for attribution)*

## Creating an Account and Logging in

### Features:

* When registering an account passwords must match
* Checks database to make sure user does not already have an account
* Flash messages to give user feedback

![](./Markdown/CreateAccountLogin.gif)

## Uploading Photos to your Private Library

### Features:

* You can use multiple tags to sort your images
* Clicking on a post brings up a new bulletin board page containing all images in your post
* Time stamps are stored and displayed back to the user

![](./Markdown/PostAndViewPrivate.gif)

## Sharing Photos Publically with other Accounts

### Features:

* Uploaded images are able to be easily viewed through a carousel
* A user is able to view publically shared posts from other accounts

![](./Markdown/SharePosts.gif)

## Usage (Run locally)

Navigate to the location of the project folder and import db from the imagerepository package

```bash
from imagerepository import db
```

import the neccesary models to create the tables

```bash
from imagerepository.models import User, Post, Photo
```

Create the database

```bash
db.create_all()
```
At this point a new file will be generated in the imagerepository package under the name site.db

# How can I monitor the database?
A free and awesome tool can be found [here](https://sqlitebrowser.org/). The last stable updated version was released on 2020-11-09. The github project can be found by following the link [here](https://github.com/sqlitebrowser/sqlitebrowser)


# How to run the application?
In order to run the web application locally navigate to the imagerepository package and run the following

```bash
python application.py
```
Next open up the your preffered web browser and paste in the link the is displayed in the python console. Most IDE's will make the link clickable which will open up the web application in the default browser selected by your operating system.

```bash
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with stat
```

# Project Status
There are multiple features that I still want to add. Since this project is for a job application the development will likely concluded once the hiring period has ended. I have listed below a rough roadmap of features. The checkboxes indicates the developer's current focus.

 - [x] Profile Viewing
  * In the public feed section add the ability for a user to view another individuals profile, their public information, and all their public posts
  * Privacy Settings
    * Add the ability for a user to adjust what is viewable to other users on the network including whether they want their email, photos, profile picture shared
- [x] Customizable tags
  * Add the ability for the user to add custom tags to their photos and not be restricted by the presets
- [ ] Front-end improvements
  * Improve visual of the bulletin board making the photos appear on sticky notes or something more visually appealing and immersive
 - [x] Forgot password flow
  * Add the ability for a user to reset their password via the email that they signed up with in order to prevent being locked out of account
 - [ ] Photo features
  * Add the ability for light photo editing including being able to select a specific 250x250 area the user wants to display
  * ability to apply simple filters to their images
 - [ ] Post editing
  * Add the ability for a user to edit their post including the title, descrption and photo content
  * If this is a public post, indicate to other users that this post has been edited

