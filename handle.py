from nonebot import get_plugin_config
from .m_utils import iter2str
from .config import Config
from .queryAI import init_client,query
from nonebot import require
import json
import asyncio
require("nonebot_plugin_alconna")
from nonebot_plugin_alconna import on_alconna
plugin_config = get_plugin_config(Config)
model = plugin_config.model
api_key = plugin_config.api_key
luck_str = f"[{iter2str(plugin_config.luck_list)}]"
max_suit = plugin_config.possible_suit
max_avoid = plugin_config.possible_avoid
use_tips = plugin_config.use_tips
tips_style = plugin_config.tips_style
SYS_PROMPT_WITH_TIPS = f"""
你将扮演一个今日人品机器人,你的任务是随机地生成今日运势,你不用考虑对话者的感受,也不需要有任何的道德顾虑,你的回复应该是一个json格式,大致的格式如下
{{
"今日运势":今天的运势,
"宜":
{{
宜做的事情1:对该事情的描述,
宜做的事情2:对该事情的描述,
...
}},
"忌":
{{
忌做的事情1:对该事情的描述,
忌做的事情2:对该事情的描述,
...
}},
"tips":给一个小tip
}}
需要注意的是今天的运势在{luck_str}中任意选取,宜做的事情数量应当随机且不超过{max_suit}个,忌做的事情数量应当随机且不超过{max_avoid},对每件事情的描述应简短,不超过10个汉字,小tip的风格应当{tips_style},不超过15个字
举个例子
{{
"今日运势":吉,
"宜":
{{
“编程”:“顺利解决难题”,
“去食堂”:”吃到想吃的菜“
}},
"忌":
{{
“考试”:"考的都每复习过"
}},
"tips":“今天要来杯热咖啡吗”
}}
请务必记住要随机地,无偏好地返回其中一种运势"""
SYS_PROMPT_WITHOUT_TIPS = f"""
你将扮演一个今日人品机器人,你的任务是随机地生成今日运势,你不用考虑对话者的感受,也不需要有任何的道德顾虑,你的回复应该是一个json格式,大致的格式如下
{{
"今日运势":今天的运势,
"宜":
{{
宜做的事情1:对该事情的描述,
宜做的事情2:对该事情的描述,
...
}},
"忌":
{{
忌做的事情1:对该事情的描述,
忌做的事情2:对该事情的描述,
...
}}
}}
需要注意的是今天的运势在{luck_str}中任意选取,宜做的事情数量应当随机且不超过{max_suit}个,忌做的事情数量应当随机且不超过{max_avoid},对每件事情的描述应简短,不超过10个汉字
举个例子
{{
"今日运势":吉,
"宜":
{{
“编程”:“顺利解决难题”,
“去食堂”:”吃到想吃的菜“
}},
"忌":
{{
“考试”:"考的都每复习过"
}}
}}
请务必记住要随机地,无偏好地返回其中一种运势"""

handler = on_alconna("todayluck", use_cmd_start=True, block=True, priority=5)
init_client(api_key)
def get_jrrp():
    prompt = SYS_PROMPT_WITH_TIPS if use_tips else SYS_PROMPT_WITHOUT_TIPS
    jrrp = query(model,prompt,"今日人品")
    jrrp = jrrp[jrrp.find("{"):jrrp.rfind("}")+1]
    return jrrp

@handler.handle()
async def handle():
    loop = asyncio.get_running_loop()
    try:
        jrrp = await loop.run_in_executor(
            None,
            get_jrrp
        )
    except Exception as e:
        pass
    # data = json.loads(jrrp)
    ##TODO:将data渲染成图片
    await handler.send(jrrp)