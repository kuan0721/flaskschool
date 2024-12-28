# 從 flaskblog 模組匯入 create_app 函數，用於創建 Flask 應用程式
from flaskblog import create_app

# 呼叫 create_app 函數來創建 Flask 應用程式實例，並將其指派給變數 app
app = create_app()

# 確保程式是直接執行而非被匯入執行時，執行以下程式碼區塊
if __name__ == '__main__':
    # 啟動 Flask 開發伺服器，啟用偵錯模式以便於開發過程中即時查看錯誤與變更
    app.run(debug=True)
