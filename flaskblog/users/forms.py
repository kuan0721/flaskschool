# 從 Flask-WTF 和 WTForms 導入所需的類和函式
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from flaskblog.models import User


# 註冊表單
class RegistrationForm(FlaskForm):
    # 用戶名字段，要求填寫且長度在 2 到 20 之間
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    # 郵箱字段，要求填寫且必須是有效的郵箱格式
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    # 密碼字段，要求填寫
    password = PasswordField('Password', validators=[DataRequired()])
    # 確認密碼字段，要求填寫且必須與密碼字段相同
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    # 提交按鈕，顯示為 "Sign Up"
    submit = SubmitField('Sign Up')

    # 用戶名的驗證函式，確保用戶名未被註冊
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    # 郵箱的驗證函式，確保郵箱未被註冊
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


# 登錄表單
class LoginForm(FlaskForm):
    # 郵箱字段，要求填寫且必須是有效的郵箱格式
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    # 密碼字段，要求填寫
    password = PasswordField('Password', validators=[DataRequired()])
    # 記住我選項（復選框）
    remember = BooleanField('Remember Me')
    # 提交按鈕，顯示為 "Login"
    submit = SubmitField('Login')


# 更新帳戶表單
class UpdateAccountForm(FlaskForm):
    # 用戶名字段，要求填寫且長度在 2 到 20 之間
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    # 郵箱字段，要求填寫且必須是有效的郵箱格式
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    # 頭像上傳字段，只允許上傳 jpg 和 png 格式的圖片
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    # 提交按鈕，顯示為 "Update"
    submit = SubmitField('Update')

    # 用戶名的驗證函式，確保用戶名未被其他用戶使用
    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    # 郵箱的驗證函式，確保郵箱未被其他用戶使用
    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')


# 密碼重置請求表單
class RequestResetForm(FlaskForm):
    # 郵箱字段，要求填寫且必須是有效的郵箱格式
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    # 提交按鈕，顯示為 "Request Password Reset"
    submit = SubmitField('Request Password Reset')

    # 郵箱的驗證函式，確保郵箱已經註冊
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')


# 密碼重置表單
class ResetPasswordForm(FlaskForm):
    # 密碼字段，要求填寫
    password = PasswordField('Password', validators=[DataRequired()])
    # 確認密碼字段，要求填寫且必須與密碼字段相同
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    # 提交按鈕，顯示為 "Reset Password"
    submit = SubmitField('Reset Password')
