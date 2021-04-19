import datetime

from mongoengine import *
from flask_login import UserMixin


class embReservation(EmbeddedDocument):
  arriveDate = DateField(required=True, null=False)
  departureDate = DateField(required=True, null=False)
  reservation = ObjectIdField(null=True, required=True)


class rooms(Document):
  meta = {'collection': 'rooms'}
  name = StringField(max_length=50, null=False, required=True)
  capacity = IntField(null=False, required=True)
  image = StringField(max_length=250, null=False, required=True)
  description = StringField(max_length=250, null=False, required=True)
  type = StringField(max_length=50, null=False, required=True)
  price = IntField(null=False, required=True)
  reservations = EmbeddedDocumentListField(embReservation, null=False, default=[])

  def __str__(self):
    return self.name


class users(Document, UserMixin):
  meta = {'collection': 'users'}
  username = StringField(max_length=50, null=False, required=True, unique=True)
  password = StringField(max_length=50, null=False, required=True)
  email = StringField(max_length=50, null=False, required=True)
  firstname = StringField(max_length=50, null=False, required=True)
  lastname = StringField(max_length=50, null=False, required=True)
  address = StringField(max_length=50, null=False, required=True)
  sex = StringField(max_length=50, null=False, required=True)
  role = IntField(null=False, required=True, default=2)
  reservations = ListField(ReferenceField(rooms), default=[])

  def is_authenticated(self):
    return True

  def is_active(self):
    return True

  def is_anonymous(self):
    return False

  def get_id(self):
    return str(self.id)

  # Required for administrative interface
  def __unicode__(self):
    return self.login

  def __str__(self):
    return self.username


class reservations(Document):
  meta = {'collection': 'reservations'}
  room = ReferenceField(rooms, required=True, null=False)
  user = ReferenceField(users, required=True, null=False)
  arriveDate = DateField(required=True, null=False)
  departureDate = DateField(required=True, null=False)
  dayTotal = IntField(null=False, required=True)
  numberOfGuest = IntField(null=False, required=True)
  hasForeigner = BooleanField(null=False, required=True)
  isOverCapacity = BooleanField(null=False, required=True)
  tax = FloatField(null=False, required=True)
  total = FloatField(null=False, required=True)

  def __str__(self):
    return str(self.id) + '_Room-' + str(self.room)


class regulation(Document):
  meta = {'collection': 'regulation'}
  name = StringField(max_length=50, null=False, required=True, unique=True)
  value = FloatField(null=False, required=True)

  def __str__(self):
    return str(self.name)


class messages(Document, UserMixin):
  meta = {'collection': 'messages'}
  fromUser = StringField(max_length=50, null=False, required=True)
  toUser = StringField(max_length=50, null=False, required=True)
  content = StringField(max_length=1000, null=False, required=True)
  created_at = DateTimeField(null=False, required=True, default=datetime.datetime.now())
