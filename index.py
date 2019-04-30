# -*- encoding: utf-8 -*-

import requests
import json
from flask import Flask, request, jsonify
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
import telegram

#---------------------------------------------------------------------------------------------------------------------------------------------
#커스텀 키보드 레이아웃을 생성(변경 및 추가 가능)
custom_keyboard0 = [['/help','btn1'],
                    ['btn2', 'btn3']]       #2 by 2 키보드 레이아웃
#custom_keyboard1 = []

reply_markup0 = telegram.ReplyKeyboardMarkup(custom_keyboard0, resize_keyboard=True)  #생성된 키보드 레이아웃을 텔레그램 키보드 객체로 사용 하도록 변수설정
#reply_markup1 = telegram.ReplyKeyboardMarkup(custom_keyboard1, resize_keyboard=True)
#------------------------------------------------------------------------------------------------------------------------------------------------


def help_command(bot, update):
    update.message.reply_text("문의사항은 010-****-****로 연락주세요!", reply_markup = reply_markup0)
    #이와 같은 방법으로 사용자에게 답변을 하면서 커스텀 키보드를 팝업시킬수있다.

    
#--------------------------!!주석 부분의 api key 입력 부분 말고는 수정 x----------------------------------------------------------------------------
# dialog flow로 문자열을 보내서 답변을 반환하는 함수 
def get_answer(text, user_key):
    data_send = { 
        'query': text,
        'sessionId': user_key,
        'lang': 'ko',
    }
    data_header = {
        'Authorization': 'Bearer ed47255b79d7425aa8bcaab42227cb87', #ed47255b~cb87 부분에 본인의 dialog flow api key를 입력(Bearer띄어쓰기 유의)
        'Content-Type': 'application/json; charset=utf-8'
    }
    dialogflow_url = 'https://api.dialogflow.com/v1/query?v=20150910'   
    res = requests.post(dialogflow_url, data=json.dumps(data_send), headers=data_header)
    if res.status_code != requests.codes.ok:
        return '오류가 발생했습니다.'
    data_receive = res.json()
    answer = data_receive['result']['fulfillment']['speech'] 
    return answer
#--------------------------------------------------------------------------------------------------------------------------------------------   


#---------------!!수정 x---------------------------------------------------------------------------
#사용자의 텔레그램 메시지를 매개변수로 위의 get_answer()를 호출하여 돌아온 답변을 채팅방에 보내는 함수
def get_message(bot, update):
    print(update.message.text)
    content = update.message.text
    chat_id = update.message.chat_id
    dialog_answer = get_answer(content, chat_id) #사용자의 메시지에 대한 dialogflow의 답변이 리턴
    update.message.reply_text("%s" % dialog_answer) #챗봇이 사용자에게 답변
#--------------------------------------------------------------------------------------------------


#----------------------------------------------------------------------------------------------------------------------------
#서버 프로그램이 동작되면 호출될 메인 함수
#풀링 방식으로 일정시간마다 다음을 반복
#챗봇이 채팅방을 확인하며 새로운 메시지의 유무를 판단 새로운 메시지가 있으면 해당 메시지로 위의 get_message()를 호출
#1. 원하는 기능의 핸들러를 추가(코드가 이해 되는 사람만.)
def main():
    updater = Updater('716140943:AAH5ZZk_tVltsDu-IMKancGlGcnzoBia-tM') #본인이 생성한 텔레그램 봇 토큰 입력
    message_handler = MessageHandler(Filters.text, get_message)
    help_handler = CommandHandler('help', help_command)
    updater.dispatcher.add_handler(help_handler)
    updater.dispatcher.add_handler(message_handler)
    updater.start_polling()
    updater.idle()
#------------------------------------------------------------------------------------------------------------------    


#플라스크 서버가 동작하기 위한 코드 부분. 수정x
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

@app.route('/', methods=['POST', 'GET'])
def index():
    return '<h1>welcome to chatbot world</h>'

if __name__ == '__main__':
    main()
    app.run(host='0.0.0.0')
#--------------------------------------------