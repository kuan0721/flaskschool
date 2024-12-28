# 導入 Flask-WTF 和 WTForms 模組
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

# 定義文章表單類別
class PostForm(FlaskForm):
    # 標題欄位，要求必填
    title = StringField('Title', validators=[DataRequired()])
    # 內容欄位，要求必填
    content = TextAreaField('Content', validators=[DataRequired()])
    # 提交按鈕
    submit = SubmitField('Post')
