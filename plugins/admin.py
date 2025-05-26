from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot
from nonebot.rule import Rule
from nonebot.adapters.onebot.v11.event import MessageEvent

from utils.UsrDB import UsrDB
from utils.rules import only_superuser

command_list = on_command("command_list", priority=5, rule=Rule(only_superuser), block=True)
@command_list.handle()
async def command_list_handle(bot:Bot):
    msg = "/give <user_id> <kind> <num>\n/clean_chat <user_id>"
    await command_list.finish(msg)

give = on_command("give", priority=5, rule=Rule(only_superuser), block=True)
@give.handle()
async def give_handle(bot: Bot, event: MessageEvent) :
    msg = str(event.get_message()).split()
    try:
        user = int(msg[1])
        kind = msg[2]
        num = int(msg[3])
    except:
        await give.finish("参数格式：/give user_id kind num")
    
    db = UsrDB()
    data = db.get(user)
    if not data:
        db.create(event.user_id)
        data = db.get(event.user_id)

    if kind=="fish":
        data.fish += num
    
    db.save(data)
    await give.finish(f"成功给予{user} {num}个{kind}")


clean_chat = on_command("clean_chat", priority=5, rule=Rule(only_superuser), block=True)
@clean_chat.handle()
async def clean_chat_handle(bot: Bot, event: MessageEvent) :
    msg = str(event.get_message()).split()
    try:
        user = int(msg[1])
    except:
        await give.finish("参数格式：/clean_chat user_id")
    
    db = UsrDB()
    data = db.get(user)
    if not data:
        db.create(event.user_id)
        data = db.get(event.user_id)

    data.chat = []
    db.save(data)
    await clean_chat.finish(f"用户{user}的gemini记忆已清空")
