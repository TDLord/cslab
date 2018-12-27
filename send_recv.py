import telegram
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
from weather import weather_info
import requests
import time
import datetime

# 커스텀 키보드 설정
custom_keyboard = [
    ["/help", "취소"],
    ["코인", "날씨", "아이디"],
]

custom_keyboard2 = [
    ["/help", "취소"],
    ["죽전동", "강남역", "처음으로"],
]

reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard, resize_keyboard=True)
reply_markup2 = telegram.ReplyKeyboardMarkup(custom_keyboard2, resize_keyboard=True)

n = time.localtime().tm_wday
now = datetime.datetime.now()

def get_message(bot, update):
    if update.message.text == '코인':
        update.message.reply_text("비트코인 마감 시세 :" + get_coin_info() + "원")
        
    if update.message.text == '서초동':
        params = {'area': update.message.text}
        msg = weather_info(**params)
        print(msg)
        update.message.reply_text(msg)
        
    if update.message.text == "날짜":
        print(update.message.text)
        now = datetime.datetime.now()
        update.message.reply_text("오늘의 날짜 : \n%s년 %s월 %s일 입니다." % (now.year, now.month, now.day))

    if update.message.text == "시간":
        print(update.message.text)
        now = datetime.datetime.now()
        update.message.reply_text("현재 시간 : \n%s시 %s분 %s초 입니다." % (now.hour, now.minute, now.second))

    if update.message.text == "아이디":
        chat_id = update.message.chat_id
        update.message.reply_text("당신의 chat_id 는 %s 입니다." % chat_id,reply_markup=reply_markup)
        
    else:
        update.message.reply_text(update.message.text)

def get_coin_info():
    url = 'https://api.bithumb.com/public/ticker/all'
    resp = requests.get(url)
    content = resp.json()
    btc_close_price = content["data"]["BTC"]["closing_price"]
    return btc_close_price

updater = Updater('716140943:AAH5ZZk_tVltsDu-IMKancGlGcnzoBia-tM')
message_handler = MessageHandler(Filters.text, get_message)
updater.dispatcher.add_handler(message_handler)
updater.start_polling()
updater.idle()