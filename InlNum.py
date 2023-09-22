from .. import utils, loader
from fuzzywuzzy import fuzz

@loader.tds
class InlNumMod(loader.Module):
    """Узнай под каким числом находится кнопка"""
    strings = {"name": "INumMod"}

    async def client_ready(self, client, db):
        self.db = db
        self.client = client

    async def inlcmd(self, message):
        """Использовать: .inl (текст)"""
        args = utils.get_args_raw(message)
        if not args:
            await message.edit("Укажите текст после команды, например: <b>.inl (текст)</b>")
            return

        text_to_find = args.strip().lower()
        button_number = 0
        reply = await message.get_reply_message()

        if reply and reply.reply_markup:
            for i, row in enumerate(reply.reply_markup.rows):
                for j, button in enumerate(row.buttons):
                    button_text = button.text.lower()
                    similarity_ratio = fuzz.ratio(text_to_find, button_text)
                    button_number += 1

                    if text_to_find in button_text or similarity_ratio > 80:
                        await message.edit(f"<b>'{button_text}'</b> находится на <b>{button_number}</b> кнопке")
                        return

        await message.edit(f"Кнопка с текстом <b>'{text_to_find}'</b> не найдена!")
