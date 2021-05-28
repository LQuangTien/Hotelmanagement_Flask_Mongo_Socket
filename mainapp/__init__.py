from flask import Flask
import os
from flask_login import LoginManager
from flask_admin import Admin
from flask_mongoengine import MongoEngine
from flask_socketio import SocketIO
# settings.py
from dotenv import load_dotenv
from mongoengine import connect, disconnect

load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)
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
socketio = SocketIO(app,logger=True,)

