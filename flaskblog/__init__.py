# 匯入必要的模組與函式
from flask import Flask  # 建立 Flask 應用程式實例
from flask_sqlalchemy import SQLAlchemy  # 提供 SQL 資料庫操作功能
from flask_bcrypt import Bcrypt  # 提供密碼加密與驗證功能
from flask_login import LoginManager  # 管理用戶登入狀態與權限
from flask_mail import Mail  # 提供電子郵件發送功能
from flaskblog.config import Config  # 匯入自定義設定檔

# 初始化 Flask 擴展模組
db = SQLAlchemy()  # 資料庫處理
bcrypt = Bcrypt()  # 密碼加密與解密
login_manager = LoginManager()  # 登入管理
login_manager.login_view = 'users.login'  # 設置未登入時的重定向頁面
login_manager.login_message_category = 'info'  # 設置登入提示訊息的分類樣式
mail = Mail()  # 電子郵件服務

# 建立應用程式的工廠函數 (Factory Function)
def create_app(config_class=Config):
    # 建立 Flask 應用程式實例
    app = Flask(__name__)

    # 將應用程式配置從設定檔載入
    app.config.from_object(Config)

    # 初始化擴展功能模組
    db.init_app(app)  # 初始化 SQLAlchemy 資料庫
    bcrypt.init_app(app)  # 初始化 Bcrypt 加密功能
    login_manager.init_app(app)  # 初始化登入管理器
    mail.init_app(app)  # 初始化電子郵件服務

    # 匯入與註冊 Blueprint 模組
    from flaskblog.users.routes import users  # 用戶管理的路由模組
    from flaskblog.posts.routes import posts  # 文章管理的路由模組
    from flaskblog.main.routes import main  # 主頁面與靜態內容的路由模組
    from flaskblog.errors.handlers import errors  # 錯誤處理的路由模組

    # 註冊 Blueprint 到應用程式
    app.register_blueprint(users)  # 註冊用戶管理路由
    app.register_blueprint(posts)  # 註冊文章管理路由
    app.register_blueprint(main)  # 註冊主頁面路由
    app.register_blueprint(errors)  # 註冊錯誤處理路由

    # 返回已配置好的應用程式實例
    return app
