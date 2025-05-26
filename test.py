import httpx
import asyncio
import re

async def random_setu():
    url = "https://api.anosu.top/img"
    headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36"}
    async with httpx.AsyncClient(headers=headers) as client:
        response = await client.get(url, headers=headers, follow_redirects=True)
        print(response.status_code==httpx.codes.OK)
    with open("./data/cache/img.jpg", "wb") as f:
        f.write(response.content)

    # 提取图像id
    print(response.url)
    id = re.findall(r"bjh/(.+)\.", str(response.url))[0]
    return id

asyncio.run(random_setu())