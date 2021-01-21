# ShopifyImageRepository
This is the technical portion of the application for Summer 2021 backend developer internship position at Shopify!

# Backend
The backend is powered by Flask and Python

# Frontend
The frontend utilises HTML, CSS, JS, and Bootstrap

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

## Key Design Decisions

I decided to use python as the primary language for this project for the following reasons: Python is great for building prototypes with it's abundunce of free to use frameworks and libraries, extremely flexible and efficient, performance and scalability were not a primary concern. To power the backend I decided to use Flask apposed to Django this decision was primariliy made on the bias of the developer having prior experience utilising flask however Django offers integrated ORM and data models that would have been sufficient for this project. Furthermore, heading into the project and given the quick iterations and timeline I was constantly making changes to the libraries I was using which favoured flasks flexibility. SQLAlchemy was an easy decision to make since it allows for the simple creation of database tables by creating models similar to that of Django.

# Demonstration

## Creating an Account and Logging in

### Features:

* When registering an account passwords must match
* Checks database to make sure user does not already have an account
* Flash messages to give user feedback

![](CreateAccountLogin.gif)

## Usage (Run locally)


In the project folder import db from package

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

# How can I monitor the database?
A free and awesome tool can be found [here](https://sqlitebrowser.org/)


# How to run the application?
In order to run the web application navigate to the imagerepository package and run

```bash
python application.py
```


