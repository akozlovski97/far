import logging

from .. import loader, utils

logger = logging.getLogger(__name__)


@loader.tds
class NotesMod(loader.Module):
    """Хранит глобальные заметки"""
    strings = {"name": "NotesMod",
               "what_note": "<b>Какую записку вы хотите увидеть?</b>\n\n<b>📍Посмотреть их можно написав:</b>\n<code>.notes</code>",
               "no_note": "<b>Заметка не найдена!</b>",
               "save_what": "<b>Вы должны ответить на сообщение, чтобы сохранить его в заметке, или ввести заметку!</b>",
               "what_name": "<b>Вы должны указать, как должна называться заметка!</b>",
               "saved": "<b>Заметка сохранена</b>",
               "notes_header": "<b>Сохраненные заметки:</b>\n\n",
               "notes_item": "<b>•</b> <code>{}</code>",
               "delnote_args": "<b>Какую заметку следует удалить?</b>",
               "delnote_done": "<b>Заметка удалена!</b>",
               "delnotes_none": "<b>Нет заметок для очистки!</b>",
               "delnotes_done": "<b>Все заметки очищены!</b>",
               "notes_none": "<b>Нет сохраненных заметок!</b>"}

    async def notecmd(self, message):
        """Показывает указанную заметку"""
        args = utils.get_args(message)
        if not args:
            await utils.answer(message, self.strings("what_note", message))
            return
        asset_id = self._db.get(__name__, "notes", {}).get(args[0], None)
        logger.debug(asset_id)
        if asset_id is not None:
            asset = await self._db.fetch_asset(asset_id)
        else:
            asset = None
        if asset is None:
            self.del_note(args[0])
            await utils.answer(message, self.strings("no_note", message))
            return

        await utils.answer(message, await self._db.fetch_asset(asset_id))

    async def delallnotescmd(self, message):
        """Удаляет все сохраненные заметки"""
        if not self._db.get(__name__, "notes", {}):
            await utils.answer(message, self.strings("delnotes_none", message))
            return
        self._db.get(__name__, "notes", {}).clear()
        await utils.answer(message, self.strings("delnotes_done", message))

    async def savecmd(self, message):
        """Сохраните новую заметку. Чтобы сохранить напиши "(реплай на код) .save" """
        args = utils.get_args(message)
        if not args:
            await utils.answer(message, self.strings("what_name", message))
            return
        if not message.is_reply:
            if len(args) < 2:
                await utils.answer(message, self.strings("save_what", message))
                return
            else:
                message.entities = None
                message.message = args[1]
                target = message
                logger.debug(target.message)
        else:
            target = await message.get_reply_message()
        asset_id = await self._db.store_asset(target)
        self._db.set(__name__, "notes", {**self._db.get(__name__, "notes", {}), args[0]: asset_id})
        await utils.answer(message, self.strings("saved", message))
    async def delnotecmd(self, message):
        """Удаляет заметку, указанная по имени"""
        args = utils.get_args(message)
        if not args:
            await utils.answer(message, self.strings("delnote_args", message))
        self.del_note(args[0])
        await utils.answer(message, self.strings("delnote_done", message))
    def del_note(self, note):
        old = self._db.get(__name__, "notes", {})
        try:
            del old[note]
        except KeyError:
            pass
        else:
            self._db.set(__name__, "notes", old)
    async def notescmd(self, message):
        """Список сохраненных заметок"""
        if not self._db.get(__name__, "notes", {}):
            await utils.answer(message, self.strings("notes_none", message))
            return
        await utils.answer(message, self.strings("notes_header", message)
                           + "\n".join(self.strings("notes_item", message).format(key)
                           for key in self._db.get(__name__, "notes", {})))

    async def client_ready(self, client, db):
        self._db = db
