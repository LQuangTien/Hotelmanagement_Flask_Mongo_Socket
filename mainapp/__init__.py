from flask import Flask
import os
from flask_login import LoginManager
from flask_admin import Admin
from flask_mail import Mail
from flask_mongoengine import MongoEngine

# settings.py
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_ACCOUNT')
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASSWORD')
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MONGODB_SETTINGS'] = {
  'db': 'hotelDB',
  'host': 'localhost',
  'port': 27017
}
db = MongoEngine()
db.init_app(app)

admin = Admin(app=app, name='QUAN LY KHACH SAN',
              template_mode='bootstrap3')
login = LoginManager(app=app)
mail = Mail(app=app)
