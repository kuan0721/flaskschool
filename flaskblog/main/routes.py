# 導入必要的 Flask 模組和資料模型
from flask import render_template, request, Blueprint
from flaskblog.models import Post

# 建立 Blueprint，用於組織主要路由
main = Blueprint('main', __name__)

# 主頁面路由
@main.route("/")  # 根路徑
@main.route("/home")  # /home 路徑
def home():
    # 從請求參數中獲取頁碼，預設為第 1 頁，並將其轉換為整數
    page = request.args.get('page', 1, type=int)
    # 查詢文章資料，按發佈日期降序排序，每頁顯示 5 篇文章
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    # 渲染主頁模板，並將查詢結果傳入模板中
    return render_template('home.html', posts=posts)

# 關於頁面的路由
@main.route("/about")
def about():
    # 渲染關於頁面的模板，並傳入標題
    return render_template('about.html', title='About')
