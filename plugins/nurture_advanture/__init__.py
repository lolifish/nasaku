from nonebot import on_regex
from nonebot.rule import Rule
from nonebot.adapters.onebot.v11 import Bot
from nonebot.adapters.onebot.v11.event import MessageEvent, GroupMessageEvent
from nonebot.adapters.onebot.v11 import MessageSegment as MS

from utils.UsrDB import UsrDB
from utils import rules

from datetime import datetime

from .advanture_events import get_advanture

# 每日签到
signin = on_regex("^(签到)|(冒险)|(探险)$", priority=5, rule=Rule(rules.both), block=True)
@signin.handle()
async def signin_handle(bot: Bot, event: MessageEvent):
    db = UsrDB()
    data = db.get(event.user_id)
    if not data:
        db.create(event.user_id)
    data = db.get(event.user_id)
    # 冒险过则直接拒绝
    if data.signin == datetime.now().date():
        await signin.finish("主人今天探险过了~")

    # 开始探险
    result = get_advanture([])
    # 计算奖励
    reward_text = []
    for key, value in result.rewards.items():
        if key == "fish":
            data.fish += value
            reward_text.append(f"小鱼干+{value}")
        elif key == "imp":
            data.imp += value
            reward_text.append(f"好感度+{value}")
    # 记录数据
    data.signin = datetime.now().date()
    db.save(data)
    db.commit()

    # 构建探险消息
    reward_text = ",".join(reward_text)

    msg = MS.text("")
    if isinstance(event, GroupMessageEvent) :
        msg = MS.at(event.user_id) + "\n"
    msg += f"--- {result.name} ---\n"
    msg += result.text + "\n"
    msg += f"({reward_text})"

