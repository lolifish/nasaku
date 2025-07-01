from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from services.UsrDataService import UsrDataService

from models.BaseItem import BaseItem

class PosionOfForgetting(BaseItem):
    name_en = "Posion of forgetting"
    name_cn = "遗忘药水"
    describe = "既是液体又是固体的淡蓝色药水，饮用后将清空与奈咲酱的AI聊天内容\n（不影响其它数据，但效果不可逆，谨慎使用）"
    tags = {"usable", "tradable"}

    def use(self, user_data_server: "UsrDataService"):
        user_data_server.edit_chat([])
        return "你喝下了这瓶淡蓝色的神秘药水...\n（与奈咲酱的聊天内容清空了）"




