import requests
import json
import time
from wxauto import WeChat
from wechat import GetHistory

wx = WeChat()
# 指定监听目标
listen_list = [
    '24级中文信息什么时候发顶会',
]

who = listen_list[0]
wx = WeChat()

for i in listen_list:
    wx.AddListenChat(who=i)  # 添加监听对象

wait = 1  # 设置1秒查看一次是否有新消息
while True:
    msgs = wx.GetListenMessage()
    for chat in msgs:
        print(chat)
        msg = msgs.get(chat)   # 获取消息内容
        for i in msg:
            if i.type == 'friend' or i.type == 'self':
                # ===================================================
                # 处理消息逻辑
                break                          
                # ===================================================
        
    time.sleep(wait)