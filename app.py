from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,StickerSendMessage,ImageSendMessage,LocationSendMessage,TemplateSendMessage, ButtonsTemplate, PostbackTemplateAction, MessageTemplateAction, URITemplateAction
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
    r = '目前的功能只有這些,請輸入:(早餐,桃園家裡位置,柔柔家裡位置,按鈕,貼圖),輸入別的會沒東西'

    if '給我貼圖' in msg:
        sticker_message = StickerSendMessage(
            package_id='19',
            sticker_id='2'
        )

        line_bot_api.reply_message(
        event.reply_token,
        sticker_message)
        return
#傳圖片
    if '早餐' in msg:
        image_message = ImageSendMessage(
        original_content_url='https://i.imgur.com/JouT00p.jpg',
        preview_image_url='https://i.imgur.com/JouT00pundefined.jpg'
        )

        line_bot_api.reply_message(
        event.reply_token,
        image_message)
        return
#傳位置
    if '桃園家裡位置' in msg:
        location_message = LocationSendMessage(
        title='桃園家裡住址',
        address='桃園家',
        latitude=25.009534,
        longitude=121.295280
        )

        line_bot_api.reply_message(
        event.reply_token,
        location_message)
        return

    if '柔柔家裡位置' in msg:
        location_message2 = LocationSendMessage(
        title='柔柔家裡位置',
        address='柔柔家',
        latitude=25.003485,
        longitude=121.514675
        )

        line_bot_api.reply_message(
        event.reply_token,
        location_message2)
        return

    if '按鈕' in msg:
        buttons_template_message = TemplateSendMessage(
        alt_text='Buttons template',
        template=ButtonsTemplate(
            thumbnail_image_url='https://i.imgur.com/08O1jth.jpg',
            title='選單',
            text='這個是buttons',
            actions=[
                PostbackTemplateAction(
                    label='這個按鈕沒有用',
                    display_text='接收PostBack使用的是@handler.add(PostbackEvent)，一樣使用後面的handle_postback(event)定義接收到的反應。',
                    data='postback1'
                ),
                MessageTemplateAction(
                    label='柔柔家裡位置',
                    text='柔柔家裡位置'
                ),
                URITemplateAction(
                    label='line機器人文章',
                    uri='https://ithelp.ithome.com.tw/articles/10195640?sc=iThomeR'
                )
            ]
        )
     )
        line_bot_api.reply_message(
        event.reply_token,
        buttons_template_message)
        return
            

    if msg in ['hi','哈瞜','HI','哈囉','你好']:
        r = 'hi'
    elif msg == '功能':
        r = '請輸入:早餐,桃園家裡位置,柔柔家裡位置,按鈕,貼圖'
    elif msg == '北鼻':
        r = '加油'
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=r))



if __name__ == "__main__":
    app.run()