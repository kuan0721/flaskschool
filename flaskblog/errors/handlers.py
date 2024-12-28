# 導入 Flask Blueprint 和渲染模板功能
from flask import Blueprint, render_template

# 建立 Blueprint，用於處理錯誤頁面
errors = Blueprint('errors', __name__)

# 處理 404 錯誤（頁面未找到）
@errors.app_errorhandler(404)
def error_404(error):
    # 渲染自訂的 404 錯誤頁面模板，並返回 404 狀態碼
    return render_template('errors/404.html'), 404

# 處理 403 錯誤（禁止訪問）
@errors.app_errorhandler(403)
def error_403(error):
    # 渲染自訂的 403 錯誤頁面模板，並返回 403 狀態碼
    return render_template('errors/403.html'), 403

# 處理 500 錯誤（內部伺服器錯誤）
@errors.app_errorhandler(500)
def error_500(error):
    # 渲染自訂的 500 錯誤頁面模板，並返回 500 狀態碼
    return render_template('errors/500.html'), 500
