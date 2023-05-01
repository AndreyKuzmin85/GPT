import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from transformers import pipeline

app = Flask(__name__)

# установить значения переменных среды
os.environ['LINE_CHANNEL_SECRET'] = "a776deaa053d06651ff34f48efcedc75"
os.environ['LINE_CHANNEL_ACCESS_TOKEN'] = "fYgf8JJrXFJER3i0HTsso+kdyBAGbh4Y8BOyp55BmCdxYnnOv4MbDtwVetJVsTrAQMACQXyeNkIKVATi6B0hlq5sxQvvC73Mg4FWWA5pRUQL9wAhHjT2WmcH2HSdtef8OLwAR0tIvUMLZgCgRU0FOwdB04t89/1O/w1cDnyilFU="

# получить значения переменных среды
line_channel_secret = os.environ.get('LINE_CHANNEL_SECRET')
line_channel_access_token = os.environ.get('LINE_CHANNEL_ACCESS_TOKEN')

line_bot_api = LineBotApi(line_channel_access_token)
handler = WebhookHandler(line_channel_secret)

@app.route("/", methods=['GET'])
def home():
    return "Hello World!"

@app.route("/", methods=['POST'])

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def reply_message(event):
    user_input = event.message.text
    generator = pipeline('text-generation', model='EleutherAI/gpt-neo-2.7B')
    output = generator(user_input, max_length=30, num_return_sequences=1)[0]['generated_text']
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=output))

if __name__ == "__main__":
    app.run(port=5000)