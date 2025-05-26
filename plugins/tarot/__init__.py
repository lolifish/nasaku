from nonebot import on_regex
from nonebot.rule import Rule
from nonebot.adapters.onebot.v11 import Bot
from nonebot.adapters.onebot.v11.event import GroupMessageEvent, Event
from nonebot.adapters.onebot.v11 import MessageSegment as MS

from .data_source import Cards
from utils import rules

tarot = on_regex("^塔罗牌$", priority=5, rule=Rule(rules.both), block=True)

@tarot.handle()
async def tarot_handle(bot: Bot, event: Event):
    # 抽卡
    cards = Cards(1)
    card_key, card_value, card_image = cards.reveal()

    # 组织消息
    msg = MS.text("")
    if isinstance(event, GroupMessageEvent) :
        msg = MS.at(event.user_id) + "\n"
    msg += MS.text("回应是：%s\n    「%s」\n" % (card_key, card_value))
    msg += MS.image(card_image)

    # 发送
    await tarot.send(msg)
