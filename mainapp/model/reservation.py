from mainapp.models_mongodb import reservations


def getByDate(start_date, end_date):
  # return Reservation.query.filter(
  #     and_(Reservation.arriveDate >= start_date, Reservation.arriveDate <= end_date),
  #     and_(Reservation.departureDate >= start_date, Reservation.departureDate <= end_date)
  #   ).all()
  result = reservations.objects().filter(
    arriveDate__gte=(start_date),
    departureDate__lte=(end_date)
  )
  return result


def create(reservationData):
  reservation = reservations(room=reservationData['room'], user=reservationData['user'],
                             arriveDate=reservationData['arriveDate'],
                             departureDate=reservationData['departureDate'], dayTotal=reservationData['dayTotal'],
                             numberOfGuest=reservationData['numberOfGuest'],
                             hasForeigner=reservationData['hasForeigner'],
                             isOverCapacity=reservationData['isOverCapacity'], tax=reservationData['tax'],
                             total=reservationData['total'])
  reservation.save()
  return reservation


def getUserReservations(currentUser):
  return reservations.objects().filter(id__in=[reservation.id for reservation in currentUser.reservations]).order_by(
    '-id')
