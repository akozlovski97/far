from .. import loader, utils
import asyncio

class GadMod(loader.Module):
    "Gad"
    strings = {"name": "GadMod"}

    async def gadcmd(self, message):
        "Gad"
        await message.respond(".zarlist @13011384 1000")
        await asyncio.sleep(1)
        await message.respond(".zarlist @23103184 1000")
        await asyncio.sleep(1)
        await message.respond(".zarlist @25215184 1000")
        await asyncio.sleep(1)
        await message.respond(".zarlist @63211184 1000")
        await asyncio.sleep(1)
        await message.respond(".zarlist @73543184 1000")
        await asyncio.sleep(1)
        await message.respond(".zarlist @13443184 1000")
        
