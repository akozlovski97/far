# -*- coding: utf-8 -*-

import asyncio
import logging
import os
import re

import telethon

from .. import loader, utils

logger = logging.getLogger(__name__)


@loader.tds
class TerminalMod(loader.Module):
    """Эмулятор терминала в телеграме"""

    strings = {
        "name": "TerminalMod",
        "flood_wait_protect_cfg_doc": "Сколько ждать в секундах между правками в командах",
        "what_to_kill": "<b>Нужно ответить на команду терминала, чтобы завершить ее❗️</b>",
        "kill_fail": "<b>Не удалось завершить процесс❗️</b>",
        "killed": "<b>✅ Завершен!</b>",
        "no_cmd": "<b>В этом сообщении не выполняется ни одна команда❗️</b>",
        "running": "<b>📋Команда:</b> <code>{}</code>",
        "finished": "\n<b>🏷Код:</b> <code>{}</code>",
        "stdout": "\n<b>📝Выполнение:</b>\n<code>",
        "stderr": "</code>\n\n<b>⚠️Ошибка:</b>\n<code>",
        "end": "</code>",
        "auth_fail": "<b>Ошибка авторизации, попробуйте еще раз❗️</b>",
        "auth_needed": '<a href="tg://user?id={}">Требуется интерактивная аутентификация❗️</a>',
        "auth_msg": (
            "<b>Измените это сообщение на пароль для</b> "
            "<code>{}</code> <b>запуска</b> <code>{}</code>"
        ),
        "auth_locked": "<b>Ошибка аутентификации, повторите попытку позже❗️</b>",
        "auth_ongoing": "<b>Аутентификация...</b>",
        "done": "<b>✅ Выполнено</b>",
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            "FLOOD_WAIT_PROTECT",
            2,
            lambda m: self.strings("flood_wait_protect_cfg_doc", m),
        )
        self.activecmds = {}

    @loader.owner
    async def terminalcmd(self, message):
        """.terminal (команда)"""
        await self.run_command(message, utils.get_args_raw(message))

    @loader.owner
    async def aptcmd(self, message):
        """Сокращение для .terminal apt"""
        await self.run_command(
            message,
            ("apt " if os.geteuid() == 0 else "sudo -S apt ")
            + utils.get_args_raw(message)
            + " -y",
            RawMessageEditor(
                message,
                "apt " + utils.get_args_raw(message),
                self.config,
                self.strings,
                message,
                True,
            ),
        )

    async def run_command(self, message, cmd, editor=None):
        if len(cmd.split(" ")) > 1 and cmd.split(" ")[0] == "sudo":
            needsswitch = True
            for word in cmd.split(" ", 1)[1].split(" "):
                if word[0] != "-":
                    break
                if word == "-S":
                    needsswitch = False
            if needsswitch:
                cmd = " ".join([cmd.split(" ", 1)[0], "-S", cmd.split(" ", 1)[1]])
        sproc = await asyncio.create_subprocess_shell(
            cmd,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=utils.get_base_dir(),
        )
        if editor is None:
            editor = SudoMessageEditor(message, cmd, self.config, self.strings, message)
        editor.update_process(sproc)
        self.activecmds[hash_msg(message)] = sproc
        await editor.redraw()
        await asyncio.gather(
            read_stream(
                editor.update_stdout, sproc.stdout, self.config["FLOOD_WAIT_PROTECT"]
            ),
            read_stream(
                editor.update_stderr, sproc.stderr, self.config["FLOOD_WAIT_PROTECT"]
            ),
        )
        await editor.cmd_ended(await sproc.wait())
        del self.activecmds[hash_msg(message)]

    @loader.owner
    async def terminatecmd(self, message):
        """Используйте в ответе, чтобы остановить процесс"""
        if not message.is_reply:
            await utils.answer(message, self.strings("what_to_kill", message))
            return
        if hash_msg(await message.get_reply_message()) in self.activecmds:
            try:
                self.activecmds[hash_msg(await message.get_reply_message())].terminate()
            except Exception:
                logger.exception("Завершение процесса не удалось")
                await utils.answer(message, self.strings("kill_fail", message))
            else:
                await utils.answer(message, self.strings("killed", message))
        else:
            await utils.answer(message, self.strings("no_cmd", message))

    @loader.owner
    async def killcmd(self, message):
        """Используйте реплай, чтобы остановить процесс"""
        if not message.is_reply:
            await utils.answer(message, self.strings("what_to_kill", message))
            return
        if hash_msg(await message.get_reply_message()) in self.activecmds:
            try:
                self.activecmds[hash_msg(await message.get_reply_message())].kill()
            except Exception:
                logger.exception("Killing process failed")
                await utils.answer(message, self.strings("kill_fail", message))
            else:
                await utils.answer(message, self.strings("killed", message))
        else:
            await utils.answer(message, self.strings("no_cmd", message))

    async def neofetchcmd(self, message):
        """Показать системную статистику через neofetch"""
        await self.run_command(
            message,
            "neofetch --stdout",
            RawMessageEditor(
                message, "neofetch --stdout", self.config, self.strings, message
            ),
        )

    async def uptimecmd(self, message):
        """Показать время безотказной работы системы"""
        await self.run_command(
            message,
            "uptime",
            RawMessageEditor(message, "uptime", self.config, self.strings, message),
        )


