from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
import os
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from flask_moment import Moment

"This is the .py file where the configurations have been defined"

# New istance of Flask class, this is needed so that Flask knows where to look for templates, static files, and so on
app = Flask(__name__)
app.config['SECRET_KEY'] = '3487430sd87dsds520852470534ds8cjdhfdjbsakhj3'

Bootstrap(app)

# Moment configuration
moment = Moment(app)

#Password encryption configuration
bcrypt = Bcrypt(app)


# DataBase configuration
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)

# Login configuration
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'


# Mail configuration
mail_settings ={
'MAIL_SERVER' : 'smtp.googlemail.com',
'MAIL_PORT' : 587,
'MAIL_USE_TLS' : True,
'MAIL_USERNAME' : "foodsharingpoint@gmail.com",
'MAIL_PASSWORD' : "Foodsharingpoint@2020"
}
app.config.update(mail_settings)
mail = Mail(app)
from fsp import routes