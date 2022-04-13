from .. import loader, utils
import logging
import asyncio


logger = logging.getLogger(__name__)


def register(cb):
    cb(SpamMod())


@loader.tds
class SpamMod(loader.Module):
    """Пишет много одинаковых сообщений"""
    strings = {"name": "SpamMod",
               "need_spam": "<b>Что? Мне нужно что-то для спама.</b>",
               "spam_urself": "<b>Займитесь спамом.</b>",
               "nice_number": "<b>Хороший номер, братан.</b>",
               "much_spam": "<b>Ха-ха, много спама.</b>"}

    def __init__(self):
        self.name = self.strings["name"]

    async def spamcmd(self, message):
        """.spam <цифра> <сообщение>"""
        use_reply = False
        args = utils.get_args(message)
        logger.debug(args)
        if len(args) == 0:
            await utils.answer(message, self.strings["need_spam"])
            return
        if len(args) == 1:
            if message.is_reply:
                use_reply = True
            else:
                await utils.answer(message, self.strings["spam_urself"])
                return
        count = args[0]
        spam = (await message.get_reply_message()) if use_reply else message
        spam.message = " ".join(args[1:])
        try:
            count = int(count)
        except ValueError:
            await utils.answer(message, self.strings["nice_number"])
            return
        if count < 1:
            await utils.answer(message, self.strings["much_spam"])
            return
        await message.delete()
        if count > 100:
            # Be kind to other people
            sleepy = 2
        else:
            sleepy = 0
        i = 0
        size = 1 if sleepy else 200
        while i < count:
            await asyncio.gather(*[message.respond(spam) for x in range(min(count, size))])
            await asyncio.sleep(sleepy)
            i += size
        await self.allmodules.log("spam", group=message.to_id, data=spam.message + " (" + str(count) + ")")
