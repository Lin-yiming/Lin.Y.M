from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import yfinance as yf

app = Flask(__name__)

# 設定 LineBot 的 Channel Access Token 和 Channel Secret
line_bot_api = LineBotApi('p7Cmx4BoCNt0LD2kgdfeOe75gPTHF3sLGrR099KNnnrTdJK5RBzaAxB58kQs7XWmOlKesfndO2M6Nl9q4SeYn7+700i3CqocUHqzN+TeBZoCiktCjDL5w9fLfW9ed++jljaF0zYUhp620TxhWDkeTwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('980186763ec26279c6c95254f44a4ae8')
line_bot_api.push_message('Uae4d95a8996273cbd5fd013544cb3d5a', TextSendMessage(text='你可以開始了'))

def fetch_stock_data(symbol, start_date, end_date):
    """
    從 Yahoo Finance 獲取指定股票在指定時間範圍內的數據。
    
    Args:
        symbol (str): 股票代號。
        start_date (str): 開始日期，格式為 'YYYY-MM-DD'。
        end_date (str): 結束日期，格式為 'YYYY-MM-DD'。
    
    Returns:
        pandas.DataFrame: 包含獲取的股票數據的 DataFrame。
    """
    # 獲取股票數據
    data = yf.download(symbol, start=start_date, end=end_date)
    return data

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text = event.message.text
    if text.startswith("/stock"):
        tokens = text.split()
        if len(tokens) != 4:
            reply_text = "請輸入正確格式：/stock [股票代號] [開始日期] [結束日期]"
        else:
            symbol = tokens[1]
            start_date = tokens[2]
            end_date = tokens[3]
            try:
                stock_data = fetch_stock_data(symbol, start_date, end_date)
                average_close_price = stock_data['Close'].mean()
                reply_text = f"{symbol} 在 {start_date} 到 {end_date} 期間的收盤價平均值為 {average_close_price:.2f}"
            except Exception as e:
                reply_text = f"發生錯誤：{e}"
    else:
        reply_text = "請輸入正確指令：/stock [股票代號] [開始日期] [結束日期]"
    
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_text)
    )

if __name__ == "__main__":
    app.run()
