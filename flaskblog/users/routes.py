# 從 Flask 框架中導入所需的模組和函式
from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from flaskblog import db, bcrypt
from flaskblog.models import User, Post
from flaskblog.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                                   RequestResetForm, ResetPasswordForm)
from flaskblog.users.utils import save_picture, send_reset_email

# 創建一個 Blueprint，用於用戶相關的路由
users = Blueprint('users', __name__)


@users.route("/register", methods=['GET', 'POST'])
def register():
    """
    用戶註冊路由。
    支持 GET 和 POST 請求。
    """
    # 如果用戶已經登入，重定向到主頁
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    
    # 創建註冊表單實例
    form = RegistrationForm()
    
    # 如果表單提交且驗證通過
    if form.validate_on_submit():
        # 對密碼進行哈希加密
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        # 創建新的用戶實例
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        # 將用戶添加到數據庫會話
        db.session.add(user)
        # 提交會話，將用戶保存到數據庫
        db.session.commit()
        # 顯示成功訊息
        flash('Your account has been created! You are now able to log in', 'success')
        # 重定向到登錄頁面
        return redirect(url_for('users.login'))
    
    # 如果是 GET 請求或表單未通過驗證，渲染註冊頁面
    return render_template('register.html', title='Register', form=form)


@users.route("/login", methods=['GET', 'POST'])
def login():
    """
    用戶登錄路由。
    支持 GET 和 POST 請求。
    """
    # 如果用戶已經登入，重定向到主頁
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    
    # 創建登錄表單實例
    form = LoginForm()
    
    # 如果表單提交且驗證通過
    if form.validate_on_submit():
        # 根據郵箱查找用戶
        user = User.query.filter_by(email=form.email.data).first()
        # 檢查用戶存在且密碼正確
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            # 登錄用戶
            login_user(user, remember=form.remember.data)
            # 獲取下一個頁面的 URL（如果有）
            next_page = request.args.get('next')
            # 重定向到下一頁或主頁
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            # 登錄失敗，顯示錯誤訊息
            flash('Login Unsuccessful. Please check email and password', 'danger')
    
    # 如果是 GET 請求或表單未通過驗證，渲染登錄頁面
    return render_template('login.html', title='Login', form=form)


@users.route("/logout")
def logout():
    """
    用戶登出路由。
    """
    # 登出當前用戶
    logout_user()
    # 重定向到主頁
    return redirect(url_for('main.home'))


@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    """
    用戶帳戶管理路由。
    需要用戶登入才能訪問。
    支持 GET 和 POST 請求。
    """
    # 創建更新帳戶表單實例
    form = UpdateAccountForm()
    
    # 如果表單提交且驗證通過
    if form.validate_on_submit():
        # 如果用戶上傳了新圖片
        if form.picture.data:
            # 保存圖片並獲取文件名
            picture_file = save_picture(form.picture.data)
            # 更新用戶的圖片文件名
            current_user.image_file = picture_file
        # 更新用戶名和郵箱
        current_user.username = form.username.data
        current_user.email = form.email.data
        # 提交更改到數據庫
        db.session.commit()
        # 顯示成功訊息
        flash('Your account has been updated!', 'success')
        # 重定向到帳戶頁面以避免表單重新提交
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        # 如果是 GET 請求，預填充表單字段
        form.username.data = current_user.username
        form.email.data = current_user.email
    
    # 獲取用戶頭像的 URL
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    # 渲染帳戶頁面
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)


@users.route("/user/<string:username>")
def user_posts(username):
    """
    顯示特定用戶的所有帖子。
    """
    # 獲取頁碼，默認為 1
    page = request.args.get('page', 1, type=int)
    # 根據用戶名查找用戶，若不存在則返回 404
    user = User.query.filter_by(username=username).first_or_404()
    # 查詢該用戶的所有帖子，按日期降序排列，並進行分頁
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
    # 渲染用戶帖子頁面
    return render_template('user_posts.html', posts=posts, user=user)


@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    """
    請求重置密碼的路由。
    支持 GET 和 POST 請求。
    """
    # 如果用戶已經登入，重定向到主頁
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    
    # 創建重置請求表單實例
    form = RequestResetForm()
    
    # 如果表單提交且驗證通過
    if form.validate_on_submit():
        # 根據郵箱查找用戶
        user = User.query.filter_by(email=form.email.data).first()
        # 發送重置郵件
        send_reset_email(user)
        # 顯示提示訊息
        flash('An email has been sent with instructions to reset your password.', 'info')
        # 重定向到登錄頁面
        return redirect(url_for('users.login'))
    
    # 如果是 GET 請求或表單未通過驗證，渲染重置請求頁面
    return render_template('reset_request.html', title='Reset Password', form=form)


@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    """
    使用令牌重置密碼的路由。
    支持 GET 和 POST 請求。
    """
    # 如果用戶已經登入，重定向到主頁
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    
    # 驗證令牌並獲取用戶
    user = User.verify_reset_token(token)
    
    # 如果令牌無效或已過期，顯示警告訊息並重定向到重置請求頁面
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    
    # 創建重置密碼表單實例
    form = ResetPasswordForm()
    
    # 如果表單提交且驗證通過
    if form.validate_on_submit():
        # 對新密碼進行哈希加密
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        # 更新用戶的密碼
        user.password = hashed_password
        # 提交更改到數據庫
        db.session.commit()
        # 顯示成功訊息
        flash('Your password has been updated! You are now able to log in', 'success')
        # 重定向到登錄頁面
        return redirect(url_for('users.login'))
    
    # 如果是 GET 請求或表單未通過驗證，渲染重置密碼頁面
    return render_template('reset_token.html', title='Reset Password', form=form)
