from nonebot import on_message
from nonebot.rule import to_me, Rule
from nonebot.adapters.onebot.v11 import Bot
from nonebot.adapters.onebot.v11.event import Event, GroupMessageEvent
from nonebot.adapters.onebot.v11 import MessageSegment as MS

from .data_source import send_to_gemini, summary_chat

from utils.UsrDB import UsrDB
from utils import rules

chat = on_message(priority=50, rule= to_me()&Rule(rules.both), block=False)

@chat.handle()
async def chat_handle(bot: Bot, event: Event):
    # 加载用户数据
    db = UsrDB()
    data = db.get(event.user_id)
    if not data:
        db.create(event.user_id)
    data = db.get(event.user_id)

    # 尝试扣除一个鱼干
    if data.fish:
        data.fish -= 1
    else:
        await chat.finish("奈咲酱有些饿了喵呜...")

    # 获取新的消息(限制30个字符)
    msg = str(event.get_message())
    if len(msg)>30:
        return
    
    # 发送请求
    data.chat = await send_to_gemini(msg, data.chat)
    reply = MS.text("")
    if isinstance(event, GroupMessageEvent) :
        reply = MS.at(event.user_id) + "\n"
    reply += data.chat[-1]["content"]
    await chat.send(reply)

    # 总结记忆
    if len(data.chat) > 40:
        data.chat = await summary_chat(data.chat)
    
    # 保存记忆
    db.save(data)
    db.commit()
    

