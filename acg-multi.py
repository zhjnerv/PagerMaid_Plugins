import json
import random
import requests
from time import sleep
from pagermaid.listener import listener
from os import remove


@listener(is_plugin=True, outgoing=True, command="acgm",
          description="多网站随机获取二刺螈（bushi） ACG图片")
async def joke(context):
    await context.edit("获取中 . . .")
    status = False
    for _ in range (20): #最多重试20次
        website = random.randint(0, 5)
        if website == 0:
            img = requests.get("http://api.btstu.cn/sjbz/?lx=m_dongman")
        elif website == 1:
            img = requests.get("https://acg.yanwz.cn/api.php")
        elif website == 2:
            img = requests.get("https://img.xjh.me/random_img.php?type=bg&ctype=acg&return=302&device=mobile")
        elif website == 3:
            img = requests.get("https://www.yunboys.cn/sjbz/api.php?method=mobile&lx=dongman")
        elif website == 4:
            headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063','Referer':'https://osk.soloop.ooo/give_me_eropics-l/'}
            img = requests.get("https://osk.soloop.ooo/rdm.php?"+ str(random.random()), headers=headers)
        elif website == 5:
            img = requests.get('https://api.lolicon.app/setu/?r18=0')
        if img.status_code == 200:
            if website == 5:
                tmp = json.loads(img.content)
                img = tmp['data'][0]['url']
                img = requests.get(img)
                if img.status_code != 200:
                    continue #如果返回不正常就赶紧下一回
            with open(r'tu.png', 'wb') as f:
                await context.edit("正在上传图片")
                f.write(img.content)
                await context.client.send_file(
                    context.chat_id,
                    "tu.png",
                    reply_to=None,
                    caption=None
                   )
            try:
                remove('tu.png')
            except:
                pass
            status = True
            break #成功了就赶紧结束啦！

    if not status:
        await context.edit("出错了呜呜呜 ~ 试了好多好多次都无法访问到 API 服务器 。")
        sleep(2)
    await context.delete()
