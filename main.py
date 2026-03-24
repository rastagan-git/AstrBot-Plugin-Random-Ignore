import random
import logging
from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register

logger = logging.getLogger("astrbot")

@register("random_ignore", "YourName", "按设定概率忽略私聊和被@/回复的消息", "1.0.0")
class RandomIgnorePlugin(Star):
    def __init__(self, context: Context, config: dict):
        super().__init__(context)
        self.config = config

    @filter.on_decorating_message()
    async def intercept_message(self, event: AstrMessageEvent):
        # 实时从配置读取最新的概率设置，默认值为 0.3
        ignore_prob = self.config.get("ignore_probability", 0.3)

        # 1. 判断是否为私聊消息
        # 在大多数平台，如果获取不到 group_id 则为私聊
        is_private_chat = not bool(event.get_group_id())
        
        # 2. 判断是否在群聊中被 @ 或被回复
        # 依赖 AstrBot message_obj 提供的原生判断方法
        is_at_bot = False
        is_reply_bot = False
        
        if hasattr(event.message_obj, 'is_at_me'):
            is_at_bot = event.message_obj.is_at_me()
            
        # 根据不同协议适配器，被回复有时被统一算作 at_me，此处预留独立判断的兼容逻辑
        if hasattr(event.message_obj, 'is_reply_me'):
            is_reply_bot = event.message_obj.is_reply_me()

        # 3. 只有当满足“私聊”或“被@”或“被回复”时，才进行概率投掷
        if is_private_chat or is_at_bot or is_reply_bot:
            # 随机生成一个 0.0 到 1.0 的浮点数
            rand_val = random.random()
            
            # 如果生成的随机数小于设定的概率阈值，则执行拦截
            if rand_val < ignore_prob:
                logger.info(f"[RandomIgnore] 触发随机忽略机制 (设定概率: {ignore_prob}, 本次随机数: {rand_val:.2f})")
                
                # 中断事件传播，底层框架将不再把这条消息交给大模型或后续插件处理
                if hasattr(event, 'stop_event'):
                    event.stop_event()
                else:
                    logger.warning("[RandomIgnore] 未能在 event 中找到 stop_event() 方法，可能版本不兼容，拦截失败。")