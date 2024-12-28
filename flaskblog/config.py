import os  # 導入作業系統模組，用於存取環境變數

class Config:
    # 設定應用程式的密鑰，從環境變數獲取，如果沒有則使用預設值
    # 這個密鑰用於加密 session 資料和其他安全相關功能
    SECRET_KEY = os.environ.get('SECRET_KEY', '5791628bb0b13ce0c676dfde280ba245')

    # 設定資料庫連線字串，從環境變數獲取，如果沒有則使用 SQLite 資料庫
    # SQLite 資料庫檔案將存儲在 site.db
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI', 'sqlite:///site.db')
    
    # 關閉 SQLAlchemy 的修改追蹤功能
    # 這可以提升應用程式效能，因為不需要追蹤每次資料庫的修改
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Gmail SMTP 伺服器設定
    MAIL_SERVER = 'smtp.googlemail.com'  # 指定 Gmail 的 SMTP 伺服器
    MAIL_PORT = 587  # 使用 TLS 的標準 SMTP 埠口
    MAIL_USE_TLS = True  # 啟用 TLS 加密

    # 郵件認證資訊，從環境變數獲取
    # 如果環境變數未設定，則使用預設值
    MAIL_USERNAME = os.environ.get('EMAIL_USER', 'default_email@example.com')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS', 'default_password')