#by https://github.com/AstonishingBoy
from telethon import events
from datetime import datetime
from uniborg.util import admin_cmd
from time import sleep


@borg.on(admin_cmd("ping"))
async def _(event):
	"""модуль написан украинцем/Слава Україні!"""
    if event.fwd_from:
        return
    start = datetime.now()
    await event.edit("Ждём ответа от сервера...")
    end = datetime.now()
    ms = (end - start).microseconds / 1000
    sleep(0.1)
    await event.edit("**Pong {}ms!**".format(ms))