from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import Length, DataRequired, EqualTo


class LoginModel(FlaskForm):
  username = StringField(
    validators=[
      DataRequired()
    ],
    render_kw={ "placeholder": "请输入用户名", "autocomplete": "off"}
  )
  password = PasswordField(
    validators=[
      DataRequired()
    ],
    render_kw={"placeholder": "请输入密码", "autocomplete": "off"}
  )
  submit = SubmitField('登录', render_kw={
    'class': 'btnDefault loginBtn'
  })


class RegisterModel(FlaskForm):
  username = StringField(
    validators=[
      Length(min=3, max=10, message="用户名长度有问题"),
      DataRequired()
    ],
    render_kw={"placeholder": "请输入用户名", "autocomplete": "off"}
  )
  password = PasswordField(
    validators=[
      Length(min=6, max=20),
      DataRequired()
    ],
    render_kw={"placeholder": "请输入密码", "autocomplete": "off"}
  )
  password1 = PasswordField(
    validators=[
      Length(min=6, max=20),
      DataRequired(),
      EqualTo('password', '密码填入的不一致')
    ],
    render_kw={ "placeholder": "请再次输入密码"}
  )
  submit = SubmitField('注册', render_kw={
    'class': 'btnDefault',
    "autocomplete": "off"
  })