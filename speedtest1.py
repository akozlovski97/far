import logging
import speedtest

from .. import loader, utils

logger = logging.getLogger(__name__)

@loader.tds
class SpeedtestMod(loader.Module):
    """Данные взяты с speedtest.net"""
    strings = {"name": "SpeedtestMod",
               "running": "<b>Запускаю Speedtest...</b>",
               "results": "<b>Результат Speedtest:</b>",
               "results_download": "<b>📥Скачивание:</b> <code>{}</code> <b>MiB/s</b>",
               "results_upload": "<b>📤Загрузка:</b> <code>{}</code> <b>MiB/s</b>",
               "results_ping": "<b>⏱Ping:</b> <code>{}</code> <b>ms</b>"}

    async def speedtestcmd(self, message):
        """Показывает скорость твоего интернета"""
        await utils.answer(message, self.strings("running", message))
        args = utils.get_args(message)
        servers = []
        for server in args:
            try:
                servers += [int(server)]
            except ValueError:
                logger.warning("Сервер не отвечает")
        results = await utils.run_sync(self.speedtest, servers)
        ret = self.strings("results", message) + "\n\n"
        ret += self.strings("results_download", message).format(round(results["download"] / 2**20, 2)) + "\n"
        ret += self.strings("results_upload", message).format(round(results["upload"] / 2**20, 2)) + "\n"
        ret += self.strings("results_ping", message).format(round(results["ping"], 2)) + "\n"
        await utils.answer(message, ret)

    def speedtest(self, servers):
        speedtester = speedtest.Speedtest()
        speedtester.get_servers(servers)
        speedtester.get_best_server()
        speedtester.download(threads=None)
        speedtester.upload(threads=None)
        return speedtester.results.dict()
