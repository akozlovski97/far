from .. import loader, utils
import asyncio, pytz, re, telethon
from telethon.tl.types import MessageEntityTextUrl
import json as JSON
from datetime import datetime, date, time

class IDDDMod(loader.Module):
	"Облегчает жизнь смертным."
	strings={"name": "IDDDMod"}
	
	async def client_ready(self, client, db):
		self.db = db
		if not self.db.get("NumMod", "exUsers", False):
			self.db.set("NumMod", "exUsers", [])
		if not self.db.get("NumMod", "infList", False):
			self.db.set("NumMod", "infList", {})
		
	async def idcmd(self, message):
		"Заражает по списку.\nВ качестве аргументов используй числа или первые символы строки.\nИспользуй:.з (аргумент) (аргумент) (аргумент)..."
		reply = await message.get_reply_message()
		a = reply.text
		exlist = self.db.get("NumMod", "exUsers")
		count_st = 0
		count_hf = 0
		if not reply:
			await message.edit('<b>Нет реплая❗️</b>')
			return
		args = utils.get_args_raw(message)
		list_args=[]
		if not args:
			await message.edit('<b>ID не обнаружен❗️</b>')
			return
		for i in args.split(' '):
			if '-' in i:
				ot_do = i.split('-')
				try:
					for x in range(int(ot_do[0]),int(ot_do[1])+1):
						list_args.append(str(x))
				except:
					await message.respond('<b>Используй правильно функцию "от-до"</b>❗️')
					return
			else:
				list_args.append(i)
		lis = a.splitlines()
		for start in list_args:
			for x in lis:
				if x.lower().startswith(str(start.lower())):
					count_st = 1
					if 'href="' in x:
						count_hf = 1
						b=x.find('href="')+6
						c=x.find('">')
						link = x[b:c]
						if link.startswith('tg'):
							list = '@' + link.split('=')[1]
							if list in exlist:
								await message.reply(f'<b>Исключение</b>: <code>{list}</code>')
							else:
								await message.reply(f'.ид {list}')
							break
						elif link.startswith('https://t.me'):
							a ='@' + str(link.split('/')[3])
							if a in exlist:
								await message.reply(f'<b>Исключение</b>: <code>{a}</code>')
							else:
								await message.reply(f'.ид {a}')
							break
						else:
							await message.reply('<b>Ты дурак⁉️</b>')
							break
			await asyncio.sleep(5)
		await message.delete() 
				
		if not count_st:
			await message.edit('<b>Не найдено ни одного совпадения в начале строк с аргументами❗️</b>')
			
		elif not count_hf:
			await message.edit('<b>Не найдено ни одной ссылки❗️</b>')
			
		elif len(list_args) >= 3:
			await message.respond('<b>ИД успешно завершены.</b>')
