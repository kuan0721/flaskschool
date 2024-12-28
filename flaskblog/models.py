# 匯入必要模組與函式
from datetime import datetime  # 用於處理日期與時間
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer  # 用於產生與驗證安全令牌
from flask import current_app  # 提供 Flask 應用程式的上下文配置
from flaskblog import db, login_manager  # 資料庫與登入管理
from flask_login import UserMixin  # 提供登入功能的輔助類別

# 登入管理器的使用者加載函數
@login_manager.user_loader
def load_user(user_id):
    # 根據用戶 ID 從資料庫中取得用戶資料
    return User.query.get(int(user_id))

# 使用者資料表模型
class User(db.Model, UserMixin):
    # 定義資料表欄位
    id = db.Column(db.Integer, primary_key=True)  # 唯一標識符
    username = db.Column(db.String(20), unique=True, nullable=False)  # 用戶名稱，必須唯一且不可為空
    email = db.Column(db.String(120), unique=True, nullable=False)  # 電子郵件，必須唯一且不可為空
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')  # 頭像圖片，預設為 default.jpg
    password = db.Column(db.String(60), nullable=False)  # 使用哈希加密後的密碼
    posts = db.relationship('Post', backref='author', lazy=True)  # 與文章模型的關聯，一對多關係

    # 產生重設密碼的令牌
    def get_reset_token(self, expires_sec=1800):
        # 使用應用程式的 SECRET_KEY 加密令牌，並設定有效時間（預設為 1800 秒 = 30 分鐘）
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')  # 生成並返回加密令牌

    # 驗證重設密碼的令牌
    @staticmethod
    def verify_reset_token(token):
        # 使用相同的 SECRET_KEY 解密令牌
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']  # 解析令牌並取得用戶 ID
        except:
            return None  # 若解析失敗，返回 None
        return User.query.get(user_id)  # 根據 ID 取得用戶物件

    # 定義物件表示形式，便於偵錯或日誌記錄
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

# 文章資料表模型
class Post(db.Model):
    # 定義資料表欄位
    id = db.Column(db.Integer, primary_key=True)  # 唯一標識符
    title = db.Column(db.String(100), nullable=False)  # 文章標題，不可為空
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)  # 發布日期，預設為當前 UTC 時間
    content = db.Column(db.Text, nullable=False)  # 文章內容，不可為空
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # 外鍵，參照 user 表的 id 欄位

    # 定義物件表示形式
    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"
