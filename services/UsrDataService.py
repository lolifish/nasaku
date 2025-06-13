from datetime import date

from services.InventoryService import InventoryService
from infra.UsrDB import UsrDB
from models.UsrData import UsrData

db = UsrDB()

class UsrDataService():
    """用户数据服务类"""
    def __init__(self, user_id, auto_create=False):
        self.auto_commit = False
        self.has_user = False
        self.user_id = user_id
        self.user_data = db.get(user_id)
        # 创建新用户数据
        if (self.user_data):
            self.has_user = True
        else:
            if auto_create:
                db.create(user_id)
                self.user_data = db.get(user_id)
                self.has_user = True
            else:
                self.has_user = False

        # 实例化InventoryService
        self.inventory = InventoryService(self, self._maybe_commit)

    # 上下文，用于支持多次操作后再保存，节省性能
    def __enter__(self):
        self.auto_commit = False
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:  # 没异常时提交
            db.save(self.user_data)
            db.commit()
        self.auto_commit = True
    # 自动commit
    def _maybe_commit(self):
        if self.auto_commit:
            db.save(self.user_data)
            db.commit()

    # 计数类货币，如fish、imp
    _allowed_currency = {"fish", "imp"}

    def get_currency(self, name) -> int:
        if not self.user_data:
            return 0
        if not name in self._allowed_currency:
            raise ValueError(f"{name} is not a allowed currency: {str(self._allowed_currency)}")
        return getattr(self.user_data, name)
    
    def adjust_currency(self, name, adjust_num, ignore_neg=False) -> bool:
        if not self.user_data:
            return None
        if not name in self._allowed_currency:
            raise ValueError(f"{name} is not a allowed currency: {str(self._allowed_currency)}")
        # 检查是否会导致负数
        new_value = getattr(self.user_data, name) + adjust_num
        if (not ignore_neg) and (new_value<0):
            return False
        # 修改
        setattr(self.user_data, name, new_value)
        self._maybe_commit()
        return True
    
    def get_fish(self):
        return self.get_currency("fish")
    def get_imp(self):
        return self.get_currency("imp")

    def adjust_fish(self, num:int):
        return self.adjust_currency("fish", num)
    def adjust_imp(self, num:int):
        return self.adjust_currency("imp", num)
    
    
    # AI聊天记录数据
    def get_chat(self) -> list:
        if not self.user_data:
            return None
        else:
            return self.user_data.chat
    def add_chat(self, new_chat: dict) -> bool:
        if not self.user_data:
            return False
        self.user_data.chat.append(new_chat)
        self._maybe_commit()
        return True
    def edit_chat(self, all_chats: list) -> bool:
        if not self.user_data:
            return False
        self.user_data.chat = all_chats
        self._maybe_commit()
        return True
    
    # 签到时间数据
    def get_signin(self) -> date:
        if not self.user_data:
            return None
        return self.user_data.signin
    def edit_signin(self, date: date) -> bool:
        if not self.user_data:
            return False
        else:
            self.user_data.signin = date
            self._maybe_commit()
            return True


if __name__ == "__main__":
    id = 2571610591
    data = db.get(id)
    
    with UsrDataService(id) as ud:
        print(data.fish, ud.get_fish())
        print(ud.adjust_fish(5))
        print(ud.adjust_imp(-100000))
        print(data.fish, ud.get_fish())

    ud = UsrDataService(id)
    print(ud.get_chat())

    print(ud.inventory.get_all())
    ud.inventory.add("Berry")
    print(ud.inventory.get_all())


