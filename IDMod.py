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

        user_id = uuser.id
caption = (
        f"<b>ID:</b> <code>{user_id}</code>\n"
    )
return caption

