import sys
sys.path.append("./")

import httpx
import io
from PIL import ImageFont, ImageDraw, Image

from utils.config import config

TOKEN_FILE = "./data/luxun/token.txt"
IMAGE = "./data/luxun/luxun.jpg"
FONT = "./data/luxun/msyh.ttf"

# 获取access_token
def get_token():
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {
        "grant_type": "client_credentials",
        "client_id": "Gv6h16SrNGCexuu3C5EPhmuU",
        "client_secret": config["baidu_check_text_secret"],
    }
    response = httpx.get(url, params=params)
    return response.json()["access_token"]

# 提交审核文本，返回结果
def check_text(text) -> bool:
    # 获取token
    with open(TOKEN_FILE) as f:
        token = f.read()
    url = "https://aip.baidubce.com/rest/2.0/solution/v1/text_censor/v2/user_defined"
    headers = {"content-type": "application/x-www-form-urlencoded"}
    data = {"text": text, "access_token": token}
    response = httpx.post(url, headers=headers, data=data)
    response = response.json()
    # 检测token过期情况，出错则递归调用
    if "error_code" in response.keys():
        with open(TOKEN_FILE, "w") as f:
            f.write(get_token())
        return check_text(text)
    # 检测结果并返回成功情况
    if response["conclusionType"] != 1:
        return False
    else:
        return True

# 图片生成
def process_img(text):
    img = Image.open(IMAGE, mode="r")
    if len(text) <= 2:
        size = 40
    if len(text) <= 4:
        size = 35
    elif len(text) <= 12:
        size = 28
    else:
        size = 22
    font1 = ImageFont.truetype(FONT, size)
    font2 = ImageFont.truetype(FONT, 25)
    bbox = font1.getbbox(text)
    text_size = bbox[2] - bbox[0]

    draw = ImageDraw.Draw(img)
    # 居中添加文本
    draw.text(
        xy = ((img.size[0]-text_size)/2+int(size/5), 350),
        text = text, fill = (255, 255, 255), font = font1
    )
    # 添加“——鲁迅”
    draw.text(
        xy = (img.size[0]-150, 380+int(size/3)),
        text = "—— 鲁迅", fill = (255, 255, 255), font = font2
    )
    #img.show()
    bytes_img = io.BytesIO()
    img.save(bytes_img, format="JPEG")
    return bytes_img.getvalue()

if __name__ == "__main__":
    print(process_img("哈喽"))