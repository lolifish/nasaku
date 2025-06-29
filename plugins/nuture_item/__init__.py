from nonebot import on_regex
from nonebot.rule import Rule
from nonebot.adapters.onebot.v11 import Bot
from nonebot.adapters.onebot.v11.event import MessageEvent, GroupMessageEvent
from nonebot.params import RegexGroup

from services.UsrDataService import UsrDataService
from utils import rules

check_item = on_regex(
    "^(?:查看|查看物品|检查|检查物品|check)\s*(.*)$", 
    rule = rules.both, priority=5, block=True
)
@check_item.handle()
async def use_item_handle(bot: Bot, event: MessageEvent, matched: tuple = RegexGroup()):
    item_name_cn = matched[0]
    if not item_name_cn:
        await check_item.finish("请像这样使用指令：查看 浆果蛋糕")
    user_data_s = UsrDataService(event.user_id)
    item_name = user_data_s.inventory.name_en(item_name_cn)

    text = user_data_s.inventory.describe(item_name)
    if not text:
        await check_item.finish("主人没有这个物品喵~")
    await check_item.finish(text)



use_item = on_regex(
    "^(?:使用|使用物品|use)\s*(.*)$", 
    rule = rules.both, priority=5, block=True
)
@use_item.handle()
async def use_item_handle(bot: Bot, event: MessageEvent, matched: tuple = RegexGroup()):
    item_name_cn = matched[0]
    if not item_name_cn:
        await use_item.finish("请像这样使用指令：使用 浆果蛋糕")
    user_data_s = UsrDataService(event.user_id)
    item_name = user_data_s.inventory.name_en(item_name_cn)
    # 使用
    text = user_data_s.inventory.use(item_name)
    if not text:
        await use_item.finish("主人没有这个物品喵~")
    await use_item.finish(text)



gift_item = on_regex(
    "^(?:送礼物|赠送|gift)\s*(.*)$", 
    rule = rules.both, priority=5, block=True
)
@gift_item.handle()
async def use_item_handle(bot: Bot, event: MessageEvent, matched: tuple = RegexGroup()):
    item_name_cn = matched[0]
    if not item_name_cn:
        await gift_item.finish("请像这样使用指令：送礼物 浆果蛋糕")
    user_data_s = UsrDataService(event.user_id)
    item_name = user_data_s.inventory.name_en(item_name_cn)
    # 使用
    text = user_data_s.inventory.gift(item_name)
    if not text:
        await gift_item.finish("主人没有这个物品喵~")
    await gift_item.finish(text)
