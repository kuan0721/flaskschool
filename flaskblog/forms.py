from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskblog.models import User


# 註冊表單類別
class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])  # 用戶名稱欄位，需提供且長度介於2到20之間
    email = StringField('Email',
                        validators=[DataRequired(), Email()])  # 電子郵件欄位，需提供且格式需為有效電子郵件
    password = PasswordField('Password', validators=[DataRequired()])  # 密碼欄位，需提供
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])  # 確認密碼欄位，必須與密碼欄位一致
    submit = SubmitField('Sign Up')  # 提交按鈕

    # 用戶名驗證，檢查是否已經有相同的用戶名
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    # 電子郵件驗證，檢查是否已經有相同的電子郵件
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


# 登入表單類別
class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])  # 電子郵件欄位，需提供且格式需為有效電子郵件
    password = PasswordField('Password', validators=[DataRequired()])  # 密碼欄位，需提供
    remember = BooleanField('Remember Me')  # 記住我選項
    submit = SubmitField('Login')  # 提交按鈕


# 更新帳戶表單類別
class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])  # 用戶名稱欄位，需提供且長度介於2到20之間
    email = StringField('Email',
                        validators=[DataRequired(), Email()])  # 電子郵件欄位，需提供且格式需為有效電子郵件
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])  # 上傳頭像圖片欄位，只允許 jpg 和 png 格式
    submit = SubmitField('Update')  # 提交按鈕

    # 用戶名驗證，檢查是否已經有相同的用戶名
    def validate_username(self, username):
        if username.data != current_user.username:  # 如果更改了用戶名稱，則檢查是否已存在
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    # 電子郵件驗證，檢查是否已經有相同的電子郵件
    def validate_email(self, email):
        if email.data != current_user.email:  # 如果更改了電子郵件，則檢查是否已存在
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')


# 文章表單類別
class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])  # 文章標題欄位，需提供
    content = TextAreaField('Content', validators=[DataRequired()])  # 文章內容欄位，需提供
    submit = SubmitField('Post')  # 提交按鈕
