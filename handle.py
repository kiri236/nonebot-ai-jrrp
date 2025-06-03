from nonebot import get_plugin_config
from .config import Config
from .queryAI import init_client,query
from .prompt import SYS_PROMPT_WITH_TIPS,SYS_PROMPT_WITHOUT_TIPS,use_tips
from nonebot import require
from nonebot.adapters import Event
from .database import DataBase
from datetime import datetime
import json
import asyncio
require("nonebot_plugin_alconna")
from nonebot_plugin_alconna import on_alconna
plugin_config = get_plugin_config(Config)
model = plugin_config.model
api_key = plugin_config.api_key
database = DataBase("todayluck")

handler = on_alconna("todayluck", use_cmd_start=True, block=True, priority=5)
init_client(api_key)
database.create_database()
def get_jrrp():
    prompt = SYS_PROMPT_WITH_TIPS if use_tips else SYS_PROMPT_WITHOUT_TIPS
    jrrp = query(model,prompt,"今日人品")
    jrrp = jrrp[jrrp.find("{"):jrrp.rfind("}")+1]
    return jrrp

@handler.handle()
async def handle(event:Event):
    date = datetime.now().strftime("%Y-%m-%d")
    name = event.get_user_id()
    jrrp = database.query(name,date)
    if jrrp == 0:
        loop = asyncio.get_running_loop()
        try:
            jrrp = await loop.run_in_executor(
                None,
                get_jrrp
            )
            jrrp = json.loads(jrrp)
            jrrp["name"] = name
            jrrp["date"] = date
            database.insert(jrrp)
        except Exception as e:
            pass
    ##TODO:将data渲染成图片
    await handler.send(jrrp["今日运势"])