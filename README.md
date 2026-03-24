# AstrBot-Plugin-Random-Ignore

这是一个用于 AstrBot 的消息过滤插件。它能够在 Bot 收到私聊、群聊被 @ 或被回复时，按设定的概率随机忽略该消息，中断后续的处理流程。

## 功能特性
- 支持通过 WebUI 独立配置忽略概率（范围 0.0 - 1.0）。
- 自动拦截私聊消息。
- 自动拦截群聊中被 @ 的消息。
- 自动拦截群聊中被回复的消息（依赖平台适配器支持）。

## 安装方法
1. 在 AstrBot 的 `data/plugins/` 目录下创建一个名为 `astrbot_plugin_random_ignore` 的文件夹。
2. 将 `main.py` 和 `_conf_schema.json` 放入该文件夹中。
3. 重启 AstrBot 进程。

## 配置说明
进入 AstrBot 的 WebUI 管理面板，在插件配置页面中找到本插件，调整 `ignore_probability` 的值：
- `0.3`：默认值，表示有 30% 的概率忽略消息。
- `0.0`：完全不忽略（必定处理）。
- `1.0`：100% 忽略（等同于对特定交互静音）。
