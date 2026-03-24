import random
from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star
from astrbot.api import logger

# 注意：移除了 @register，由外部的 metadata.yaml 接管元数据
class RandomIgnorePlugin(Star):
    def __init__(self, context: Context, config: dict = None):
        super().__init__(context)
        # 兼容处理 config 注入
        self.config = config or {}

    # 使用消息前置装饰器进行拦截
    @filter.on_decorating_message()
    async def intercept_message(self, event: AstrMessageEvent):
        ignore_prob = self.config.get("ignore_probability", 0.3)

        is_private_chat = not bool(event.get_group_id())
        
        is_at_bot = False
        is_reply_bot = False
        
        if hasattr(event.message_obj, 'is_at_me'):
            is_at_bot = event.message_obj.is_at_me()
            
        if hasattr(event.message_obj, 'is_reply_me'):
            is_reply_bot = event.message_obj.is_reply_me()

        if is_private_chat or is_at_bot or is_reply_bot:
            rand_val = random.random()
            
            if rand_val < ignore_prob:
                logger.info(f"[RandomIgnore] 触发拦截机制 (概率: {ignore_prob}, 随机数: {rand_val:.2f})")
                
                # 尝试中断事件传播。如果 V4 更改了底层的拦截 API，请观察终端此处的 Warning 日志
                if hasattr(event, 'stop_event'):
                    event.stop_event()
                else:
                    # 备用拦截方案：直接将当前消息的文本清空或置位，阻断大模型的后续处理
                    event.message_str = ""
                    logger.warning("[RandomIgnore] 当前 V4 核心未暴露 stop_event，已尝试通过清空 message_str 拦截。")
