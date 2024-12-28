# 導入必要的 Flask 模組和功能
from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from flaskblog import db
from flaskblog.models import Post
from flaskblog.posts.forms import PostForm

# 建立 Blueprint，用於組織與文章相關的路由
posts = Blueprint('posts', __name__)

# 新增文章的路由
@posts.route("/post/new", methods=['GET', 'POST'])
@login_required  # 確保用戶必須登入才能訪問此路由
def new_post():
    # 建立表單實例
    form = PostForm()
    # 驗證表單提交
    if form.validate_on_submit():
        # 創建新的文章實例並設置標題、內容和作者
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        # 將文章加入資料庫會話
        db.session.add(post)
        # 提交變更到資料庫
        db.session.commit()
        # 提示用戶文章已成功創建
        flash('Your post has been created!', 'success')
        # 重定向到主頁
        return redirect(url_for('main.home'))
    # 渲染文章創建模板
    return render_template('create_post.html', title='New Post',
                           form=form, legend='New Post')

# 顯示特定文章的路由
@posts.route("/post/<int:post_id>")
def post(post_id):
    # 根據文章 ID 查詢文章，若不存在則返回 404 錯誤
    post = Post.query.get_or_404(post_id)
    # 建立表單實例
    form = PostForm()
    # 渲染顯示文章的模板
    return render_template('post.html', title=post.title, post=post, form=form)

# 更新文章的路由
@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required  # 確保用戶必須登入才能訪問此路由
def update_post(post_id):
    # 根據文章 ID 查詢文章，若不存在則返回 404 錯誤
    post = Post.query.get_or_404(post_id)
    # 確保當前用戶是文章的作者，否則返回 403 錯誤
    if post.author != current_user:
        abort(403)
    # 建立表單實例
    form = PostForm()
    # 驗證表單提交
    if form.validate_on_submit():
        # 更新文章標題與內容
        post.title = form.title.data
        post.content = form.content.data
        # 提交變更到資料庫
        db.session.commit()
        # 提示用戶文章已成功更新
        flash('Your post has been updated!', 'success')
        # 重定向到文章詳細頁面
        return redirect(url_for('posts.post', post_id=post.id))
    # 若為 GET 請求，則將現有內容填入表單
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    # 渲染更新文章的模板
    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post')

# 刪除文章的路由
@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required  # 確保用戶必須登入才能訪問此路由
def delete_post(post_id):
    # 根據文章 ID 查詢文章，若不存在則返回 404 錯誤
    post = Post.query.get_or_404(post_id)
    # 確保當前用戶是文章的作者，否則返回 403 錯誤
    if post.author != current_user:
        abort(403)
    # 從資料庫刪除文章
    db.session.delete(post)
    # 提交變更到資料庫
    db.session.commit()
    # 提示用戶文章已刪除
    flash('Your post has been deleted!', 'success')
    # 重定向到主頁
    return redirect(url_for('main.home'))
