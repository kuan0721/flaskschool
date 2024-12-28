import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from flaskblog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required


# 首頁路由
@app.route("/")
@app.route("/home")
def home():
    # 取得所有文章並顯示於首頁
    posts = Post.query.all()
    return render_template('home.html', posts=posts)

# 關於頁面路由
@app.route("/about")
def about():
    # 顯示關於頁面
    return render_template('about.html', title='About')

# 註冊頁面路由
@app.route("/register", methods=['GET', 'POST'])
def register():
    # 如果已登入，直接導向首頁
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    # 驗證表單資料是否有效
    if form.validate_on_submit():
        # 密碼加密處理後存入資料庫
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        # 註冊成功提示並跳轉登入頁面
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    # 顯示註冊表單
    return render_template('register.html', title='Register', form=form)

# 登入頁面路由
@app.route("/login", methods=['GET', 'POST'])
def login():
    # 已登入的用戶重定向到首頁
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    # 驗證登入資訊
    if form.validate_on_submit():
        # 驗證用戶郵件與密碼
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            # 登入成功並記住狀態
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')  # 檢查是否有原本要前往的頁面
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            # 登入失敗提示
            flash('Login Unsuccessful. Please check email and password', 'danger')
    # 顯示登入表單
    return render_template('login.html', title='Login', form=form)

# 登出路由
@app.route("/logout")
def logout():
    # 執行登出並導向首頁
    logout_user()
    return redirect(url_for('home'))

# 儲存圖片函數
def save_picture(form_picture):
    # 產生隨機檔名，避免檔名重複
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    # 縮小圖片尺寸以節省空間
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

# 用戶帳號頁面路由
@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    # 更新用戶帳號資訊
    form = UpdateAccountForm()
    if form.validate_on_submit():
        # 若上傳新頭像，儲存並更新
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        # 更新用戶名稱與電子郵件
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        # 預設表單值為當前用戶資訊
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    # 顯示帳號資訊頁面
    return render_template('account.html', title='Account', image_file=image_file, form=form)

# 新增文章路由
@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        # 新增文章到資料庫
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))
    # 顯示新增文章頁面
    return render_template('create_post.html', title='New Post', form=form, legend='New Post')

# 顯示單篇文章內容路由
@app.route("/post/<int:post_id>")
def post(post_id):
    # 根據 ID 顯示文章內容
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)

# 更新文章路由
@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    # 僅允許作者修改
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        # 更新文章內容
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        # 預設表單值為文章內容
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post', form=form, legend='Update Post')

# 刪除文章路由
@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    # 刪除指定文章
    post = Post.query.get_or_404(post_id)
    # 確保只有作者可以刪除
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))