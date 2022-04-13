from .. import loader, utils
import asyncio
import time
from time import sleep
import random

def register(cb):
    cb(PentaMod())
    
@loader.tds
class PentaMod(loader.Module):
    """Показывает ссылку откуда был скачан модуль"""
    strings = {'name': 'PentaMod'}
    
    async def hackcmd(self, message):
        """Показывает ссылку на модуль"""
        perc = 0
        
        while(perc < 100):
            try:
                text = "👮‍ Взлом пентагона в процессе ..." + str(perc) + "%"
                msg.edit(text)
                
                perc += random.randint(1, 3)
                sleep(0.1)
        except:
            return await message.edit("Ошибка, попробуй еще раз")
                
        msg.edit("🟢 Пентагон успешно взломан!")
        sleep(3)
        
        msg.edit("👽 Поиск секретных данных об НЛО ...")
        perc = 0
        
        while(perc < 100):
            try:
                text = "👽 Поиск секретных данных об НЛО ..." + str(perc) + "%"
                msg.edit(text)
                
                perc += random.randint(1, 5)
                sleep(0.15)
        except:
            return await message.edit("Ошибка, попробуй еще раз")
                
        msg.edit("🦖 Найдены данные о существовании динозавров на земле!")
