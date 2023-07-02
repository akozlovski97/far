__version__ = (1, 5, 6)
# meta developer: Тёма
from .. import loader, utils
import asyncio, re, telethon, string

class data:
    owner_id = [ 5438261148 ]
    dovs_ids = [ 5220558050, 5438261148 ]
  
class CowMod(loader.Module):
    """Коров`яча доверка
Использование: а (аргумент)\n
Аргументы:
Для управления коровкой — мук, мулс, муд, мув, муз, муф, муг, муко, муку, мул, муб, муби, пок
Для управления телям — бб, ббт, ббз, ббц, ббу, ббп, ббд, ббя, ббч, ббс, ббм, бби
Для управления инлайн кнопками — (-∞; +∞)"""
    strings = {"name": "CowMod"}
    async def client_ready(self, client_var, db):
        global client
        
    async def watcher(self, message):
        if not isinstance(message, telethon.tl.types.Message): return
        author, content = await message.get_sender(), message.message
        reply = await message.get_reply_message()
        
#Действия с коровкой
        if author.id in data.dovs_ids and re.match(r'А\s+мук$', content, re.IGNORECASE):
            await message.respond("Мук")
        if author.id in data.dovs_ids and re.match(r'А\s+мулс$', content, re.IGNORECASE):
            await message.respond("Мулс")
        if author.id in data.dovs_ids and re.match(r'А\s+муф$', content, re.IGNORECASE):
            await message.respond("Муф")
        if author.id in data.dovs_ids and re.match(r'А\s+мув$', content, re.IGNORECASE):
            await message.respond("Мув") 
        if author.id in data.dovs_ids and re.match(r'А\s+муз$', content, re.IGNORECASE):
            await message.respond("Муз")  
        if author.id in data.dovs_ids and re.match(r'А\s+муд$', content, re.IGNORECASE):
            await message.respond("Муд")
        if author.id in data.dovs_ids and re.match(r'А\s+муко$', content, re.IGNORECASE):
            await message.respond("Муко")
        if author.id in data.dovs_ids and re.match(r'А\s+муку$', content, re.IGNORECASE):
            await message.respond("Муку")
        if author.id in data.dovs_ids and re.match(r'А\s+мул$', content, re.IGNORECASE):
            await message.respond("Мул")
        if author.id in data.dovs_ids and re.match(r'А\s+муг$', content, re.IGNORECASE):
            await message.respond("Муг")
        if author.id in data.dovs_ids and re.match(r'А\s+муби$', content, re.IGNORECASE):
            await message.respond("Муби")
        if author.id in data.dovs_ids and re.match(r'А\s+муб$', content, re.IGNORECASE):
            await message.respond("Муб")
        if author.id in data.dovs_ids and re.match(r'А\s+пок$', content, re.IGNORECASE):
            await message.respond("Пок")

#Действия с теля
        if author.id in data.dovs_ids and re.match(r'А\s+бб$', content, re.IGNORECASE):
            await message.respond("Бб")
        if author.id in data.dovs_ids and re.match(r'А\s+ббц$', content, re.IGNORECASE):
            await message.respond("Ббц")
        if author.id in data.dovs_ids and re.match(r'А\s+ббу$', content, re.IGNORECASE):
            await message.respond("Ббу")
        if author.id in data.dovs_ids and re.match(r'А\s+ббз$', content, re.IGNORECASE):
            await message.respond("Ббз")
        if author.id in data.dovs_ids and re.match(r'А\s+ббп$', content, re.IGNORECASE):
            await message.respond("Ббп")
        if author.id in data.dovs_ids and re.match(r'А\s+ббд$', content, re.IGNORECASE):
            await message.respond("Ббд")
        if author.id in data.dovs_ids and re.match(r'А\s+ббя$', content, re.IGNORECASE):
            await message.respond("Ббя")
        if author.id in data.dovs_ids and re.match(r'А\s+ббч$', content, re.IGNORECASE):
            await message.respond("Ббч")
        if author.id in data.dovs_ids and re.match(r'А\s+ббс$', content, re.IGNORECASE):
            await message.respond("Ббс")
        if author.id in data.dovs_ids and re.match(r'А\s+ббм$', content, re.IGNORECASE):
            await message.respond("Ббм")
        if author.id in data.dovs_ids and re.match(r'А\s+бби$', content, re.IGNORECASE):
            await message.respond("Бби")
        if author.id in data.dovs_ids and re.match(r'А\s+ббт$', content, re.IGNORECASE):
            await message.respond("Ббт")

#Действия с инлайнами
        args = utils.get_args_raw(message)
        try:
            n = int(args)-1
            if author.id in data.dovs_ids and re.search(r'А\s+' + str(args), content, re.IGNORECASE):
                await reply.click(n)
        except ValueError: return
