import base64
import copy
from os import environ

from flask.json import dumps
from flask_mail import Message
from flask import render_template, session, jsonify
from flask_socketio import emit, join_room, send

from mainapp import app, login, utils, mail, socketio
from flask_login import login_user, login_required

from mainapp.models_mongodb import messages as MesModel, Animal
from mainapp.services import auth, room, user, messages as Messes

login.login_view = "login"


@login.user_loader
def load_user(user_id):
  return users.objects(id=user_id).first()


@app.route("/", methods=['post', 'get'])
def index():
  if request.method == 'GET':
    rooms = room.getAll()
    return render_template('hotel/index.html', error=request.args.get('error'), rooms=rooms[:-2][0])


@app.route("/history")
def history():
  page = request.args.get('page') or 1
  reservations, perPage, totalPage = user.getReservations()
  return render_template('hotel/history.html', reservations=reservations, perPage=perPage, totalPage=totalPage,
                         page=int(page))


@app.route("/rooms")
def rooms():
  if request.method == 'GET':
    type, arriveDate, departureDate = room.handleGetRooms(request)
    rooms, perPage, totalPage = room.getByDate(type, arriveDate, departureDate)
    return render_template('hotel/our-room.html',
                           rooms=rooms, totalPage=totalPage, perPage=perPage)


@app.route("/our-rooms")
def ourRooms():
  if request.method == 'GET':
    rooms, perPage, totalPage = room.getAll()
    return render_template('hotel/our-room.html', rooms=rooms, visit=True, totalPage=totalPage, perPage=perPage)


@app.route("/aboutus")
@login_required
def aboutus():
  return render_template('hotel/about-us.html')


@app.route("/contact", methods=['post', 'get'])
def contact():
  if request.method == 'GET':
    return render_template('hotel/contact-us.html')
  if request.method == 'POST':
    name, email, message = auth.contactValidate(request)
    msg = Message("Customer's contact",
                  sender='tienkg5554@gmail.com',
                  recipients=['tienkg4445@gmail.com'])
    msg.body = "Email: " + email + "\n" + "Name: " + name + "\n" + message
    mail.send(msg)
    return redirect('/')


@app.route("/booking", methods=['post', 'get'])
@login_required
def booking():
  if request.method == 'GET':
    [bookingInfo, qrURL, errorCode] = room.handleGetBooking(request)
    return render_template('hotel/booking.html', bookingInfo=bookingInfo, qrURL=qrURL, errorCode=errorCode)
  if request.method == 'POST':
    bookingInfo, qrURL = room.handlePostBooking(request)
    return render_template('hotel/booking.html', bookingInfo=bookingInfo, qrURL=qrURL)


@app.errorhandler(404)
def notFound(e):
  return render_template('hotel/404.html'), 404


@app.route('/register', methods=['post', 'get'])
def register():
  if request.method == 'GET':
    return render_template('hotel/register.html')
  if request.method == 'POST':
    user, result = auth.registerValidate(request)
    if not user:
      return render_template('hotel/register.html', error=result)
    return render_template('hotel/register.html', result=result)


@app.route('/login', methods=['post', 'get'])
def login():
  if request.method == 'GET':
    return render_template('hotel/login.html')
  if request.method == 'POST':
    user, error = auth.authValidate(request)
    if not user:
      return render_template('hotel/login.html', error=error)
    login_user(user=user)
    session['user'] = [str(user.id), user.role]
    next = utils.handleNextUrl(request)
    return redirect(next)


@app.route('/logout', methods=['post', 'get'])
def logout():
  if request.method == 'GET':
    logout_user()
    return redirect('/')


@app.route('/login-admin', methods=['post', 'get'])
def login_admin():
  if request.method == 'POST':
    user, error = auth.authValidate(request)
    if user:
      login_user(user=user)
  return redirect('/admin')


@app.route('/api/roomtypes')
def roomtypes():
  types, maxCapacity = room.getRoomTypes()
  return jsonify({"types": types, "maxCapacity": maxCapacity})

@app.route('/api/currentuser')
def currentuser():
  [id, role] = session.get('user')
  return user.getById(id)

