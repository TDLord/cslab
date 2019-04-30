# -*- coding: utf-8 -*-
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
import requests

def get_message(bot, update): 	
    if update.message.text == '쿵':
        update.message.reply_text('짝')
    if update.message.text == '코인':
        update.message.reply_text("비트코인 마감 시세 :" + get_coin_info() + "원")

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