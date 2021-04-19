from mainapp.model import messages


def get(fromUser, toUser):
  return messages.get(fromUser, toUser)


def create(fromUser, toUser, content):
  return messages.create(fromUser, toUser, content)


def getConsultantHistory(consultant):
  data  = list(messages.getConsultantHistory(consultant))
  data.reverse()
  result = []
  for mess in data:
    if mess['toUser'] not in result:
      result.append(mess['toUser'])
    if mess['fromUser'] not in result:
      result.append(mess['fromUser'])
  result.remove(consultant)
  return  result
