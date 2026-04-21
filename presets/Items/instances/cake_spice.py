from models.BaseItem import BaseItem

class PosionOfForgetting(BaseItem):
    name_en = "Spice Cake"
    name_cn = "香草蛋糕"
    describe = "看起来非常美味的香草蛋糕~\n是店里的热卖产品"
    tags = {"gift", "tradable"}

    gift_imp = 5
    gift_replies = [
        "香草蛋糕~香草蛋糕~好香呀！谢谢主人~",
        "给...给我吃喵？（流口水）\n这个看着就很好吃诶！\n主人要不要也尝一口？"
        "喵呜！是香草蛋糕的味道！喵的鼻子灵吧~\n好美味，谢谢主人！",
    ]
