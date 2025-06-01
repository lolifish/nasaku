from nonebot import on_regex
from nonebot.rule import Rule
from nonebot.adapters.onebot.v11 import Bot
from nonebot.adapters.onebot.v11.event import Event

from utils.UsrDB import UsrDB
from utils import rules

## 每日签到
#signin = on_regex("^签到$", priority=5, rule=Rule(rules.both), block=True)
#@signin.handle()
#async def signin_handle(bot: Bot, event: Event):
#    db = UsrDB()
#    data = db.get(event.user_id)
#    if not data:
#        db.create(event.user_id)
#    data = db.get(event.user_id)
#    # 签过到直接拒绝
#    if data.signin == datetime.now().date():
#        await signin.finish("主人今天签过到了~")
#    # 发送签到奖励
#    reward = 5
#    data.fish += reward
#    # 记录签到日期
#    data.signin = datetime.now().date()
#    db.save(data)
#    db.commit()
#    await signin.finish(f"签到成功！\n给主人{reward}枚小鱼干~")


# 查询属性
backpack = on_regex("^属性$", priority=5, rule=Rule(rules.both), block=True)
@backpack.handle()
async def backpack_handle(bot: Bot, event: Event):
    db = UsrDB()
    data = db.get(event.user_id)
    if not data:
        db.create(event.user_id)
        data = db.get(event.user_id)

    text = '┌' + ' '*40 + '┐'
    text += f"\n好感度：{data.imp}"
    text += f"\n小鱼干: {data.fish}枚"
    text += '\n└' + ' '*40 + '┘'

    await backpack.finish(text)
    