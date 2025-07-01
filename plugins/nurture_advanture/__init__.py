from nonebot import on_regex
from nonebot.rule import Rule
from nonebot.adapters.onebot.v11 import Bot
from nonebot.adapters.onebot.v11.event import MessageEvent, GroupMessageEvent
from nonebot.adapters.onebot.v11 import MessageSegment as MS
from datetime import datetime

from .advanture_events import get_advanture

from services.UsrDataService import UsrDataService
from utils import rules

# 每日签到
signin = on_regex("^(签到|冒险|探险)$", priority=5, rule=Rule(rules.both), block=True)
@signin.handle()
async def signin_handle(bot: Bot, event: MessageEvent):
    reward_text = []

    with UsrDataService(event.user_id, auto_create=True) as user_data:
        # 冒险过则直接拒绝
        if user_data.get_signin() == datetime.now().date():
            await signin.finish("主人今天探险过了~")

        # 开始探险
        result = get_advanture([])
        # 计算奖励
        for key, value in result.rewards.items():
            if key == "fish":
                user_data.adjust_fish(value)
                reward_text.append(f"小鱼干+{value}")
            elif key == "imp":
                user_data.adjust_imp(value)
                reward_text.append(f"好感度+{value}")
            else:
                # 物品奖励
                user_data.inventory.add(key, value)
                reward_text.append(f"{user_data.inventory.name_cn(key)}+{value}")

        # 记录签到时间
        user_data.edit_signin(datetime.now().date()) 

    # 构建探险消息
    reward_text = ",".join(reward_text)

    # 发送消息
    msg = MS.text("")
    if isinstance(event, GroupMessageEvent) :
        msg = MS.at(event.user_id) + "\n"
    msg += f"--- {result.name} ---\n"
    msg += result.text + "\n"
    msg += f"({reward_text})"
    await signin.finish(msg)
