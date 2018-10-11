from __future__ import unicode_literals

import json
import urllib.request
import urllib.parse
# 调用微信的包
from wxpy import *

bot = Bot(cache_path=True)
bot.enable_puid()

def get_turing_reply(text):
    url = "http://openapi.tuling123.com/openapi/api/v2"
    # 这里是我的机器人密钥，图灵机器人官网：http://openapi.tuling123.com/
    data = {"reqType": 0,
            "userInfo": {"apiKey": "bdc21a7bbe926436827927b73249b8ac", "userId": "1FE2D1A0A2B55770E18B5D3F985217DD"},
            "perception": {"inputText": {"text": str(text)}}}
    data = json.dumps(data)
    data = bytes(data, 'utf-8')
    request = urllib.request.Request(url)
    result = urllib.request.urlopen(request, data).read()
    result = result.decode('utf-8')
    result = json.loads(result)
    return result['results'][0]['values']['text']

@bot.register(chats=bot.friends(), msg_types='Text', except_self=False)
def auto_reply(msg):
    if msg.sender.puid == bot.self.puid:
        if 'on' == msg.text:
            G.flag = True
            msg.sender.send_msg("已开启微信聊天代理")
            print(" ")
            print(str(msg.create_time) + "  ON")
        elif 'off' == msg.text:
            G.flag = False
            msg.sender.send_msg("已关闭微信聊天代理")
            print(" ")
            print(str(msg.create_time) + "  OFF")
    else:
        if G.flag:
            print(" ")
            print(msg.create_time)
            print(msg)
            try:
                reply = get_turing_reply(msg.text)
                msg.sender.send_msg(reply)
                print("Reply: " + reply)
            except Exception:
                print("Reply error.")

class G:
    flag = False

embed()
