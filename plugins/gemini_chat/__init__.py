from nonebot import on_message
from nonebot.rule import to_me, Rule
from nonebot.adapters.onebot.v11 import Bot
from nonebot.adapters.onebot.v11.event import MessageEvent, GroupMessageEvent
from nonebot.adapters.onebot.v11 import MessageSegment as MS

from .data_source import send_to_gemini, summary_chat

from services.UsrDataService import UsrDataService
from utils import rules

chat = on_message(priority=50, rule= to_me()&Rule(rules.both), block=False)

@chat.handle()
async def chat_handle(bot: Bot, event: MessageEvent):
    # 获取新的消息(限制50个字符)
    msg = str(event.get_message())
    if len(msg)>50:
        return
    
    # 加载用户数据
    with UsrDataService(event.user_id) as user_data:
        # 扣除一个鱼干
        if not user_data.adjust_fish(-1):
            await chat.finish("奈咲酱有些饿了喵呜...\n（得有小鱼干才能聊天呢）")
    
        # 发送请求
        new_chats = await send_to_gemini(msg, user_data.get_chat())
    
        # 生成回应消息
        reply = MS.text("")
        if isinstance(event, GroupMessageEvent) :
            reply = MS.at(event.user_id) + "\n"
        reply += new_chats[-1]["content"]
    
        # 总结记忆
        if len(new_chats) > 40:
            new_chats = await summary_chat(new_chats)
        
        # 保存记忆
        user_data.edit_chat(new_chats)

    await chat.send(reply)
