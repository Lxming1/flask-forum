import hashlib


def handlePas(password):
  md5 = hashlib.md5()
  md5.update(password.encode('utf-8'))
  return md5.hexdigest()