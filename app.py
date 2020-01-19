import requests
import re
import random
import configparser
from bs4 import BeautifulSoup

from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,StickerSendMessage,ImageSendMessage,LocationSendMessage,TemplateSendMessage, ButtonsTemplate, PostbackTemplateAction, MessageTemplateAction, URITemplateAction,TemplateSendMessage, CarouselColumn,CarouselTemplate,MessageAction
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
#蘋果頭條前8
def apple_news():
    target_url = 'https://tw.appledaily.com/new/realtime'
    print('Start parsing appleNews....')
    rs = requests.session()
    res = rs.get(target_url, verify=False)
    soup = BeautifulSoup(res.text, 'html.parser')
    content = ""
    for index, data in enumerate(soup.select('.rtddt a'), 0):
        if index == 8:
            return content
        link = data['href']
        content += '{}\n\n'.format(link)
    return

def technews():
    target_url = 'https://technews.tw/'
    print('Start parsing movie ...')
    rs = requests.session()
    res = rs.get(target_url, verify=False)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'html.parser')
    content = ""

    for index, data in enumerate(soup.select('article div h1.entry-title a')):
        if index == 12:
            return content
        title = data.text
        link = data['href']
        content += '{}\n{}\n\n'.format(title, link)
    return content 

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    r = '請輸入:功能'

    if '貼圖' in msg:
        sticker_message = StickerSendMessage(
            package_id='2',
            sticker_id='36'
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


    if '電影' in msg:
        Carousel_template1 = TemplateSendMessage(
        alt_text='看電影專用',
        template=CarouselTemplate(
        columns=[
            CarouselColumn(
                thumbnail_image_url='https://i.imgur.com/mj76gq0.jpg',
                title='八德國賓',
                text='八德國賓資訊',
                actions=[
                    MessageTemplateAction(
                        label='電影院位置',
                        text='八德國賓'
                    ),
                    URITemplateAction(
                        label='電影時刻',
                        uri='https://www.ambassador.com.tw/home/Showtime?ID=8fda9934-73d4-4c14-b1c4-386c2b81045c&D'
                    ),
                    URITemplateAction(
                        label='即將上映電影',
                        uri='https://www.ambassador.com.tw/home/MovieList?Type=0'
                    ),
                    URITemplateAction(
                        label='影城資訊',
                        uri='https://www.ambassador.com.tw/home/theater_intro_a12'
                    )
                ]
            ),
            CarouselColumn(
                thumbnail_image_url='https://i.imgur.com/mj76gq0.jpg',
                title='新莊國賓',
                text='新莊國賓資訊',
                actions=[
                    MessageTemplateAction(
                        label='電影院位置',
                        text='新莊國賓'
                    ),
                    URITemplateAction(
                        label='電影時刻',
                        uri='https://www.ambassador.com.tw/home/Showtime?ID=3301d822-b385-4aa8-a9eb-aa59d58e95c9&DT'
                    ),
                    URITemplateAction(
                        label='即將上映電影',
                        uri='https://www.ambassador.com.tw/home/MovieList?Type=0'
                    ),
                    URITemplateAction(
                        label='影城資訊',
                        uri='https://www.ambassador.com.tw/home/theater_intro_a10'
                    )
                ]
            )
        ]
    )
)
        line_bot_api.reply_message(
        event.reply_token,
        Carousel_template1)
        return    

    if '外幣' in msg:
        Carousel_template2 = TemplateSendMessage(
        alt_text='找匯率專用',
        template=CarouselTemplate(
        columns=[
            CarouselColumn(
                thumbnail_image_url='https://i.imgur.com/XMtYFim.jpg',
                title='日幣',
                text='查日幣匯率專用',
                actions=[
                    URITemplateAction(
                        label='日幣新聞',
                        uri='https://udn.com/search/tagging/2/%E6%97%A5%E5%B9%A3'
                    ),
                    URITemplateAction(
                        label='日幣換匯即時網站',
                        uri='https://www.findrate.tw/JPY/#.XiRassgzaUk'
                    )
                ]
            ),
            CarouselColumn(
                thumbnail_image_url='https://i.imgur.com/2h6IcPH.jpg',
                title='美金',
                text='查美金匯率專用',
                actions=[
                    URITemplateAction(
                        label='美金新聞',
                        uri='https://news.ltn.com.tw/topic/%E7%BE%8E%E5%85%83'
                    ),
                    URITemplateAction(
                        label='美金換匯即時網站',
                        uri='https://tw.rter.info/currency/USD/'
                    )
                ]
            )
        ]
    )
)
        line_bot_api.reply_message(
        event.reply_token,
        Carousel_template2)
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
    
    if '八德國賓' in msg:
        location_message3 = LocationSendMessage(
        title='八德國賓電影院位置',
        address='八德國賓電影院',
        latitude=24.964764,
        longitude=121.298895
        )
        line_bot_api.reply_message(
        event.reply_token,
        location_message3)
        return

    if '新莊國賓' in msg:
        location_message4 = LocationSendMessage(
        title='新莊國賓電影院位置',
        address='新莊國賓電影院位置',
        latitude=25.063936,
        longitude=121.458913
        ) 
        line_bot_api.reply_message(
        event.reply_token,
        location_message4)
        return 

    if msg in ['hi','哈瞜','HI','哈囉','你好']:
        r = 'hi'
    elif msg == '功能':
        r = '請輸入:(早餐,電影,貼圖,外幣,蘋果新聞,科技新聞),其中一下即可進入功能,輸入其他字無法啟動'
    elif msg == '北鼻':
        r = '加油'
    elif msg == '蘋果新聞':
        r = apple_news()
    elif msg == '科技新聞':
        r = technews()


    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=r))

if __name__ == "__main__":
    app.run()