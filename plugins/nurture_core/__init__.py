from nonebot import on_regex
from nonebot.rule import Rule
from nonebot.adapters.onebot.v11 import Bot
from nonebot.adapters.onebot.v11.event import MessageEvent

from services.UsrDataService import UsrDataService
from presets.imp_level import imp_level
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
backpack = on_regex("^(?:属性|背包)$", priority=5, rule=Rule(rules.both), block=True)
@backpack.handle()
async def backpack_handle(bot: Bot, event: MessageEvent):
    with UsrDataService(event.user_id) as user_data:
        imp = user_data.get_imp()
        text = '┌' + ' '*40 + '┐'
        text += f"\n    好感度：{imp_level(imp)}({imp})"
        text += f"\n    小鱼干: {user_data.get_fish()}枚"
        inventory_content = ", ".join([f"{user_data.inventory.name_cn(key)}*{value}" for key, value in user_data.inventory.get_all().items()])
        if inventory_content:
            text += f"\n    背包: {inventory_content}"
        else:
            text += "\n    背包: 空"
        text += '\n└' + ' '*40 + '┘'

    await backpack.finish(text)
    