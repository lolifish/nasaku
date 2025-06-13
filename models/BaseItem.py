from __future__ import annotations
from typing import Optional, TYPE_CHECKING
from abc import ABC, abstractmethod

if TYPE_CHECKING:
    from services.UsrDataService import UsrDataService


allowed_tags = {
    "usable",       # 可使用
    "gift",         # 可赠送
    "material",     # 可作为合成材料
    "tradable",     # 可交易
    "rare",         # 珍贵物品
}

class BaseItem(ABC):
    """物品的抽象基类"""
    name_en: str = None             # 必填，英文名
    name_cn: str = None             # 必填，中文名
    describe: str = None            # 必填，描述
    tags: list[str] = []            # 物品标签

    gift_imp: int = 0               # 赠送物品能产生的好感度
    gift_replies: list[str] = []    # 赠送物品产生的消息

    def __init__(self):
        self._validate_required_fields()
        self._validate_tags()

    # 错误检查
    def _validate_required_fields(self):
        missing = []
        for attr in ("name_en", "name_cn", "describe"):
            if not getattr(self, attr):
                missing.append(attr)
        if missing:
            raise ValueError(f"{self.__class__.__name__} lost necessary property: {', '.join(missing)}")
    def _validate_tags(self):
        for tag in self.tags:
            if tag not in allowed_tags:
                raise ValueError(f"{tag} is not an allowed tag: {allowed_tags}")

    @property
    def name(self):
        """物品的英文名"""
        return self.name_en

    def use(self, user_data_server: Optional["UsrDataService"] = None) -> str | None:
        """物品使用逻辑。返回使用消息，None表示不可用"""
        return None





if __name__ == "__main__":
    class Apple(BaseItem):
        name_en = "apple"
        name_cn = "苹果"
        describe = "一种美味的水果，可以吃"
        gift_imp = 1
        tags = ["gift"]

        @staticmethod
        def use():
            return "吃掉苹果了"
    
    apple = Apple()
    print(apple.name, apple.name_en, apple.describe, apple.use(), apple.tags, apple.gift_imp)
