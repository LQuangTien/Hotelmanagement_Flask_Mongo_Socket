from datetime import datetime

from mongoengine import Q

from mainapp.models_mongodb import rooms, reservations
import time


# ROOM_ROOMTYPE = db.session.query(Room, RoomType).join(RoomType, Room.type == RoomType.id)
# ROOM_ROOMTYPE_RESERVATION = db.session.query(Room, RoomType, Reservation)
# JOINED_TABLE = ROOM_ROOMTYPE_RESERVATION.join(RoomType, Room.type == RoomType.id)
# LEFTJOINED_TABLE = JOINED_TABLE.outerjoin(Reservation, Room.id == Reservation.room)


def getAll():
  # ROOM_ROOMTYPE_RESERVATION = db.session.query(Room, RoomType, Reservation)
  # JOINED_TABLE = ROOM_ROOMTYPE_RESERVATION.join(RoomType, Room.type == RoomType.id)
  # return JOINED_TABLE.group_by(Room.id).order_by(Room.name).all()
  return rooms.objects()


def get(name):
  return rooms.objects(name=str(name)).first()


#
# tìm trong khoảng tgian đó những phòng nào trống
def getByDate(type=None, arriveDate=None, departureDate=None):
  # Chua bat chuan hoa
  # matchedReservations = reservations.objects().filter(
  #   arriveDate__gte=datetime.fromisoformat(arriveDate),
  #   departureDate__lte=datetime.fromisoformat(departureDate)
  # )
  # if (type == None or type == 'None'):
  #   rooms.objects().filter(
  #     name__nin=[res.room.name for res in matchedReservations]
  #   )
  #
  #   rooms.objects().filter(
  #     name__nin=[res.room.name for res in matchedReservations],
  #     type=type
  #   )

  # Bat chuan hoa
  roomList = rooms.objects()
  a = Q(reservations__arriveDate__gte=datetime.fromisoformat(arriveDate))
  b = Q(reservations__arriveDate__lte=datetime.fromisoformat(arriveDate))
  c = Q(reservations__departureDate__lte=datetime.fromisoformat(departureDate))
  d = Q(reservations__departureDate__gte=datetime.fromisoformat(departureDate))
  bookedRoom = roomList.filter( (a and b) or (c and d) )
  if (type == None or type == 'None'):
    return roomList.filter(
      name__nin=[room.name for room in bookedRoom]
    )
  return roomList.filter(
    name__nin=[room.name for room in bookedRoom],
    type=type
  )
