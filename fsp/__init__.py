from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
import os
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from flask_moment import Moment

app = Flask(__name__)
app.config['SECRET_KEY'] = '3487430sd87dsds520852470534ds8cjdhfdjbsakhj3'

Bootstrap(app)
moment = Moment(app)



# DataBase configuration
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)

bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'  # il login_required ti manda alla pagina del login
login_manager.login_message_category = 'info'  # coloro di blu il messaggio in cui viene richiesto
                                               # il login per poter accedere ad una pagina

# Mail configuration
mail_settings ={
'MAIL_SERVER' : 'smtp.googlemail.com',
'MAIL_PORT' : 587,
'MAIL_USE_TLS' : True,
'MAIL_USERNAME' : "foodsharingpoint@gmail.com",  # os.environ.get('EMAIL_USER')
'MAIL_PASSWORD' : "Foodsharingpoint@2020"   #os.environ.get('EMAIL_PASS')
}
app.config.update(mail_settings)
mail = Mail(app)
from fsp import routes