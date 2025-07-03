from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot
from nonebot.rule import Rule
from nonebot.adapters.onebot.v11.event import MessageEvent

from services.UsrDataService import UsrDataService
from services.InventoryService import item_list
from utils.rules import only_superuser

command_list = on_command("command_list", priority=5, rule=Rule(only_superuser), block=True)
@command_list.handle()
async def command_list_handle(bot:Bot):
    msg = "/give <user_id> <kind> <num>\n/clean_chat <user_id>"
    await command_list.finish(msg)

give = on_command("give", priority=5, rule=Rule(only_superuser), block=True)
@give.handle()
async def give_handle(bot: Bot, event: MessageEvent) :
    # 提取参数
    msg = str(event.get_message()).split()
    try:
        user = int(msg[1])
        kind = msg[2]
        num = int(msg[3])
    except:
        await give.finish("参数格式：/give user_id kind num")

    # 给予物品
    with UsrDataService(user) as user_data:
        if user_data.inventory.name_en(kind) in item_list:
            user_data.inventory.add(user_data.inventory.name_en(kind), num)
            await give.finish("success")
        else:
            user_data.adjust_currency(kind, num, ignore_neg=True)
            await give.finish("success")


clean_chat = on_command("clean_chat", priority=5, rule=Rule(only_superuser), block=True)
@clean_chat.handle()
async def clean_chat_handle(bot: Bot, event: MessageEvent) :
    msg = str(event.get_message()).split()
    try:
        user = int(msg[1])
    except:
        await give.finish("参数格式：/clean_chat user_id")
    
    with UsrDataService(user) as user_data:
        user_data.edit_chat([])

    await clean_chat.finish(f"用户{user}的gemini记忆已清空")
