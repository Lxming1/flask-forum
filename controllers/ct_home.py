import json

from flask import render_template, Blueprint, session, request, flash
from werkzeug.utils import redirect

from db.db_home import DbHome
from db.db_moment import DbMoment
from form_model.moment_model import MomentModel

xmHomeApi = Blueprint('home', __name__)

@xmHomeApi.route('/')
@xmHomeApi.route('/home')
def xmHome():
  try:
    if session['username'] == '':
      return redirect('/login')
    else:
      moment = DbHome().getMomment()
      session['moment'] = json.dumps(moment, default=str)
      return showHome(moment)
  except Exception as e:
    print(e)
    return redirect('/login')

def showHome(moment):
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
  return render_template('main_cpn/home.html', moment=moment, momentForm=momentForm)


@xmHomeApi.route('/search', methods=['POST'])
def xmSearch():
  content = request.form['content']
  selectItem = request.form['searchItem']
  result = []
  if selectItem == 'username':
    result = DbMoment().searchMomentByUser(content)
  elif selectItem == 'label':
    result = DbMoment().searchMomentByLabel(content)
  else:
    result = DbMoment().searchMoment(content)

  return showHome(result)


@xmHomeApi.route('/createMoment', methods=['POST'])
def xmCreateMoment():
  momentForm = MomentModel()
  if momentForm.validate_on_submit():
    userId = int(session['userid'])
    content = momentForm.content.data
    labelList = momentForm.labels.data.split(' ')
    labelList = list(set(labelList))
    labelIds = handleLabels(labelList)
    momentId = DbMoment().insertMoment(content, userId)

    for item in labelIds:
      DbMoment().insertMomentAndLabel(momentId, item)

    # session['message'] = '发布成功'
    return redirect('/')

def not_empty2(s):
  return s['name'] and s['name'].strip()


def not_empty1(s):
  return s and s.strip()


def handleLabels(labelList):
  existList = []
  labelList = list(filter(not_empty1, labelList))

  for item in labelList:
    existList.append(DbMoment().searchLabel(item))

  existList = list(filter(not_empty2, filter(None, existList)))
  name = []
  for item in existList:
    name.append(item['name'])
  labelIds = []
  noExistList = [x for x in labelList if x not in name]
  for item in noExistList:
    labelIds.append(DbMoment().insertLabel(item))

  for item in existList:
    labelIds.append(item['id'])

  return labelIds


@xmHomeApi.route('/addComment/<id>', methods=['POST'])
def addComment(id):
  userId = session['userid']
  path = request.form['path']
  content = request.form['commentContent']
  DbMoment().addComment(content, id, userId)
  # session['message'] = '发布成功'
  return redirect(path)

@xmHomeApi.route('/replyComment/<momentId>/<commentId>', methods=['POST'])
def replyComment(momentId, commentId):
  userId = session['userid']
  path = request.form['path']
  content = request.form['content']
  DbMoment().addReplyComment(content, userId, momentId, commentId)
  # session['message'] = '发布成功'
  return redirect(path)


@xmHomeApi.route('/delComment/<commentId>', methods=['POST'])
def delCommentInProfile(commentId):
  path = request.form['path']
  DbMoment().delComment(commentId)
  # session['message'] = '删除成功'
  return redirect(path)