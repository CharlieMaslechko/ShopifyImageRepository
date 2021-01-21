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

## Usage (Run locally)

#Setup flask

#Setup local database

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


# To run the application
In order to run the web application navigate to the imagerepository package and run

```bash
python application.py
```


