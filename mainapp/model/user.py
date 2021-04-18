from mainapp.models_mongodb import users


def get(id):
  return users.objects(id=id).first()


def create(userInfo):
  user = users(username=userInfo['username'], password=userInfo['password'], email=userInfo['email'],
               firstname=userInfo['firstname'], lastname=userInfo['lastname'], address=userInfo['address'],
               sex=userInfo['sex'])
  user.save()
  return user
