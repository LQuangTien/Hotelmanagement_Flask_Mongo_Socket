from math import ceil
from flask import session
from mainapp.model import user, reservation
from mainapp.model.user import get


def getById(id):
  return get(id).username
def getReservations():
  currentUser = user.get(session.get('user')[0])
  perPage = 10
  res = reservation.getUserReservations(currentUser)
  totalPage = ceil(len(currentUser.reservations) / perPage)
  return res, perPage, totalPage