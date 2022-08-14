from .. import loader, utils
import asyncio
from telethon.tl.types import MessageEntityTextUrl
import json as JSON

class IDMod(loader.Module):
	"Показывает @id по реплаю."
	strings={"name": "IDMod"}

	async def ииcmd(self, message):
		"Показывает @id по списку.\nИспользуй: .ии (аргумент) (аргумент) (аргумент)...\nВ качестве аргумента используй цифры со списка."
		reply = await message.get_reply_message()
		a = reply.text
		count_st = 0
		count_hf = 0
		if not reply:
			await message.edit('Нет реплая❗️')
			return
		args = utils.get_args_raw(message)
		list_args=[]
		if not args:
			await message.edit('Нет аргументов❗️')
			return
		await message.delete()
		for i in args.split(' '):
			if '-' in i:
				ot_do = i.split('-')
				try:
					for x in range(int(ot_do[0]),int(ot_do[1])+1):
						list_args.append(str(x))
				except:
					await message.respond('Используй правильно функцию "от-до"❗️')
					return
			else:
				list_args.append(i)
		lis = []
		for i in a.splitlines():
			lis.append(i)
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
							list = []
							for i in link.split('='):
								list.append(i)
							await message.reply(f'.ид @{list[1]}')
							break
						elif link.startswith('https://t.me'):
							a ='@' + str(link.split('/')[3])
							await message.reply(f'.ид {a}')
							break
						else:
							await message.reply('Ты че делаешь, чо за хуйня?')
							break
			await asyncio.sleep(5)
		await message.delete() 

		if not count_st:
			await message.edit('Не найдено ни одного совпадения в начале строк с аргументами❗️')

		elif not count_hf:
			await message.edit('Не найдено ни одной ссылки❗️')

		elif len(list_args) >= 3:
			await message.respond('<b>Извлечение @id успешно завершено.</b>')

	async def иcmd(self, message):
		"Показывает @id по реплаю.\nИспользуй: .и (в ответ на реплай)"
		reply = await message.get_reply_message()
		json = JSON.loads(reply.to_json())
		for i in range(0, len(reply.entities) ):
			try:
				link = json["entities"][i]["url"]
				if link.startswith('tg'):
					list = []
					for i in link.split('='):
						list.append(i)
					await message.reply('.ид @' + list[1])
				elif link.startswith('https://t.me'):
					a ='@' + str(link.split('/')[3])
					await message.delete()

					await message.reply(f'.ид {a}')
				else:
					await message.reply('что за хуета?')
			except:
				await message.reply(".ид " + reply.raw_text[json["entities"][i]["offset"]:json["entities"][i]["offset"]+json["entities"][i]["length"]] )
			await asyncio.sleep(5)
		await message.delete() 
