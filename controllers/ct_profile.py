from flask import session, render_template, Blueprint, redirect, flash, request

from controllers.ct_home import handleLabels
from db.db_moment import DbMoment
from form_model.moment_model import MomentModel

xmProfileApi = Blueprint('profile', __name__)

@xmProfileApi.route('/profile', methods=['GET'])
def xmProfile():
  if session['userid'] == '':
    return redirect('/login')
  userId = session['userid']
  moment = DbMoment().profileMoment(userId)
  for item in moment:
    item['author'] = eval(item['author'])
    if item['labels'] is None:
      item['labels'] = []
    else:
      item['labels'] = eval(item['labels'])

    commentList = DbMoment().showComments(item['id'])
    for item1 in commentList:
      item1['author'] = eval(item1['author'])

    item['commentList'] = commentList

  momentForm = MomentModel()
  return render_template('main_cpn/profile.html', moment=moment, momentForm=momentForm)

@xmProfileApi.route('/editMoment/<momentId>', methods=['POST'])
def editMoment(momentId):
  momentForm = MomentModel()
  userId = int(session['userid'])
  content = momentForm.content.data

  beforeLabel = request.form['beforeLabel'].split(' ')
  afterLabel = request.form['afterLabel'].split(' ')

  shouldDel = (list(set(beforeLabel) - set(afterLabel)))
  shouldAdd = list(set(afterLabel) - set(beforeLabel))

  DbMoment().editMoment(content, userId, momentId)

  shouldDelIds = []

  for item in shouldDel:
    if item != '':
      shouldDelIds.append(DbMoment().getLabelId(item))

  labelIds = handleLabels(shouldAdd)

  for item in shouldDelIds:
    DbMoment().delMomentAndLabel(momentId, item)

  for item in labelIds:
    DbMoment().insertMomentAndLabel(momentId, item)

  # session['message'] = '编辑成功'
  return redirect('/profile')


@xmProfileApi.route('/delMoment/<momentId>', methods=['POST'])
def delMoment(momentId):
  DbMoment().delMoment(momentId)
  return redirect('/profile')