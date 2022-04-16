import os
from .. import loader, utils
import logging
from telethon.tl.functions.channels import GetFullChannelRequest, GetParticipantsRequest
from telethon.tl.functions.messages import GetHistoryRequest
from telethon.tl.functions.photos import GetUserPhotosRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import (
    MessageActionChannelMigrateFrom,
    ChannelParticipantsAdmins,
    UserStatusOnline,
)

logger = logging.getLogger(__name__)


@loader.tds
class IDMod(loader.Module):
    """Показывает ID человека по реплаю"""

    strings = {"name": "IDMod"}

    async def idcmd(self, message):
        """.id (@id либо реплай)"""
        args = utils.get_args_raw(message)
        reply = await message.get_reply_message()

        await message.edit("<b>Загружаю информацию...</b>")

        try:
            if args:
                user = await message.client.get_entity(
                    args if not args.isdigit() else int(args)
                )
            else:
                user = await message.client.get_entity(reply.sender_id)
        except:
            user = await message.client.get_me()

        user = await message.client(GetFullUserRequest(user.id))
        caption = await get_user_info(user, message)

async def get_user_info(user, message):
    """Подробная информация о пользователе."""
    uuser = user.users[0]
    user = user.full_user
    logger.info(str(user))

    user_id = uuser.id
    first_name = uuser.first_name or "Нету"
    last_name = uuser.last_name or "Нету"
    username = uuser.username or "Нету"
    user_bio = user.about or "Нету"
    common_chat = user.common_chats_count
    is_bot = "Да" if uuser.bot else "Нет"
    restricted = "Да" if uuser.restricted else "Нет"
    verified = "Да" if uuser.verified else "Нет"

caption = (
        f"<b>ИНФОРМАЦИЯ ПРО ПОЛЬЗОВАТЕЛЯ:</b>\n\n"
        f"<b>Имя:</b> {first_name}\n"
        f"<b>Фамилия:</b> {last_name}\n"
        f"<b>Ник:</b> @{username}\n"
        f"<b>ID:</b> <code>{user_id}</code>\n"
        f"<b>Это бот?</b> {is_bot}\n"
        f"<b>Ограниченный?</b> {restricted}\n"
        f"<b>Подтвержденный?</b> {verified}\n\n"
        f"<b>О {first_name}:</b> \n<code>{user_bio}</code>\n\n"
        f"<b>Количество фото в профиле:</b> {user_photos_count}\n"
        f"<b>Общие чаты:</b> {common_chat}\n"
        f'<b>t.me ссылка:</b> <a href="tg://user?id={user_id}">клик</a>'
    )
return caption

