from nonebot import on_regex
from nonebot.rule import Rule
from nonebot.adapters.onebot.v11 import Bot
from nonebot.adapters.onebot.v11.event import Event
from nonebot.adapters.onebot.v11.message import MessageSegment as MS

import httpx
import re
import os

from utils import rules

# 每日签到
setu = on_regex("^setu$", priority=5, rule=Rule(rules.both), block=True)
@setu.handle()
async def setu_handle(bot: Bot, event: Event):
    id = await random_setu()
    msg = MS.image(os.path.join(os.getcwd(), "data/cache/img.jpg"))
    await setu.finish(msg)


async def random_setu():
    url = "https://api.anosu.top/img"
    headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36"}
    async with httpx.AsyncClient(headers=headers) as client:
        response = await client.get(url, headers=headers, follow_redirects=True)
        print(response.status_code==httpx.codes.OK)
    with open("./data/cache/img.jpg", "wb") as f:
        f.write(response.content)

    # 提取图像id
    print(response.url)
    id = re.findall(r"bjh/(.+)\.", str(response.url))[0]
    return id

