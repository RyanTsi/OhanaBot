import nonebot
import os
from nonebot.adapters.onebot.v11 import Adapter as ONEBOT_V11Adapter

if not os.path.exists("data") :
    os.mkdir("data")

nonebot.init(apscheduler_autostart=True)

driver = nonebot.get_driver()
driver.register_adapter(ONEBOT_V11Adapter)

nonebot.load_builtin_plugins('echo')

nonebot.load_from_toml("pyproject.toml")

if __name__ == "__main__":
    nonebot.run()