def hash_msg(message):
    return str(utils.get_chat_id(message)) + "/" + str(message.id)


async def read_stream(func, stream, delay):
    last_task = None
    data = b""
    while True:
        dat = await stream.read(1)
        if not dat:
            # EOF
            if last_task:
                # Send all pending data
                last_task.cancel()
                await func(data.decode("utf-8"))
            # If there is no last task there is inherently no data, so theres no point sending a blank string
            break
        data += dat
        if last_task:
            last_task.cancel()
        last_task = asyncio.ensure_future(sleep_for_task(func, data, delay))


async def sleep_for_task(func, data, delay):
    await asyncio.sleep(delay)
    await func(data.decode("utf-8"))


class MessageEditor:
    def __init__(self, message, command, config, strings, request_message):
        self.message = [message]
        self.command = command
        self.stdout = ""
        self.stderr = ""
        self.rc = None
        self.redraws = 0
        self.config = config
        self.strings = strings
        self.request_message = request_message

    async def update_stdout(self, stdout):
        self.stdout = stdout
        await self.redraw()

    async def update_stderr(self, stderr):
        self.stderr = stderr
        await self.redraw()

    async def redraw(self):
        text = self.strings("running", self.request_message).format(
            utils.escape_html(self.command)
        )
        if self.rc is not None:
            text += self.strings("finished", self.request_message).format(
                utils.escape_html(str(self.rc))
            )
        text += self.strings("stdout", self.request_message)
        text += utils.escape_html(self.stdout[max(len(self.stdout) - 2048, 0) :])
        text += self.strings("stderr", self.request_message)
        text += utils.escape_html(self.stderr[max(len(self.stderr) - 1024, 0) :])
        text += self.strings("end", self.request_message)
        try:
            self.message = await utils.answer(self.message, text)
        except telethon.errors.rpcerrorlist.MessageNotModifiedError:
            pass
        except telethon.errors.rpcerrorlist.MessageTooLongError as e:
            logger.error(e)
            logger.error(text)

    # The message is never empty due to the template header

    async def cmd_ended(self, rc):
        self.rc = rc
        self.state = 4
        await self.redraw()

    def update_process(self, process):
        pass


