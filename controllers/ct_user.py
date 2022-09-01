from flask import request, session, redirect, render_template, Blueprint, flash

from db.db_user import DbUser
from form_model.user_model import LoginModel, RegisterModel

xmUserApi = Blueprint('user', __name__)


@xmUserApi.route('/login', methods=['POST', 'GET'])
def xmLogin():
  if request.method == 'POST':
    form = LoginModel()
    username = form.username.data
    password = form.password.data
    flag = form.validate_on_submit()
    if flag:
      user = DbUser().dbLogin(username, password)
      if user != []:
        session['username'] = user['name']
        session['userid'] = user['id']
        if user['avatar_url'] == '':
          session['avatar_url'] = '../static/img/avatars/default.png'
        else:
          session['avatar_url'] = user['avatar_url']
        return redirect('/')
      else:
        flash('用户名或密码错误')
        return redirect('/login')
  else:
    loginForm = LoginModel()
    return render_template('login.html', form=loginForm, )


@xmUserApi.route('/register', methods=['POST', 'GET'])
def xmRegister():
  if request.method == 'POST':
    form = RegisterModel()
    if form.validate_on_submit():
      username = form.username.data
      password = form.password.data
      try:
        DbUser().dbRegister(username, password)
        flash('注册成功')
        return redirect('/login')
      except:
        flash('注册失败，用户名已存在')
        return redirect('/register')
    else:
      flash('两次密码不一致')
      return redirect('/register')
  else:
    registerForm = RegisterModel()
    return render_template('register.html', registerForm=registerForm)


@xmUserApi.route('/logout', methods=['POST'])
def logout():
  session.clear()
  return redirect('/login')


@xmUserApi.route('/editUser', methods=['POST'])
def editUser():
  userId = session['userid']
  username = request.form['username']
  beforePas = request.form['beforePas']
  afterPas = request.form['afterPas']

  if beforePas != '' and afterPas != '':
    currentUsername = session['username']
    # 查询当前操作用户是否在数据库中且输入的原密码正确
    result = DbUser().dbLogin(currentUsername, beforePas)
    if result != []:
      try:
        DbUser().updateUserMes(username, userId, afterPas)
        session['username'] = username
        return redirect('/')
      except Exception as e:
        print(e)
        # flash('用户名已存在，编辑失败')
        # return redirect('/')
        return render_template('404.html', message='用户名已存在，编辑失败')

    else:
      # flash('原密码错误，编辑失败！')
      # return redirect('/')
      return render_template('404.html', message='原密码错误，编辑失败')

  else:
    try:
      DbUser().updateUserMes(username, userId)
      session['username'] = username
      return redirect('/')
    except Exception as e:
      print(e)
      # flash('用户名已存在，编辑失败')
      # return redirect('/')
      return render_template('404.html', message='用户名已存在，编辑失败')

