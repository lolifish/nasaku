from nonebot import on_regex
from nonebot.adapters.onebot.v11 import Bot, MessageEvent
from nonebot.params import RegexGroup
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11.message import MessageSegment as MS

from .data_source import check_text, process_img

from services.UsrDataService import UsrDataService
from utils import rules


luxun_say = on_regex(
    "^鲁迅说(?::|：|,|，)?(.*)$", 
    rule = rules.both, priority=5, block=True
)
@luxun_say.handle()
async def luxun_say_handle(bot: Bot, event: MessageEvent, matched: tuple = RegexGroup()):
    result = matched[0]
    if not result:
        text = "请像这样使用 “鲁迅说:奈咲酱赛高”"
    else:
        text = result
        # 处理字数限制
        if len(text) > 20:
            await luxun_say.finish("话太长啦，鲁迅说不完！")
        # 调用api对文本安全进行检验
        if check_text(text):
            result = True
        else:
            result = False
        if not result:
            await luxun_say.finish("鲁迅不可以说这个！")

    # 扣除鱼干
    with UsrDataService(event.user_id) as user_data:
        if not user_data.adjust_fish(-1):
            await luxun_say.finish("主人的鱼干不够哦")
            
    # 发送图片
    await luxun_say.finish(MS.image(process_img(text)))


            

