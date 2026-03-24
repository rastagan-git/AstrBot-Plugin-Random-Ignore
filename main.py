import random
from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star
from astrbot.api import logger

class RandomIgnorePlugin(Star):
    def __init__(self, context: Context, config: dict = None):
        super().__init__(context)
        self.config = config or {}

    # 使用 on_llm_request 钩子，在发给大模型之前进行物理拦截
    # 注意：V4 版本的该钩子强制要求接收 event 和 req 两个参数
    @filter.on_llm_request()
    async def intercept_before_llm(self, event: AstrMessageEvent, req):
        ignore_prob = self.config.get("ignore_probability", 0.3)

        is_private_chat = False
        is_at_or_reply = False
        
        # 1. 识别是否为私聊（通常群聊消息会携带 group_id，为空则判定为私聊）
        if hasattr(event.message_obj, 'group_id') and not event.message_obj.group_id:
            is_private_chat = True
            
        # 2. 识别是否被 @ 或被回复
        if hasattr(event.message_obj, 'is_at_me') and event.message_obj.is_at_me():
            is_at_or_reply = True
            
        if hasattr(event.message_obj, 'is_reply_me') and event.message_obj.is_reply_me():
            is_at_or_reply = True
            
        # 兼容部分适配器的统一唤醒标记
        if hasattr(event, 'is_at_or_wake_command') and getattr(event, 'is_at_or_wake_command'):
            is_at_or_reply = True

        # 3. 执行概率拦截
        if is_private_chat or is_at_or_reply:
            rand_val = random.random()
            
            if rand_val < ignore_prob:
                logger.info(f"[RandomIgnore] 触发上游物理拦截 (设定概率: {ignore_prob}, 本次随机数: {rand_val:.2f})")
                
                # 彻底中断事件传播，Bot 会像没看见这条消息一样，不耗 Token，不写记忆
                event.stop_event()
