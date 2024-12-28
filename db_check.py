# 從flaskblog模塊中匯入應用實例和資料庫對象
from flaskblog import app, db
# 從flaskblog.models匯入User模型
from flaskblog.models import User

# 創建並推送應用上下文，這對於在Flask應用之外執行資料庫查詢非常重要
app.app_context().push()

# 查詢所有的用戶資料
users = User.query.all()

# 列印所有用戶的資料
print("所有用户:")
for user in users:
    print(f"{user.username} - {user.email}")
