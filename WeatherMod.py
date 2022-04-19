import requests
from .. import loader, utils


@loader.tds
class WeatherMod(loader.Module):
    """Показывает погоду.\n Оставлять (Город) пустым для своего местоположения! """

    strings = {"name": "WeatherMod "}

    async def pwcmd(self, m):
        """Изображение погоды.\n.pw (Город)"""
        args = utils.get_args_raw(m).replace(" ", "%20")
        city = requests.get(
            f"https://wttr.in/{args if args != None else ''}.png?&lang=ru"
        ).content
        await utils.answer(m, city)
        await message.delete()

    async def awcmd(self, m):
        """ASCII-арт погоды.\n.aw (Город)"""
        city = utils.get_args_raw(m).replace(" ", "%20")
        r = requests.get(f"https://wttr.in/{city if city != None else ''}?0?q?T&lang=ru")
        await utils.answer(m, f"<b>Город:</b> <code>{r.text}</code>")

    async def wcmd(self, m):
        """Погода в тексте. \n.w (Город) """
        city = utils.get_args_raw(m).replace(" ", "%20")
        if city:
            r = requests.get("https://wttr.in/" + city + "?format=%l:+%c+%t,+%w+%m")
        else:
            r = requests.get("https://wttr.in/?format=%l:+%c+%t,+%w+%m")

        await utils.answer(m, r.text)
