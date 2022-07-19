from .. import loader, utils
from datetime import timedelta
from telethon import functions
from telethon.tl.types import Message
import datetime
from datetime import timedelta


@loader.tds
class SheduleMod(loader.Module):
    """Таймеры на ферму"""
    strings = {"name": "SheduleMod"}
    async def shelfcmd(self, message):
        for i in range(101):
            await message.respond("Ферма", schedule=timedelta(seconds=14460 * int(i)))
            await message.delete()

