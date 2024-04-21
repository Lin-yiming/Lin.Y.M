from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, ImageMessage
import requests

app = Flask(__name__)

# 設定 Line Bot 的 Channel Access Token 和 Channel Secret
line_bot_api = LineBotApi('p7Cmx4BoCNt0LD2kgdfeOe75gPTHF3sLGrR099KNnnrTdJK5RBzaAxB58kQs7XWmOlKesfndO2M6Nl9q4SeYn7+700i3CqocUHqzN+TeBZoCiktCjDL5w9fLfW9ed++jljaF0zYUhp620TxhWDkeTwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('980186763ec26279c6c95254f44a4ae8')

# 接收 Line Bot 的訊息事件
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    # 簽名驗證
    try:
        handler.handle(request.data.decode('utf-8'), signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

# 處理圖片訊息
@handler.add(MessageEvent, message=ImageMessage)
def handle_image_message(event):
    message_content = line_bot_api.get_message_content(event.message.id)
    image = message_content.content

    # 將圖片上傳到 Imgur
    imgur_url = upload_to_imgur(image)
    reply_message = f"Your image is uploaded to {imgur_url}"
    line_bot_api.reply_message(event.reply_token, TextMessage(text=reply_message))

def upload_to_imgur(image):
    client_id = 'd6f8a94c37e2b83'
    headers = {'Authorization': f'Client-ID {client_id}'}
    url = 'https://api.imgur.com/3/image'
    files = {'image': image}
    response = requests.post(url, headers=headers, files=files)
    data = response.json()
    imgur_url = data['data']['link']
    return imgur_url

if __name__ == "__main__":
    app.run(debug=True)
