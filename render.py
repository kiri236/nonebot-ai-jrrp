from nonebot import require
from typing import Dict
from .constant import HTML_TEMPLATE
from jinja2 import Template
require("nonebot_plugin_htmlrender")
from nonebot_plugin_htmlrender import md_to_pic,html_to_pic
def get_event(data:Dict)->str:
    ans = ""
    for act,desc in data.items():
        ans += f"{act}:{desc}\n"
    return ans
async def render_jrrp(data:Dict)->bytes:
    md = f"""# {data["name"]}的今日运势:{data["今日运势"]}
## 宜
{get_event(data["宜"])}
## 忌
{get_event(data["忌"])}
## tips
{data["tips"]}"""
    pic = await md_to_pic(md)
    return pic

async def render_jrrp_jinja(data:Dict)->bytes:
    template = Template(HTML_TEMPLATE)
    html = template.render(name=data["name"],date=data["date"],fortune=data["今日运势"],tips=data["tips"],宜=data["宜"],忌=data["忌"])
    pic = await html_to_pic(html=html)
    return pic