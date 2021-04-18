import hashlib
from mainapp.models_mongodb import users
from mainapp.model import user


def authValidate(request):
  username = request.form.get('username')
  isUsernameMatched = not not users.objects(username=username.strip()).first()

  if not isUsernameMatched:
    return None, "User not existed"

  password = request.form.get('password')
  password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
  isPasswordMatched = not not users.objects(password=password.strip()).first()

  if not isPasswordMatched:
    return None, "Wrong password"

  user = users.objects(username=username.strip(), password=password.strip()).first()
  return user, ""


def registerValidate(request):
  userInfo = {
    'username': request.form.get('Username'),
    'password': str(hashlib.md5(request.form.get('Password').strip().encode('utf-8')).hexdigest()),
    'email': request.form.get('Email'),
    'lastname': request.form.get('Lastname'),
    'firstname': request.form.get('Firstname'),
    'sex': request.form.get('sex'),
    'address': request.form.get('Address')
  }

  isUsernameDuplicate = not not users.objects(username=userInfo['username'].strip()).first()
  isMailDuplicate = not not users.objects(email=userInfo['email'].strip()).first()
  if isUsernameDuplicate:
    return None, "User existed"
  if isMailDuplicate:
    return None, "Email existed"

  newUser = user.create(userInfo)
  return newUser, "Register successfully"


def contactValidate(request):
  name = request.form.get('name')
  email = request.form.get('email')
  message = request.form.get('message')
  return name, email, message
