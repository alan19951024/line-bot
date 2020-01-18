from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('1tcZp3oaE9v3p3PhQ747vbVKmZHQylZtYFhFf4OPCzstF2Cdu+fhL9hCjTtgZ1sQqgagFkr4wIpGj4ovJGQ6tGLdBJF4h35eBVNJEFHnYbRZYu/Zc7v4qSYN5/4/6GbOM5y8x2Jl6oY4bFF7V2JC+QdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('2e6efb5ea8f4c3f9a8ec0e68c4544ce4')


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
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    r = '我看不懂你說啥'

    if msg in ['hi','哈瞜','HI']:
        r = 'hi'
    elif msg == '吃了嗎':
        r = '還沒'
    elif '訂位' in msg:
        r = '您想訂位,幾位?'
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=r))


if __name__ == "__main__":
    app.run()