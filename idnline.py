import asyncio
from telethon import Button
from .. import utils, loader

class InlMod(loader.Module):
	"""инлайн"""
	strings = {"name": "GayMod"}
    
	def inlcmd(self, message):
		"""Нажимает"""
		reply = await event.get_reply_message()
		inline_keyboard = reply.reply_markup
		buttons = await reply.get_buttons()
		button = buttons[1][0]
		await button.click()
		await asyncio.sleep(3)
		reply = await event.get_reply_message()
		new_inline_keyboard = reply.reply_markup
		buttons = await reply.get_buttons()
		button = buttons[2][0]
		await button.click()
