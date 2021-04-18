from pychartjs import BaseChart, ChartType
import random
import datetime
import calendar
from mainapp.model import reservation, room


class MyBarGraph(BaseChart):
  type = ChartType.Doughnut

  class labels:
    grouped = [0]

  class data:
    data = [0]
    backgroundColor = [0]

  class options:
    tooltips = {
      "callbacks": {
        "afterLabel": "<<function(tooltipItem, data) { var dataset = data.datasets[tooltipItem.datasetIndex];  var total = dataset.data.reduce(function(previousValue, currentValue, currentIndex, array) {return previousValue + currentValue;}); var currentValue = dataset.data[tooltipItem.index]; var percentage = Math.floor(((currentValue/total) * 100)+0.5); return percentage + '%';}>>",
        "label": "<<function(tooltipItem, data) { var dataLabel = data.labels[tooltipItem.index]; var value = ': ' + data.datasets[tooltipItem.datasetIndex].data[tooltipItem.index].toLocaleString(); if (Chart.helpers.isArray(dataLabel)) { dataLabel = dataLabel.slice(); dataLabel[0] += value; } else { dataLabel += value; } return dataLabel; }>>"
      }
    }
    title = {
      "display": True,
      "text": ''
    }

  def __init__(self, data, types, title):
    self.labels.grouped = types
    self.data.data = data
    self.data.backgroundColor = [str("#{:06x}".format(random.randint(0, 0xFFFFFF))) for i in range(0, len(types))]
    self.options.title["text"] = title


def getReservationByQuery(input, month, year):
  start_date, end_date = getMonthRange(month, year)
  reservations = reservation.getByDate(start_date, end_date)
  types = list(set([room.type for room in room.getAll()]))
  result = [0 for i in range(0, len(types))]

  for reser in reservations:
    for index in range(0, len(types)):
      if (types[index] == reser.room.type):
        if (input == "total"):
          result[index] += int(reser.total)
        elif (input == "dayTotal"):
          result[index] += int(reser.dayTotal)
  return result, types


def getMonthRange(month, year):
  num_days = calendar.monthrange(year, month)[1]
  start_date = datetime.date(year, month, 1)
  end_date = datetime.date(year, month, num_days)
  return start_date, end_date
