import random
from .. import utils, loader
import asyncio, pytz, re, telethon

@loader.tds
class GayMod(loader.Module):
    """Узнай на сколько ты гей!"""
    strings = {"name": "GayMod"}
    
    async def gaycmd(self, message):
        """Покажет на сколько ты гей"""
        await message.respond("<b>Ты гей на</b> " + str(random.randrange(0, 101)) + "%")
