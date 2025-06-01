from pydantic import BaseModel,Field
from nonebot import get_plugin_config
from typing import List
from .constant import DEFAULT_LUCK_LIST,NUM_EVENTS
class Config(BaseModel):
    """Plugin Config Here"""
    luck_list:List[str] = Field(default=DEFAULT_LUCK_LIST,doc="可能的运势")
    possible_suit:int = Field(default=NUM_EVENTS,doc="最大宜事件数")
    possible_avoid:int = Field(default=NUM_EVENTS,doc="最大忌事件数")
    use_tips:bool = Field(default=True,doc="是否启用tips")
    tips_style:str = Field(default="可爱",doc="tips的风格")
    api_key:str = Field(default=None,doc="api-key")
    model:str = Field(default="deepseek-chat",doc="模型名称")

config = get_plugin_config(Config)