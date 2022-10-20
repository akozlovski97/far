from .. import loader, utils
from datetime import timedelta
from telethon import functions
from telethon.tl.types import Message
import datetime
from datetime import timedelta


@loader.tds
class vkidMod(loader.Module):
    """Таймеры на vkid"""
    strings = {"name": "vkidMod"}
    async def shelfcmd(self, message):
        for i in range(101):
            await message.respond("Вкид", schedule=timedelta(seconds=600 * int(i)))
            await message.delete()
