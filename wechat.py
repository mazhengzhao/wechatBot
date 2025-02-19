import time 
from wxauto import WeChat
from llm import LLMSummary

listen_list = ['YourChatName']

def RecordHistory(wx, who, num = 200):#获取打开对话框前的200条历史消息
    wx.SwitchToChat()
    wx.ChatWith(who)

    num_ite = 1
    msgs = wx.GetAllMessage()
    while (len(msgs) <= num and num_ite <= 50):
        wx.LoadMoreMessage()
        msgs = wx.GetAllMessage(savevoice = True)
        num_ite += 1
    chat_history = ''

    for msg in msgs:
        if msg.type == 'friend' or msg.type == 'self':#获取聊天消息
            sender = msg.sender 
            new_msg = f'<sender>{sender}:<message>{msg.content}\n'
            chat_history += new_msg 

        elif msg.type == 'recall':#获取撤回消息信息
            sender = msg.sender
            new_msg = f'<sender>{sender}:<message>{msg.content}\n'
            chat_history += new_msg

        elif msg.type == 'time':#获取时间信息
            new_msg = f'<time>{msg.time}\n'
            chat_history += new_msg

    with open(f'chat_history_{who}.txt', 'w', encoding='utf-8') as f:
        f.write(chat_history)#维护一个txt文件作为历史消息数据库
    
    return chat_history

def ReplySummaryMsg(reply_num, who):#从历史聊天记录中生成回复
    with open(f'chat_history_{who}.txt', 'r', encoding='utf-8') as f:
        Msgs = f.readlines()

    Msgs = Msgs[-reply_num:]
    Msgs = '\n'.join(Msgs)
    reply = LLMSummary(Msgs)

    return reply

def main():
    wx = WeChat()

    for who in listen_list:
        RecordHistory(wx, who)
        wx.AddListenChat(who=who)  # 添加监听对象        
    
    wait = 1  # 设置1秒查看一次是否有新消息
    while True:
        msgs = wx.GetListenMessage()
        for k,chat in enumerate(msgs):
            msg = msgs.get(chat)   # 获取消息内容
            for i in msg:
                if i.type == 'friend' or i.type == 'self':
                    # ===================================================
                    # 处理消息逻辑
                    sender = i.sender
                    new_msg = f'<sender>{sender}:<message>{i.content}\n'
                    
                    if i.content.startswith('Bot总结'):#先暂定启动词为 ： Bot总结{需要总结的对话数量}
                        reply = ReplySummaryMsg(int(i.content[5:]), listen_list[k])
                        print(reply)
                        #回复消息
                        chat.SendMsg(reply)

                    with open(f'chat_history_{listen_list[k]}.txt', 'a', encoding='utf-8') as f:
                        f.write(new_msg)#记录新消息
                    print(new_msg)
                    # ===================================================
            
        time.sleep(wait)
        #break

if __name__ == '__main__':
    main()