from flaskblog import db
from flaskblog.models import User
from flask_bcrypt import Bcrypt
from flaskblog import app

# 初始化Bcrypt實例
bcrypt = Bcrypt(app)

# 創建資料庫和表格
with app.app_context():
    # 這會創建所有的資料表
    db.create_all()

    # 如果資料庫中沒有用戶，可以新增一個測試用戶
    hashed_password = bcrypt.generate_password_hash('12345678').decode('utf-8')
    test_user = User(username='kuan', email='kuan@blog.com', password=hashed_password)
    
    # 將測試用戶添加到資料庫會話中
    db.session.add(test_user)
    # 提交資料庫會話，保存更改
    db.session.commit()

    # 輸出提示消息，確認測試用戶已創建
    print("Test user created.")