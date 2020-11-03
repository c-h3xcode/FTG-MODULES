#by https://github.com/AstonishingBoy
from .. import loader, utils
import logging
from requests import get
import io


logger = logging.getLogger(__name__)

def register(cb):
	cb(WebShotMod())


@loader.tds
class WebShotMod(loader.Module):
	"""модуль написан украинцом/Слава Україні!"""
	strings = {"name": "WebShot"}
		
	def __init__(self):
		self.name = self.strings['name']
	
	@loader.sudo
	async def webshotcmd(self, message):
		reply = None
		link = utils.get_args_raw(message)
		if not link:
			reply = await message.get_reply_message()
			if not reply:
				await message.delete()
				return
			link = reply.raw_text
		await message.edit("Screenshoting....")
		await self.client.send_file(message.to_id, caption=f"<b>Webshot for {link}</b>", file=f"https://webshot.deam.io/{link}/?width=1920&height=1080?type=png", reply_to=reply)
		await message.delete()

	async def client_ready(self, client, db):
		self.client = client
