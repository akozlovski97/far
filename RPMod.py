from .. import loader, utils
import io
import json
from telethon.tl.types import Message


@loader.tds
class RPMod(loader.Module):
    """Добавит RP в чат"""

    strings = {
        "name": "RPMod",
        "args": "🤯 <b>Неправильные аргументы!</b>",
        "success": "👌 <b>Успех!</b>",
        "rp_on": "🟢 <b>RPMod Включен</b>",
        "rp_off": "🔴 <b>RPMod Выключен</b>",
        "rplist": "🟠 <b>Лист RP команд</b>\n\n{}",
        "backup_caption": "⚫️ <b>Мои команды РП. Восстановить с помощью </b><code>.rprestore</code>",
        "no_file": "⚫️ <b>Реплай на файл</b>",
        "restored": "⚫️ <b>RP команды восстановлены. Увидеть их </b><code>.rplist</code>",
    }

    async def client_ready(self, client, db):
        self._db = db
        self._client = client
        self.rp = db.get("RPMod", "rp", {})
        self.chats = db.get("RPMod", "active", [])

    async def rpcmd(self, message: Message) -> None:
        """.rp (команда) (сообщение) - Добавить RP команду. Оставь пустным чтобы удалить RP команду!"""
        args = utils.get_args_raw(message)
        try:
            command = args.split(" ", 1)[0]
            msg = args.split(" ", 1)[1]
        except Exception:
            if not args or command not in self.rp:
                await utils.answer(message, self.strings("args", message))
            else:
                del self.rp[command]
                self._db.set("RPMod", "rp", self.rp)
                await utils.answer(message, self.strings("success", message))
            return
        self.rp[command] = msg
        self._db.set("RPMod", "rp", self.rp)
        await utils.answer(message, self.strings("success", message))

    async def rptogglecmd(self, message: Message) -> None:
        """Триггерит на команды в чате"""
        cid = str(utils.get_chat_id(message))
        if cid in self.chats:
            self.chats.remove(cid)
            await utils.answer(message, self.strings("rp_off", message))
        else:
            self.chats.append(cid)
            await utils.answer(message, self.strings("rp_on", message))
        self._db.set("RPMod", "active", self.chats)

    @loader.unrestricted
    async def rplistcmd(self, message: Message) -> None:
        """Лист RP команд"""
        await utils.answer(
            message,
            self.strings("rplist").format(
                "\n".join(
                    [f" 🔴  {command} - {msg}" for command, msg in self.rp.items()]
                )
            ),
        )

    async def rpbackupcmd(self, message: Message) -> None:
        """Бэкап RP команд в файл"""
        file = io.BytesIO(json.dumps(self.rp).encode("utf-8"))
        file.name = "rp-backup.json"
        await self._client.send_file(
            utils.get_chat_id(message), file, caption=self.strings("backup_caption")
        )
        await message.delete()

    async def rprestorecmd(self, message: Message) -> None:
        """Восстановить RP команды из файла"""
        reply = await message.get_reply_message()
        if not reply or not reply.media:
            await utils.answer(message, self.strings("no_file"))
            return

        file = (await self._client.download_file(reply.media)).decode("utf-8")
        self.rp = json.loads(file)
        self._db.set("RPMod", "rp", self.rp)
        await utils.answer(message, self.strings("restored"))

    async def rpchatscmd(self, message: Message) -> None:
        """Список чатов, в которых активен RPMod"""
        res = f"🟠 <b>RPMod активен в {len(self.chats)} чатах:</b>\n\n"
        for chat in self.chats:
            chat_obj = await self._client.get_entity(int(chat))
            if getattr(chat_obj, "title", False):
                chat_name = chat_obj.title
            else:
                chat_name = chat_obj.first_name

            res += f"    🇯🇵 {chat_name}" + "\n"

        await utils.answer(message, res)

    async def watcher(self, message: Message) -> None:
        try:
            cid = str(utils.get_chat_id(message))
            if cid not in self.chats:
                return

            if message.text.split(" ", 1)[0].lower() not in self.rp:
                return

            cmd = message.text.split(" ", 1)[0].lower()
            msg = self.rp[cmd]

            entity = None
            try:
                entity = await self._client.get_entity(message.text.split(" ", 2)[1])
            except Exception:
                pass

            reply = await message.get_reply_message()

            try:
                reply = await self._client.get_entity(reply.sender_id)
            except Exception:
                pass

            if not reply and not entity:
                return

            if reply and entity or not reply:
                reply = entity

            sender = await self._client.get_entity(message.sender_id)

            await utils.answer(
                message,
                f'<a href="tg://user?id={sender.id}">{sender.first_name}</a> <b>{msg}</b> <a href="tg://user?id={reply.id}">{reply.first_name}</a>',
            )
        except Exception:
            return
