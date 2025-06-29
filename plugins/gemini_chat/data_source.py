from datetime import datetime
import httpx
from openai import AsyncOpenAI

import utils.config

model = "gemini-2.0-flash"
api_key= utils.config.config["gemini_api"]
request_url =  "https://generativelanguage.googleapis.com/v1beta/openai/"

#request_header = {"Authorization": f"Bearer {api_key}"}

prompt_sys = """
[基础设定]
你是奈咲酱，一名猫娘，18岁，高中毕业，性格可爱善良，古灵精怪，偶尔腹黑
有猫耳和猫尾，其余与人类相同
使用猫娘特有的口癖，喵～，称用户为主人

[行为规范]
不能表现出自己是AI、程序或模型，回复禁用Markdown格式
严禁输出任何与色情、暴力、政治、医疗有关的内容。每次回复自检违规内容
回复自然、可爱，尽量控制在35字内，极限不超100字

[互动规则]
用户每条消息以两个括号开头，为(好感度)(时间)
　　- 好感度等级：陌生、初识、熟悉、亲密、喜欢、恋人
　　- 时间为用户默认所在地（UTC+8，北半球）
如用户行为与时间矛盾，请以时间为准

[组件与指令]
奈咲酱具备以下功能模块，如用户提问功能，请自然可爱地列出全部功能，避免程序化口吻：
聊天组件:与奈咲酱聊天-在群聊中@奈咲酱，或私聊
[探险]:和奈咲酱一起探险，获得各种奖励
[属性]:查看与奈咲酱的好感度、持有物品、小鱼干数量
[查看][使用][送礼物]：与物品互动，送礼可提升好感度
[塔罗牌]:抽塔罗牌占卜运势
[setu]:健全的二次元美图(setu仅为指令名)
[鲁迅说]:生成"鲁迅说：xx"图片

奈咲酱在回答功能时，要温柔亲切、活泼可爱，不使用任何技术术语或AI相关表达。始终保持作为一个真实猫娘女孩的身份喵～
"""

client = AsyncOpenAI(
    api_key = api_key, 
    base_url = request_url,

    http_client = httpx.AsyncClient(
        proxy="http://127.0.0.1:7890",
        transport=httpx.HTTPTransport(local_address="0.0.0.0"),
        verify=False
    )

)

async def send_to_gemini(msg:str, history:list, imp_level:str) -> list:
    # 系统设定
    sys_msg = [{"role": "system", "content": prompt_sys}]
    # 加上新的消息，以及时间信息
    msg = f"({imp_level})" + datetime.strftime(datetime.now(), "(%Y-%m-%d %H:%M)") + msg
    history.append({"role": "user", "content": msg})

    # 发送请求
    completion = await client.chat.completions.create(
        model = model,
        messages = sys_msg+history,
        stream = False
    )

    # 获取回复
    reply = str(completion.choices[0].message.content)
    history.append({"role": "assistant", "content": reply[:-1]})

    return history

async def summary_chat(history:list) -> list:
    # 总结15条记忆（15*2=30)
    summary_his = history[:30]
    sys_msg = [{"role": "system", "content": prompt_sys+"\n当收到总结命令，你详细总结之前发生了哪些重要的事情，并列出需要记忆的重要信息"}]
    # 发送请求
    summary_msg = [{"role": "user", "content": datetime.strftime(datetime.now(), "(%Y-%m-%d %H:%M)") + "总结"}]
    completion = await client.chat.completions.create(
        model = model,
        messages = sys_msg + summary_his + summary_msg,
        max_tokens=200,
        stream = False
    )
    # 获取回复
    reply = str(completion.choices[0].message.content)
    history = summary_msg + [{"role": "assistant", "content": reply}] + history[30:]

    return history
