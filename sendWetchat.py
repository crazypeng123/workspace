from __future__ import unicode_literals
from threading import Timer
from wxpy import *
import requests
bot = Bot()
def send_news(receiver, text):
    try:
        my_friend = bot.friends().search(receiver)[0]
        my_friend.send(text)
    except Exception:
        my_friend = bot.friends().search(u"crazypeng")[0]
        my_friend.send(u"发给 " + receiver + u" 的消息失败了")


def tiaoXin():
    friends = [u"江湖第一武学废材", u"林必红", ]
    for f in friends:
        send_news(f, "叫你一声傻逼，你敢答应吗")


def tiaoXin_timer():
    t = Timer(10, tiaoXin)
    t.start()


tiaoXin_timer()