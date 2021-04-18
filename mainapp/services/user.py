from math import ceil
from flask import session
from mainapp.model import user, reservation


def getReservations():
  currentUser = user.get(session.get('user'))
  perPage = 10
  res = reservation.getUserReservations(currentUser)
  totalPage = ceil(len(currentUser.reservations) / perPage)
  return res, perPage, totalPage