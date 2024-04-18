# -*- coding: utf-8 -*-
"""
Created on Wed Jun  2 21:16:35 2021

@author: Ivan
版權屬於「行銷搬進大程式」所有，若有疑問，可聯絡ivanyang0606@gmail.com

Line Bot聊天機器人
第三章 互動回傳功能
傳送貼圖StickerSendMessage
"""
#載入LineBot所需要的套件
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import re
import yfinance as yf  # 新增的模塊

app = Flask(__name__)

# 必須放上自己的Channel Access Token
line_bot_api = LineBotApi('p7Cmx4BoCNt0LD2kgdfeOe75gPTHF3sLGrR099KNnnrTdJK5RBzaAxB58kQs7XWmOlKesfndO2M6Nl9q4SeYn7+700i3CqocUHqzN+TeBZoCiktCjDL5w9fLfW9ed++jljaF0zYUhp620TxhWDkeTwdB04t89/1O/w1cDnyilFU=')
# 必須放上自己的Channel Secret
handler = WebhookHandler('980186763ec26279c6c95254f44a4ae8')

line_bot_api.push_message('Uae4d95a8996273cbd5fd013544cb3d5a', TextSendMessage(text='你可以開始了'))

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

# 股票數據獲取功能
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

#訊息傳遞區塊
##### 基本上程式編輯都在這個function #####
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = text=event.message.text
    if re.match('睡',message):
        # 貼圖查詢：https://developers.line.biz/en/docs/messaging-api/sticker-list/#specify-sticker-in-message-object
        sticker_message = StickerSendMessage(
            package_id='1',
            sticker_id='1'
        )
        line_bot_api.reply_message(event.reply_token, sticker_message)
    elif re.match('好', message):
        # 新增第二個貼圖
        sticker_message = StickerSendMessage(
            package_id='1',
            sticker_id='2'
        )
        line_bot_api.reply_message(event.reply_token, sticker_message)
    elif re.match('驚', message):
        # 新增第三個貼圖
        sticker_message = StickerSendMessage(
            package_id='1',
            sticker_id='3'
        )
        line_bot_api.reply_message(event.reply_token, sticker_message)
    # 繼續新增其他貼圖...
    elif re.match('請求', message):
        sticker_message = StickerSendMessage(
            package_id='1',
            sticker_id='4'
        )
        line_bot_api.reply_message(event.reply_token, sticker_message)
    elif re.match('美好', message):
        sticker_message = StickerSendMessage(
            package_id='1',
            sticker_id='5'
        )
        line_bot_api.reply_message(event.reply_token, sticker_message)
    elif re.match('生氣', message):
        sticker_message = StickerSendMessage(
            package_id='1',
            sticker_id='6'
        )
        line_bot_api.reply_message(event.reply_token, sticker_message)
    elif re.match('是你', message):
        sticker_message = StickerSendMessage(
            package_id='1',
            sticker_id='7'
        )
        line_bot_api.reply_message(event.reply_token, sticker_message)
    elif re.match('怕', message):
        sticker_message = StickerSendMessage(
            package_id='1',
            sticker_id='8'
        )
        line_bot_api.reply_message(event.reply_token, sticker_message)
    elif re.match('衰', message):
        sticker_message = StickerSendMessage(
            package_id='1',
            sticker_id='9'
        )
        line_bot_api.reply_message(event.reply_token, sticker_message)
    elif re.match('笑', message):
        sticker_message = StickerSendMessage(
            package_id='1',
            sticker_id='10'
        )
        line_bot_api.reply_message(event.reply_token, sticker_message)
    elif re.match('關鍵字',message):
        flex_message = TextSendMessage(text='以下有雷，請小心',
                               quick_reply=QuickReply(items=[
                                   QuickReplyButton(action=MessageAction(label="關鍵價位", text="關鍵！")),
                                   QuickReplyButton(action=MessageAction(label="密碼", text="密碼！")),
                                   QuickReplyButton(action=MessageAction(label="木沐", text="木沐！")),
                                   QuickReplyButton(action=MessageAction(label="重要筆記", text="重要！！")),
                                   QuickReplyButton(action=MessageAction(label="早安", text="早安！")),
                                   QuickReplyButton(action=MessageAction(label="歡迎", text="歡迎！")),
                                   QuickReplyButton(action=MessageAction(label="貼圖", text="笑！")),                               
                               ]))
        line_bot_api.reply_message(event.reply_token, flex_message)
    elif re.match('股票', message):  # 新增對股票查詢的回應
        try:
            # 指定股票代號和時間範圍
            symbol = "2317.TW"  # 代號，你可以更改為其他股票代號
            start_date = '2023-04-01'
            end_date = '2024-04-10'
            
            # 獲取股票數據
            stock_data = fetch_stock_data(symbol, start_date, end_date)
            
            # 計算收盤價的平均值
            average_close_price = stock_data['Close'].mean()
            
            # 準備回覆訊息
            reply_message = f"收盤價的平均值: {average_close_price}"
            
            # 回覆訊息
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_message))
        except Exception as e:
            # 若發生錯誤，回覆錯誤訊息
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=str(e)))
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(message))
       
#主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
