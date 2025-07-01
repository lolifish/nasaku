import importlib
import inspect
import os

from models.BaseItem import BaseItem

ItemsFolder = "./presets/Items/instances"
ImportPath = "presets.Items.instances"

def load_items_presets() -> dict[str, BaseItem]:
    item_map = {}
    item_files = os.listdir(ItemsFolder)

    for item_file in item_files:
        if not item_file.endswith(".py"):
            continue
        # 引入模块
        module = importlib.import_module(f"{ImportPath}.{item_file[:-3]}")
        # 遍历所有成员，找到BaseItem的子类
        for _, obj in inspect.getmembers(module, inspect.isclass):
            if issubclass(obj, BaseItem) and obj is not BaseItem:
                instance = obj()  # 实例化
                item_map[instance.name_en] = instance

    return item_map

if __name__ == "__main__":
    print(load_items_presets())
    print(load_items_presets()["Berry"].name_cn)
