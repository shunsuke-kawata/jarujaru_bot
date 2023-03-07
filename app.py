from flask import Flask, request, abort
import os

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

CHANNEL_ACCESS_TOKEN = os.environ["ACCESS_TOKEN"]
CHANNEL_SECRET = os.environ["CHANNEL_SECRET"]
line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

import os

app = Flask(__name__)

app.route("/", methods=['GET']) 
def test():
    return "<h1>It Works<h1>";

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

    return "OK"

country_list = ['アメリカ', 'アルゼンチン', 'イギリス', 'イタリア', 'インドネシア', 'エジプト', 'オーストラリア', 'カナダ', 'ギリシャ', 'スイス', 'ドイツ', 'モンゴル', '中国', '日本', '韓国'] #ソートされた国名リスト

#文字列を返す関数
def binary_search_country(list_obj, word): #引数には（ソートされた国名リスト,受け取った単語）
    left = 0          
    right = len(list_obj) - 1  
    while left <= right:
        mid = (left + right) // 2            
        if list_obj[mid].startswith(word):
            reply_word = list_obj[mid][len(word):]
            if reply_word=='':
                reply_word='全部言うな！' #探索に成功したが、返す文字数がない
            return reply_word
        elif list_obj[mid] < word:
            left = mid + 1
        else:
            right = mid - 1
    return '知らんわ！' #探索に失敗した場合

#tryの中の処理を記述
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    
    post_word=event.message.text #postからテキストを取得
    reply_word = binary_search_country(country_list, post_word)
    line_bot_api.reply_message(event.reply_token,TextSendMessage(reply_word))


if __name__ == "__main__":
    app.run()
