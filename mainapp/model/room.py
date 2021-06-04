from datetime import datetime

from mongoengine import Q

from mainapp.models_mongodb import rooms, reservations
import time



def getAll():
  return rooms.objects()


def get(name):
  return rooms.objects(name=str(name)).first()


#
# tìm trong khoảng tgian đó những phòng nào trống
def getByDate(type=None, arriveDate=None, departureDate=None):
  roomList = rooms.objects()
  a = Q(reservations__arriveDate__gte=datetime.fromisoformat(arriveDate))
  b = Q(reservations__arriveDate__lte=datetime.fromisoformat(arriveDate))
  c = Q(reservations__departureDate__lte=datetime.fromisoformat(departureDate))
  d = Q(reservations__departureDate__gte=datetime.fromisoformat(departureDate))
  bookedRoom = roomList.filter( (a and b) and (c and d) )
  if (type == None or type == 'None'):
    return roomList.filter(
      name__nin=[room.name for room in bookedRoom]
    )
  return roomList.filter(
    name__nin=[room.name for room in bookedRoom],
    type=type
  )
