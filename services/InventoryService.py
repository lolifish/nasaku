from __future__ import annotations
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from services.UsrDataService import UsrDataService

from presets.Items.ItemsLoader import load_items_presets
from models.BaseItem import BaseItem



item_map = load_items_presets()
item_list = set(item_map.keys())

class InventoryService():
    """物品服务类"""
    def __init__(self, user_data_service: "UsrDataService", commit_hook=None):
        self.user_data = user_data_service.user_data
        self.user_data_service = user_data_service
        self._maybe_commit = commit_hook or (lambda: None)    # 支持回调UsrDataService的_maybe_commit
    
    def name_cn(self, item_name) -> Optional[str]:
        if not item_name in item_list:
            return None
        else:
            return item_map[item_name].name_cn

    def get_all(self) -> dict[str, BaseItem]:
        if not self.user_data:
            return {}
        return self.user_data.inventory
    
    def get(self, item_name) -> int:
        inventory = self.get_all()
        num = inventory.get(item_name)
        if not num:
            return 0
        else:
            return num 

    def add(self, item_name, num=1) -> bool:
        if not self.user_data:
            return False
        # 检查物品是否合法
        if not item_name in item_list:
            raise ValueError(f"{item_name} is not an allowed item")
        # 添加物品
        inventory = self.user_data.inventory
        if item_name in inventory.keys():
            inventory[item_name] += num
        else:
            inventory[item_name] = num
        self._maybe_commit()
        return True
    
    def remove(self, item_name, num=1) -> bool:
        if not self.user_data:
            return False
        inventory = self.user_data.inventory
        # 检查物品是否充足
        if num > self.get(item_name):
            return False
        # 成功使用物品
        else:
            inventory[item_name] -= num
            # 如果归零，直接删除以节省空间
            if not inventory[item_name]:
                del inventory[item_name]
            # 自动保存
            self._maybe_commit()
            return True
    
    def describe(self, item_name) -> Optional[str]:
        if not self.user_data:
            return None
        if not self.get(item_name):
            return None
        return item_map[item_name].describe
    
    def use(self, item_name, remove_item=True) -> Optional[str]:
        if not self.user_data:
            return None
        if not self.get(item_name):
            return None
        # 使用物品
        text = item_map[item_name].use(self.user_data_service)
        # 扣除
        if remove_item:
            self.remove(item_name, 1)
        return text


if __name__ == "__main__":
    from services.UsrDataService import UsrDataService
    user_data_service = UsrDataService(2571610591)
    inventory = InventoryService(user_data_service)

    print(inventory.get_all())
    print(inventory.add("Berry", 2))
    print(inventory.get("Berry"))
    print(inventory.get_all())
    print(inventory.remove("Berry", 1))
    print(inventory.remove("Berry"))
    print(inventory.get_all())
    print(inventory.use("Berry"))

    #inventory.add("NotAllowedItem")
