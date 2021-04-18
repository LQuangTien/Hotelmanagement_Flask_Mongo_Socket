from mainapp.models_mongodb import regulation


def getAll():
  return regulation.objects()
