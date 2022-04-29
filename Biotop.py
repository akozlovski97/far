from .. import loader
import telethon
import time
import asyncio 

px = int(2)
idp = "@ajshsuwj"
mes = "Биотоп"

class BioMod(loader.Module):
	strings = {"name": "BioMod"}
	async def ruscmd(self, message):
		while(1==1):
			await message.edit(idp, mes)
			await sleep(7)
