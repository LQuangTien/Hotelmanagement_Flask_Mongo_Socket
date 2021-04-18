# import hashlib
#
# from flask_login import UserMixin
# from sqlalchemy import Column, Integer, Float, String, Date, Boolean, ForeignKey
# from sqlalchemy import Enum
# from sqlalchemy.orm import relationship
# from mainapp import db
# from datetime import datetime


# class Role(db.Model):
#   __tablename__ = 'role'
#   id = Column(Integer, primary_key=True, autoincrement=True)
#   name = Column(String(50), nullable=False, unique=True)
#   user = relationship('User', backref='Role', lazy=True)
#
#   def __str__(self):
#     return self.name
#
#
# class User(db.Model, UserMixin):
#   __tablename__ = 'user'
#   id = Column(Integer, primary_key=True, autoincrement=True)
#   username = Column(String(50), nullable=False, unique=True)
#   password = Column(String(50), nullable=False)
#   email = Column(String(50), nullable=True, unique=True)
#   firstname = Column(String(50), nullable=False)
#   lastname = Column(String(50), nullable=False)
#   address = Column(String(100), nullable=True)
#   sex = Column(Enum('Male', 'Female', 'Other'))
#   reservationId = relationship('Reservation', backref='User', lazy=True)
#   role = Column(Integer, ForeignKey(Role.id), nullable=False)
#
#   def __str__(self):
#     return self.username
#
#
# class RoomType(db.Model):
#   __tablename__ = 'roomtype'
#
#   id = Column(Integer, primary_key=True, autoincrement=True)
#   name = Column(String(50), nullable=False, unique=True)
#   price = Column(Integer, nullable=False)
#   roomId = relationship('Room', backref='room', lazy=True)
#
#   def __str__(self):
#     return str(self.name)
#
#
# class Room(db.Model):
#   __tablename__ = 'room'
#
#   id = Column(Integer, primary_key=True, autoincrement=True)
#   name = Column(Integer, nullable=False, unique=True)
#   capacity = Column(Integer, default=3)
#   image = Column(String(50), nullable=False)
#   description = Column(String(1000), nullable=True)
#   type = Column(Integer, ForeignKey(RoomType.id), nullable=False)
#   reservation = relationship('Reservation', backref='Room', lazy=True)
#
#   def __str__(self):
#     return str(self.name)
#
#
# class Reservation(db.Model):
#   __tablename__ = 'reservation'
#
#   id = Column(Integer, primary_key=True, autoincrement=True)
#   room = Column(Integer, ForeignKey(Room.id), nullable=False)
#   user = Column(Integer, ForeignKey(User.id), nullable=False)
#   arriveDate = Column(Date, nullable=False)
#   departureDate = Column(Date, nullable=False)
#   dayTotal = Column(Integer, nullable=False)
#   numberOfGuest = Column(Integer, nullable=False)
#   hasForeigner = Column(Boolean, nullable=False)
#   isOverCapacity = Column(Boolean, nullable=False)
#   tax = Column(Float, nullable=False)
#   total = Column(Float, nullable=False)
#
#   def __str__(self):
#     return str(self.id) + '_' + str(self.room)
#
#
# class Regulation(db.Model):
#   __tablename__ = 'regulation'
#
#   id = Column(Integer, primary_key=True, autoincrement=True)
#   name = Column(String(100), nullable=False, unique=True)
#   value = Column(Float, nullable=False)
#
#   def __str__(self):
#     return str(self.name)
#
#
# if __name__ == '__main__':
#   db.create_all()
