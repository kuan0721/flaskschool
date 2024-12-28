# 匯入必要模組
import os  # 用於操作檔案與路徑
import secrets  # 用於生成隨機安全字串
from PIL import Image  # 用於處理圖片
from flask import url_for, current_app  # Flask 的 URL 與應用程式上下文功能
from flask_mail import Message  # Flask-Mail 模組用於發送電子郵件
from flaskblog import mail  # 從應用程式中匯入已配置的電子郵件功能


def save_picture(form_picture):
    # 生成隨機檔名，避免檔案名稱重複
    random_hex = secrets.token_hex(8)  # 建立 8 位元隨機十六進位字串
    _, f_ext = os.path.splitext(form_picture.filename)  # 分離檔名與副檔名
    picture_fn = random_hex + f_ext  # 新檔名 = 隨機字串 + 原檔案副檔名
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)  # 建立儲存路徑

    # 設定輸出圖片大小
    output_size = (125, 125)  # 將圖片縮放為 125x125 像素
    i = Image.open(form_picture)  # 開啟圖片檔案
    i.thumbnail(output_size)  # 縮放圖片大小
    i.save(picture_path)  # 儲存處理後的圖片到指定路徑

    # 回傳檔案名稱以便存入資料庫
    return picture_fn

def send_reset_email(user):
    # 生成重設密碼的令牌
    token = user.get_reset_token()

    # 建立電子郵件訊息內容
    msg = Message('Password Reset Request',  # 電子郵件標題
                  sender='noreply@demo.com',  # 發件人地址
                  recipients=[user.email])  # 收件人地址 (從用戶資料中取得)

    # 設定電子郵件內容
    msg.body = f'''To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}  # 使用 URL 生成重設密碼連結

If you did not make this request then simply ignore this email and no changes will be made.
'''

    # 發送電子郵件
    mail.send(msg)
