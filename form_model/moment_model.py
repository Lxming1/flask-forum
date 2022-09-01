from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import Length, DataRequired

class MomentModel(FlaskForm):
  content = TextAreaField(
    validators=[
      DataRequired()
    ],
    render_kw={
      "placeholder": "说些什么吧...",
      'autocomplete': "off",
      "rows": "10",
      "cols": "100",
      "class": "formMomentContent"
    }
  )

  labels = StringField(
    render_kw={
      "class": 'textfield formMomentLabels',
      "placeholder": "不同标签用空格分开",
      'autocomplete': "off",
    }
  )
  submit = SubmitField(label='提交', render_kw={
    'class': 'btnDefault subEditMoment'
  })

