# -*- encoding: utf-8 -*-

import requests
import json
from flask import Flask, request, jsonify
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
import telegram

custom_keyboard0 = [
    ['/help'],
    ['안녕!', '옷가게'],
]
reply_markup0 = telegram.ReplyKeyboardMarkup(custom_keyboard0, resize_keyboard=True)

def help_command(bot, update):
    update.message.reply_text("문의사항은 010-****-****로 연락주세요!")
    
def get_answer(text, user_key):
    data_send = { 
        'query': text,
        'sessionId': user_key,
        'lang': 'ko',
    }
    data_header = {
        'Authorization': 'Bearer ed47255b79d7425aa8bcaab42227cb87',
        'Content-Type': 'application/json; charset=utf-8'
    }
    dialogflow_url = 'https://api.dialogflow.com/v1/query?v=20150910'   
    res = requests.post(dialogflow_url, data=json.dumps(data_send), headers=data_header)
    if res.status_code != requests.codes.ok:
        return '오류가 발생했습니다.'
    data_receive = res.json()
    answer = data_receive['result']['fulfillment']['speech'] 
    return answer

def get_message(bot, update):
    print(update.message.text)
    content = update.message.text
    chat_id = update.message.chat_id
    dialog_answer = get_answer(content, chat_id)
    update.message.reply_text("%s" % dialog_answer)

def main():
    updater = Updater('716140943:AAH5ZZk_tVltsDu-IMKancGlGcnzoBia-tM')
    updater.bot.send_message(chat_id = 720240770, text="챗봇에 오신 것을 환영합니다", reply_markup = reply_markup0)
    message_handler = MessageHandler(Filters.text, get_message)
    help_handler = CommandHandler('help', help_command)
    updater.dispatcher.add_handler(help_handler)
    updater.dispatcher.add_handler(message_handler)
    updater.start_polling()
    updater.idle()
    
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

@app.route('/', methods=['POST', 'GET'])
def index():
    return '<h1>welcome to chatbot world</h>'

if __name__ == '__main__':
    main()
    app.run(host='0.0.0.0')
