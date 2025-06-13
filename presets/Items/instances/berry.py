from models.BaseItem import BaseItem

class Berry(BaseItem):
    name_en = "Berry"
    name_cn = "浆果"
    describe = "一种美味的浆果，可以食用，也能吸引鱼类和动物"
    tags = {"gift", "material", "tradable"}

    gift_imp = 1
    gift_replys = [
        "是甜甜的浆果喵？很美味呢，好好吃，谢谢主人！",
        "喵~奈咲酱很喜欢这个浆果的香气，谢谢主人啦喵~"
        "喵呜！好甜的浆果~做成蛋糕的话说不定会更美味呢！",
    ]