class SudoMessageEditor(MessageEditor):
    # Let's just hope these are safe to parse
    PASS_REQ = "[sudo] password for"
    WRONG_PASS = r"\[sudo\] password for (.*): Sorry, try again\."
    TOO_MANY_TRIES = (
        r"\[sudo\] password for (.*): sudo: [0-9]+ incorrect password attempts"
    )

    def __init__(self, message, command, config, strings, request_message):
        super().__init__(message, command, config, strings, request_message)
        self.process = None
        self.state = 0
        self.authmsg = None

    def update_process(self, process):
        logger.debug("got sproc obj %s", process)
        self.process = process

    async def update_stderr(self, stderr):
        logger.debug("stderr update " + stderr)
        self.stderr = stderr
        lines = stderr.strip().split("\n")
        lastline = lines[-1]
        lastlines = lastline.rsplit(" ", 1)
        handled = False
        if (
            len(lines) > 1
            and re.fullmatch(self.WRONG_PASS, lines[-2])
            and lastlines[0] == self.PASS_REQ
            and self.state == 1
        ):
            logger.debug("switching state to 0")
            await self.authmsg.edit(self.strings("auth_failed", self.request_message))
            self.state = 0
            handled = True
            await asyncio.sleep(2)
            await self.authmsg.delete()
        if lastlines[0] == self.PASS_REQ and self.state == 0:
            logger.debug("Success to find sudo log!")
            text = self.strings("auth_needed", self.request_message).format(
                (await self.message[0].client.get_me()).id
            )
            try:
                await utils.answer(self.message, text)
            except telethon.errors.rpcerrorlist.MessageNotModifiedError as e:
                logger.debug(e)
            logger.debug("edited message with link to self")
            command = "<code>" + utils.escape_html(self.command) + "</code>"
            user = utils.escape_html(lastlines[1][:-1])
            self.authmsg = await self.message[0].client.send_message(
                "me",
                self.strings("auth_msg", self.request_message).format(command, user),
            )
            logger.debug("sent message to self")
            self.message[0].client.remove_event_handler(self.on_message_edited)
            self.message[0].client.add_event_handler(
                self.on_message_edited,
                telethon.events.messageedited.MessageEdited(chats=["me"]),
            )
            logger.debug("registered handler")
            handled = True
        if (
            len(lines) > 1
            and re.fullmatch(self.TOO_MANY_TRIES, lastline)
            and self.state in [1, 3, 4]
        ):
            logger.debug("password wrong lots of times")
            await utils.answer(
                self.message, self.strings("auth_locked", self.request_message)
            )
            await self.authmsg.delete()
            self.state = 2
            handled = True
        if not handled:
            logger.debug("Didn't find sudo log.")
            if self.authmsg is not None:
                await self.authmsg[0].delete()
                self.authmsg = None
            self.state = 2
            await self.redraw()
        logger.debug(self.state)

    async def update_stdout(self, stdout):
        self.stdout = stdout
        if self.state != 2:
            self.state = 3  # Means that we got stdout only
        if self.authmsg is not None:
            await self.authmsg.delete()
            self.authmsg = None
        await self.redraw()

    async def on_message_edited(self, message):
        # Message contains sensitive information.
        if self.authmsg is None:
            return
        logger.debug("got message edit update in self " + str(message.id))
        if hash_msg(message) == hash_msg(self.authmsg):
            # The user has provided interactive authentication. Send password to stdin for sudo.
            try:
                self.authmsg = await utils.answer(
                    message, self.strings("auth_ongoing", self.request_message)
                )
            except telethon.errors.rpcerrorlist.MessageNotModifiedError:
                # Try to clear personal info if the edit fails
                await message.delete()
            self.state = 1
            self.process.stdin.write(
                message.message.message.split("\n", 1)[0].encode("utf-8") + b"\n"
            )


class RawMessageEditor(SudoMessageEditor):
    def __init__(
        self, message, command, config, strings, request_message, show_done=False
    ):
        super().__init__(message, command, config, strings, request_message)
        self.show_done = show_done

    async def redraw(self):
        logger.debug(self.rc)
        if self.rc is None:
            text = (
                "<code>"
                + utils.escape_html(self.stdout[max(len(self.stdout) - 4095, 0) :])
                + "</code>"
            )
        elif self.rc == 0:
            text = (
                "<code>"
                + utils.escape_html(self.stdout[max(len(self.stdout) - 4090, 0) :])
                + "</code>"
            )
        else:
            text = (
                "<code>"
                + utils.escape_html(self.stderr[max(len(self.stderr) - 4095, 0) :])
                + "</code>"
            )
        if self.rc is not None and self.show_done:
            text += "\n" + self.strings("done", self.request_message)
        logger.debug(text)
        try:
            await utils.answer(self.message, text)
        except telethon.errors.rpcerrorlist.MessageNotModifiedError:
            pass
        except (telethon.errors.rpcerrorlist.MessageEmptyError, ValueError):
            pass
        except telethon.errors.rpcerrorlist.MessageTooLongError as e:
            logger.error(e)
            logger.error(text)
