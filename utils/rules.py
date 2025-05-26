from nonebot.adapters.onebot.v11 import GroupMessageEvent,PrivateMessageEvent
import yaml

with open('./config.yaml',encoding='utf-8') as file1:
    config = yaml.load(file1,Loader=yaml.FullLoader)

# 仅允许超级用户
async def only_superuser(event) -> bool:
    if event.user_id == config["SUPERUSER"]:
        return True
    else:
        return False

# 同时允许私聊和群聊
async def both(event) -> bool:
    # 群聊要求白名单
    if isinstance(event, GroupMessageEvent) :
        if event.group_id in config["whitelist"] :
            return True
        else:
            return False
    # 私聊通过
    elif isinstance(event, PrivateMessageEvent):
        return True
    # 其余拒绝
    else:
        return False

# 仅许可私聊
async def private(event) -> bool:
    if isinstance(event, PrivateMessageEvent) :
        return True
    else:
        return False

# 仅许可群聊
async def group(event) -> bool:
    # 群聊要求白名单
    if isinstance(event, GroupMessageEvent) :
        if event.group_id in config["whitelist"] :
            return True
        else :
            return False
    # 其余拒绝
    else :
        return False

