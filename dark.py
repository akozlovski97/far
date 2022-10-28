from .. import loader, utils
from datetime import timedelta
from telethon import functions
from telethon.tl.types import Message
import datetime
from datetime import timedelta


@loader.tds
class TaimerMod(loader.Module):
    """Таймеры на Дарка"""
    strings = {"name": "TaimerMod"}
    async def darkcmd(self, message):
        for i in range(101):
            await message.respond("Заразить @5394249008", schedule=timedelta(seconds=21700 * int(i)))
            await message.delete()
