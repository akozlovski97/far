from .. import loader, utils
import asyncio
from telethon.tl.types import MessageEntityTextUrl
import json as JSON

class NoxMod(loader.Module):
    "Показывает список @id"
    strings = {"name": "NoxMod"}

    async def noxcmd(self, message):
        "Нотексес модуль"
b = reply.raw_text.splitlines()
b.pop(0)
hh = []
for i in b:
 try:
  hh.append(i.split('|')[1])
 except: pass
json = JSON.loads(reply.to_json())
sms = ''
count = 1
for i in range(0, len(reply.entities) ):
 try:
  exp = hh[i]
 except:
  exp = i
 link = json["entities"][i]["url"]
 try:
  if link.startswith('tg'):
   bla = []
   for i in link.split('='):
    bla.append(i)
   b = await message.client.get_entity(int(bla[1]))
   sms+=f'{str(count)}. <b>{b.first_name}</b> - <code>@{b.id}</code> | <u>{exp}</u>\n'
  elif link.startswith('https://t.me'):
   a ='@' + str(link.split('/')[3])
   sms+=f'{str(count)}. <code>{a}</code> | <u>{exp}</u>\n'
  else:
   sms+='{str(count)}. что за хуета?\n'
 except:
  if link.startswith('https://t.me'):
   a ='@' + str(link.split('/')[3])
   sms+=f'{str(count)}. <code>{a}</code> | <u>{exp}</u> \n'
  elif link.startswith('tg'):
   bla = []
   for i in link.split('='):
    bla.append(i)
   sms+=f'{str(count)}. <code>@{bla[1]}</code> | <u>{exp}</u> \n'
 count += 1
await message.reply(sms)
await message.delete()
