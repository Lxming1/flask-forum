import os
import uuid
from flask import Blueprint, session, request, redirect, flash, render_template

from db.db_upload import DbUpload
from db.db_user import DbUser

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
xmAvatarApi = Blueprint('avatar', __name__)

@xmAvatarApi.route('/upload_avatar', methods=['POST'])
def xmHome():
  # 通过表单中name值获取图片
  imgData = request.files['avatar']
  if len(imgData.filename) == '':
    return redirect('/')

  # 获取图片名称及后缀名
  try:
    imgExt = imgData.filename.split('.')[1]
  except:
    return render_template('404.html', message='错误，请重新选择图片')

  user = session['userid']
  # 设置图片要保存到的路径
  path = basedir + "/static/img/avatars/"

  # 图片path和名称组成图片的保存路径

  uuid_str = uuid.uuid4().hex
  file_name = uuid_str + '.' + imgExt
  file_path = path + file_name

  mimetypes = imgData.mimetype


  # 保存图片
  imgData.save(file_path)
  size = os.stat(file_path).st_size

  # url是图片的路径
  url = '/static/img/avatars/' + file_name
  delExistAvatar(user, path)


  DbUpload().dbSaveAvatar(file_name, mimetypes, size, user)
  DbUser().setAvatar(url, user)
  session['avatar_url'] = url

  # flash('修改头像成功')
  return redirect('/')

def delExistAvatar(user, path):
  filename = DbUser().delAvatar(user)
  if filename == '':
    return
  filePath = path + str(filename)

  if os.path.exists(filePath):
    os.remove(filePath)