@app.route('/api/audio')
def audio():
  # mes = MesModel.objects().filter(toUser='tien', content='wav').first()
  # with open('static/audio/CantinaBand3.wav', 'rb') as fd:
  #     mes.file.put(fd, content_type='audio/wav')
  # mes.save()
  # print("save roi")
  # marmot = Animal.objects().first()
  # photo = marmot.photo.read()
  # a = base64.b64encode(photo)
  # a = a.decode("utf-8")
  # content_type = marmot.photo.content_type
  return jsonify({"audio":""})

@app.route("/chat", methods=['post', 'get'])
@login_required
def chat():
  return render_template('hotel/chat.html')


@socketio.on('join')
def join():
  if not session.get('user'): return

  [id, role] = session.get('user')
  if (role == 2):
    join_room('users')
    if not hasattr(socketio, "consultants"): return
    socketio.emit('user_join_chat', socketio.consultants, room='users')
    return
  if (role == 3):
    consultant = user.getById(id)
    if not hasattr(socketio, "consultants"):
      socketio.consultants = []
    if (consultant not in socketio.consultants):
      socketio.consultants.append(consultant)
    join_room(consultant)
    history = Messes.getConsultantHistory(consultant)
    socketio.emit('consultants_join_chat', socketio.consultants, room='users')
    socketio.emit('consultants_work', history, room=consultant)
  return


@socketio.on('disconnect')
def disconnect():
  [id, role] = session.get('user')
  if (role != 3):
    return
  consultant = user.getById(id)
  # if (consultant in socketio.consultants):
  socketio.consultants.remove(consultant)
  socketio.emit('consultants_join_chat', socketio.consultants, room='users')
  return

def serializeChatResponse(mess):
  result = []
  for mes in mess:
    if(mes.file == None):
      result.append(mes)
    else:
      file = base64.b64encode(mes.file.read())
      file = file.decode("utf-8")
      result.append({
        "fromUser": mes.fromUser,
        "toUser": mes.toUser,
        "content": mes.content,
        "created_at": mes.created_at,
        "file": file
      })
  return result

@socketio.on('user_load_chat')
def user_load_chat(target):
  [id, role] = session.get('user')
  currentUser = user.getById(id)
  roomChat = currentUser+'_'+target
  join_room(roomChat)

  # mes = MesModel.objects().filter(toUser='tien', content='wav').first()
  # with open('static/audio/a.jpg', 'rb') as fd:
  #   mes.file.put(fd, content_type='image/jpg')
  # mes.save()
  # print("save roi")

  mess = Messes.get(currentUser, target);
  socketio.emit('server_respone_chat_toUser', dumps({"data": mess, "target": target}), room=roomChat)

@socketio.on('consultant_load_chat')
def consultant_load_chat(target):
  [id, role] = session.get('user')
  currentUser = user.getById(id)
  roomChat = currentUser+'_'+target
  join_room(roomChat)
  mess = Messes.get(target, currentUser);
  socketio.emit('server_respone_chat_toConsultant', dumps({'data': mess, 'target': target}), room=roomChat)

@socketio.on('send_message')
def send_message(data):
  [id, role] = session.get('user')
  currentUser = user.getById(id)
  message = data['message']
  toUser = data['toUser']
  file = data['file']
  type = data['type']
  roomUser = ''
  roomConsultant = ''
  if(role == 2):
    roomUser = currentUser + '_' + toUser
    roomConsultant = toUser + '_' + currentUser
  if (role == 3):
    roomUser = toUser + '_' + currentUser
    roomConsultant = currentUser + '_' + toUser
  Messes.create(currentUser, toUser, message, file['binary'], type);
  mess = Messes.get(currentUser, toUser);

  if (role == 2):
    socketio.emit('server_respone_chat_toUser', dumps({'data': mess, 'target': toUser}), room=roomUser)
    socketio.emit('server_respone_chat_toConsultant', dumps({'data': mess, 'target': currentUser}), room=roomConsultant)
    history = Messes.getConsultantHistory(toUser)
    socketio.emit('consultants_work', history, room=toUser)
  if (role == 3):
    socketio.emit('server_respone_chat_toUser', dumps({'data': mess, 'target': currentUser}), room=roomUser)
    socketio.emit('server_respone_chat_toConsultant', dumps({'data': mess, 'target': toUser}), room=roomConsultant)
    history = Messes.getConsultantHistory(currentUser)
    socketio.emit('consultants_work', history, room=currentUser)

if __name__ == "__main__":
  from mainapp.admin_module import *

  socketio.run(app, debug=True, port=int(environ.get('PORT')))
