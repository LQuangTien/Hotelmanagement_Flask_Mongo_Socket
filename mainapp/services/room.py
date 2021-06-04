from math import ceil
from flask import session
from werkzeug.utils import redirect
from bson import ObjectId

from mainapp import utils
from mainapp.models_mongodb import rooms, embReservation
from mainapp.utils import subtractDate
from mainapp.services import reservation

from mainapp.model import room, user, regulation

SECONDS_IN_ONE_DAY = 60 * 60 * 24


def getAll():
  rooms = room.getAll()
  perPage = 3
  totalPage = ceil(len(rooms) / perPage)
  return rooms, perPage, totalPage


def getRoomTypes():
  rooms = room.getAll()
  types = list(set([room.type for room in rooms]))
  maxCapacity = int(regulation.getAll().filter(name='maxCapacity').first().value)
  return types, maxCapacity


def getByDate(type, arriveDate, departureDate):
  rooms = room.getByDate(type, arriveDate, departureDate)
  perPage = 3
  totalPage = ceil(len(rooms) / perPage)
  return rooms, perPage, totalPage


def handlePostBooking(request):
  bookingInfo = bookingRoom(request)
  #amount = float(bookingInfo['tax']) * bookingInfo['price'] * bookingInfo['dayTotal']
  #qrURL = utils.createQRCode(int(amount))
  qrURL = '?errorCode=0'
  session['booking']['qrURL'] = qrURL
  return bookingInfo, qrURL


def handleGetBooking(request):
  bookingInfo = session.get('booking')
  if (not bookingInfo):
    return redirect('/')
  qrURL = bookingInfo['qrURL'] or None
  errorCode = request.args.get('errorCode') or None
  if (errorCode):
    bookingInfo['isDone'] = True
  if (bookingInfo['isDone']):
    createReservation(bookingInfo)
    session['booking'] = None
    session['bookForm'] = None
  return [bookingInfo, qrURL, errorCode]

def createReservation(bookingInfo):
  reserv = reservation.create(bookingInfo)
  userId = session.get('user')[0]
  currentUser = user.get(userId)
  currentUser.reservations.append(reserv.id)
  currentUser.save()
  currentRoom = room.get(bookingInfo['room'])
  emb = embReservation(arriveDate=bookingInfo['arriveDate'], departureDate=bookingInfo['departureDate'], reservation=ObjectId(bookingInfo['roomId']))
  currentRoom.reservations.append(emb)
  currentRoom.save()

def handleGetRooms(request):
  type = None if request.args.get('type') == 'Any' else request.args.get('type')
  arriveDate = request.args.get('arriveDate')
  departureDate = request.args.get('departureDate')
  numberOfGuest = int(request.args.get("numberOfGuest"))
  hasForeigner = request.args.get("hasForeigner")
  hasForeigner = True if hasForeigner == 'True' else False
  session['bookForm'] = {
    "arriveDate": arriveDate,
    "departureDate": departureDate,
    "numberOfGuest": numberOfGuest,
    "hasForeigner": hasForeigner,
    "type": type,
  }
  return type, arriveDate, departureDate


def bookingRoom(request):
  regulations = regulation.getAll()
  LIMIT_CAPACITY = int(regulations.filter(name='limitCapacity').first().value)
  SURCHARGE_CAPACITY = regulations.filter(name='surchargeCapacity').first().value
  SURCHARGE_FOREIGNER = regulations.filter(name='surchargeForeigner').first().value
  roomName = int(request.form.get("roomName"))
  currentRoom = room.get(roomName)
  userId = session.get('user')[0]
  currentUser = user.get(userId)
  bookForm = session.get('bookForm')
  arriveDate = bookForm['arriveDate']
  departureDate = bookForm['departureDate']
  numberOfGuest = bookForm['numberOfGuest']
  hasForeigner = bookForm['hasForeigner']
  dayTotal = subtractDate(departureDate, arriveDate) / SECONDS_IN_ONE_DAY
  tax = 1
  isOverCapacity = False
  if (hasForeigner):
    tax = SURCHARGE_FOREIGNER
  elif (int(numberOfGuest) > LIMIT_CAPACITY):
    tax = SURCHARGE_CAPACITY
    isOverCapacity = True
  session['booking'] = {
    "tax": tax,
    "room": currentRoom.name,
    "roomId": str(currentRoom.id),
    "sex": currentUser.sex,
    "image": currentRoom.image,
    "description": currentRoom.description,
    "price": currentRoom.price,
    "arriveDate": arriveDate,
    "dayTotal": int(dayTotal),
    "email": currentUser.email,
    "hasForeigner": hasForeigner,
    "isOverCapacity": isOverCapacity,
    "address": currentUser.address,
    "numberOfGuest": numberOfGuest,
    "departureDate": departureDate,
    "lastname": currentUser.lastname,
    "firstname": currentUser.firstname,
    "isDone": False,
  }
  return session['booking']
