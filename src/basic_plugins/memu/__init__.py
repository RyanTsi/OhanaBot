from nonebot.adapters.onebot.v11.message import Message, MessageSegment
from nonebot.permission import SUPERUSER
from nonebot.matcher import Matcher
from nonebot.plugin import PluginMetadata
from nonebot import on_command, get_driver
from nonebot.params import CommandArg
from .Data_manager import Data_manager
from nonebot import logger

__plugin_meta__ = PluginMetadata(
    name="菜单",
    description="这是一个菜单插件",
    usage="输入#help以获取功能菜单, 输入#help + 对应的数字以获取对应菜单的详细功能",
    extra={
        "unique_name": "menu",
        "author": "xjq <466010106@qq.com>",
        "version": "1.0.0"
    }
)

driver = get_driver()


@driver.on_startup
async def _():
    data_manager.load_plugin_info()


data_manager = Data_manager()
menu_switch = True


async def menu_switch_rule():
    return menu_switch


menu = on_command("菜单", aliases={
                  "menu", "帮助", "功能", "help"}, priority=5, block=True, rule=menu_switch_rule)
switch_on = on_command(("help","on"), priority=5, permission=SUPERUSER, block=True)
switch_off = on_command(("help","off"), priority=5, permission=SUPERUSER, block=True)
set_width = on_command(("help","set_width"), priority=1, block=True, permission=SUPERUSER)

@switch_on.handle()
async def _(matcher: Matcher):
    global menu_switch
    menu_switch = True
    await matcher.finish("菜单已经开启")


@switch_off.handle()
async def _(matcher: Matcher):
    global menu_switch
    menu_switch = False
    await matcher.finish("菜单已经关闭")

@set_width.handle()
async def _(matcher : Matcher, args: Message = CommandArg()):
    width = args.extract_plain_text().strip()
    logger.info(width)
    if width != None and width.isdigit():
        data_manager.set_with(int(width))
        await matcher.finish(f"成功设置宽度为{width}")
    else:
        await matcher.finish(f"请输入合法的宽度")


@menu.handle()
async def _(arg: Message = CommandArg()):
    msg = arg.extract_plain_text().strip()
    if not msg:
        await menu.finish(MessageSegment.image(await data_manager.get_menu_names()))
    elif not msg.isdigit() or eval(msg) > len(data_manager.plugins_menu_list) or eval(msg) <= 0:
        await menu.finish(f"请输入help + 阿拉伯数字{1}~{len(data_manager.plugins_menu_list)}以获取菜单的详细信息")
    else:
        await menu.finish(MessageSegment.image(await data_manager.get_details(eval(msg))))
