import os


class Config:
    # 安全性設定
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your_secret_key')

    # 資料庫設定
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI', 'sqlite:///site.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # 避免效能警告

    # 郵件設定
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER', 'default_email@example.com')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS', 'default_password')
