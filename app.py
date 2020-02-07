import requests
import re
import random
import configparser
from bs4 import BeautifulSoup
from requests import get
import bs4

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

# 協助分析爬蟲後的網址整理
def string_merge(a):
    r = ''
    for i in a:
        #r += i[0] + '\n' + i[1] + '\n\n'
        r += '{0} \n {1} \n\n'.format(i[0],i[1])
    return r

#聯合報新聞
def udn ():
    url = 'https://udn.com/search/tagging/2/%E4%BB%8A%E6%97%A5%E9%A0%AD%E6%A2%9D'
    headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
    }
    res = get(url,headers=headers)#記得.text
    res.encoding = 'utf8'
    #print(response.text)

    soup = bs4.BeautifulSoup(res.text,'html.parser') #讓beautifulsoup 協助我們解析 html格式文件
    titles = soup.find_all('div',class_='story-list__text')
    lst =[]
    for title in titles :
        for a in title.find_all('h2'):
            #print(a.text)
            for b in a.find_all('a'):
                #print(b.get('href'))
                lst.append([a.text.replace('\n',''),b.get('href')])
    return lst

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
    #r = '請輸入:功能  \n  (輸入這兩個字,可以找目前所有功能)'
    if msg == "功能":
        buttons_template = TemplateSendMessage(
            alt_text='功能列表',
            template=ButtonsTemplate(
                title='功能選單',
                text='請點下列選項',
                thumbnail_image_url='https://i.imgur.com/xQF5dZT.jpg',
                actions=[
                    MessageTemplateAction(
                        label='蘋果即時新聞',
                        text='蘋果即時新聞'
                    ),
                    MessageTemplateAction(
                        label='國賓電影',
                        text='電影'
                    ),
                    MessageTemplateAction(
                        label='查看外幣匯率',
                        text='外幣'
                    ),
                    MessageTemplateAction(
                        label='科技新聞',
                        text='科技新聞'
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, buttons_template)
        return 

    if '貼圖' in msg:
        sticker_message = StickerSendMessage(
            package_id='2',
            sticker_id='36'
        )

        line_bot_api.reply_message(
        event.reply_token,
        sticker_message)
        return

    if msg == '餐點':
        buttons_template2 = TemplateSendMessage(
            alt_text='餐點列表',
            template=ButtonsTemplate(
                title='餐點選單',
                text='請點下列選項',
                thumbnail_image_url='https://i.imgur.com/bAIN2lW.jpg',
                actions=[
                    URITemplateAction(
                        label='早餐',
                        uri='https://photos.app.goo.gl/excAZsSxNEKqbWcn8'
                    ),
                    URITemplateAction(
                        label='77.food 美食ig',
                        uri='https://www.instagram.com/77.food/?hl=zh-tw'
                    ),
                    URITemplateAction(
                        label='eatnini 美食ig',
                        uri='https://www.instagram.com/eatnini/?hl=zh-tw'
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, buttons_template2)
        return 

    if '電影' in msg:
        Carousel_template1 = TemplateSendMessage(
        alt_text='看電影專用',
        template=CarouselTemplate(
        columns=[
            CarouselColumn(
                thumbnail_image_url='https://i.imgur.com/u6t3k33.jpg',
                title='八德國賓',
                text='八德國賓資訊',
                actions=[
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
                thumbnail_image_url='https://i.imgur.com/M1Xmw4h.jpg',
                title='新莊國賓',
                text='新莊國賓資訊',
                actions=[
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
            ),
            CarouselColumn(
                thumbnail_image_url='https://i.imgur.com/EQtfDY6.jpg',
                title='人民幣',
                text='人民幣匯率專用',
                actions=[
                    URITemplateAction(
                        label='人民幣新聞',
                        uri='https://news.ltn.com.tw/topic/%E4%BA%BA%E6%B0%91%E5%B9%A3'
                    ),
                    URITemplateAction(
                        label='人民幣換匯即時網站',
                        uri='https://www.taiwanrate.org/exchange_rate.php?c=CNY#.XiVW_sgzaUk'
                    )
                ]
            ),    
            CarouselColumn(
                thumbnail_image_url='https://i.imgur.com/MBMuK3n.jpg',
                title='韓元',
                text='韓元匯率專用',
                actions=[
                    URITemplateAction(
                        label='韓元新聞',
                        uri='https://www.ettoday.net/news_search/doSearch.php?keywords=%E9%9F%93%E5%85%83&kind=17&idx=2'
                    ),
                    URITemplateAction(
                        label='韓元換匯即時網站',
                        uri='https://www.findrate.tw/KRW/#.XiVZ7cgzaUk'
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
    elif msg == '北鼻':
        r = '加油'
    elif msg == '蘋果即時新聞':
        r = apple_news()
    elif msg == '科技新聞':
        r = technews()
    elif msg == '聯合報新聞':
        a = udn()
        r = string_merge(a)
        print(r)
        


    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=r))

if __name__ == "__main__":
    app.run()
