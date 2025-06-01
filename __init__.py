from nonebot import get_plugin_config
from nonebot.plugin import PluginMetadata
from . import handle
from .config import Config

__plugin_meta__ = PluginMetadata(
    name="nonebot_ai_jrrp",
    description="",
    usage="",
    config=Config,
)

config = get_plugin_config(Config)

