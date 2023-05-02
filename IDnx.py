from .. import loader, utils
from telethon.tl.types import MessageEntityTextUrl
import json

class IDnotexecMod(loader.Module):
    "Показывает список @id"
    strings = {"name": "IDnotexecMod"}

    async def ncmd(self, message):
        "Лист ников и ID биотопа"
        reply = await message.get_reply_message()
        if not reply:
            await message.edit("<b>Ответь на сообщение!</b>")
            return
        text = reply.raw_text.splitlines()[1:]
        users = [t.split("|")[1].strip() for t in text]
        entities = reply.entities or []
        count = 1
        result = []
        for entity in entities:
            if not isinstance(entity, utils.misc.MessageEntityUrl):
                result.append(f"{count}. что за хуета?")
                count += 1
                continue
            link = entity.url
            if link.startswith('tg'):
                chat_id = link.split('=')[1]
                try:
                    user = await message.client.get_entity(chat_id)
                    result.append(f"{count}. <b>{user.first_name}</b> - <code>@{user.username}</code> | <u>{users[count-1]}</u>")
                except:
                    result.append(f"{count}. что за хуета?")
            elif link.startswith('https://t.me'):
                username = link.split('/')[3]
                result.append(f"{count}. <code>@{username}</code> | <u>{users[count-1]}</u>")
            count += 1
        await message.reply('\n'.join(result), parse_mode="html")
        await message.delete()
