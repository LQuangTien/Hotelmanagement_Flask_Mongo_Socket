from mongoengine import Q

from mainapp.models_mongodb import messages


def get(fromUser, toUser):
  return messages.objects().filter(fromUser__in=[fromUser, toUser], toUser__in=[fromUser, toUser]).order_by(
    'created_at')


def create(fromUser, toUser, content, file, type):
  mess = messages(fromUser=fromUser, toUser=toUser, content=content, file=file, type=type)
  mess.save()
  return mess

def getConsultantHistory(consultant):
  pipeline = [
    {"$match": {"$or": [
      {"fromUser": consultant},
      {"toUser": consultant}
    ]}}
  ]
  return messages.objects().aggregate(pipeline)

