from datetime import datetime
import json
from urllib.request import urlopen, Request
import uuid
import hmac
import hashlib
from flask import session
from os import environ

def subtractDate(firstDateString, seccondDateString):
  result = datetime.strptime(firstDateString, '%Y-%m-%d') - datetime.strptime(seccondDateString, '%Y-%m-%d')
  return result.total_seconds()

def handleNextUrl(request):
  if not request:
    return None
  next = request.args.get('next')
  bookForm = session.get('bookForm')
  if bookForm:
    return f"rooms?arriveDate={bookForm['arriveDate']}&departureDate={bookForm['departureDate']}&type={bookForm['type']}&numberOfGuest={bookForm['numberOfGuest']}&hasForeigner={bookForm['hasForeigner']}"
  if next == None:
    return "/"
  return next


def createQRCode(amount):
  # parameters send to MoMo get get payUrl
  endpoint = environ.get('PAYMENT_ENDPOINT')
  partnerCode = environ.get('PARTNER_CODE')
  accessKey = environ.get('ACCESS_KEY')
  serectkey = b"2l9NSfk8rWqc4CpYGZva7dBfCYo9xM25"
  orderInfo = "Thanh toán tiền khách sạn"
  returnUrl = environ.get('DOMAIN')+"/booking"
  notifyurl = environ.get('DOMAIN')
  amount = str(amount)
  orderId = str(uuid.uuid4())
  requestId = str(uuid.uuid4())
  requestType = "captureMoMoWallet"
  extraData = "merchantName=;merchantId="  # pass empty value if your merchant does not have stores else merchantName=[storeName]; merchantId=[storeId] to identify a transaction map with a physical store
  # before sign HMAC SHA256 with format
  # partnerCode=$partnerCode&accessKey=$accessKey&requestId=$requestId&amount=$amount&orderId=$oderId&orderInfo=$orderInfo&returnUrl=$returnUrl&notifyUrl=$notifyUrl&extraData=$extraData
  rawSignature = "partnerCode=" + partnerCode + "&accessKey=" + accessKey + "&requestId=" + requestId + "&amount=" + amount + "&orderId=" + orderId + "&orderInfo=" + orderInfo + "&returnUrl=" + returnUrl + "&notifyUrl=" + notifyurl + "&extraData=" + extraData
  # puts raw signature
  # signature
  h = hmac.new(serectkey, rawSignature.encode('utf-8'), hashlib.sha256)
  signature = h.hexdigest()
  # json object send to MoMo endpoint
  data = {
    'partnerCode': partnerCode,
    'accessKey': accessKey,
    'requestId': requestId,
    'amount': amount,
    'orderId': orderId,
    'orderInfo': orderInfo,
    'returnUrl': returnUrl,
    'notifyUrl': notifyurl,
    'extraData': extraData,
    'requestType': requestType,
    'signature': signature
  }
  data = json.dumps(data).encode('utf-8')
  clen = len(data)
  req = Request(endpoint, data, {'Content-Type': 'application/json', 'Content-Length': clen})
  f = urlopen(req)
  response = f.read()
  f.close()
  return json.loads(response)['payUrl']
