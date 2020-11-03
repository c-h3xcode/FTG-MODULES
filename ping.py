#by https://github.com/AstonishingBoy
from telethon import events
from datetime import datetime
from uniborg.util import admin_cmd
from time import sleep


@borg.on(admin_cmd("ping"))
async def _(event):
    if event.fwd_from:
        return
    start = datetime.now()
    """модуль написан украинцем/Слава Україні!"""
    await event.edit("Ждём ответа от сервера...")
    end = datetime.now()
    ms = (end - start).microseconds / 1000
    sleep(0.5)
    await event.edit("**Pong {}ms!**".format(ms))
