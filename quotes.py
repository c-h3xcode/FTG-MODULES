#Changed by https://github.com/AstonishingBoy
#Requires: Pillow

import logging
from .. import loader, utils
import telethon
import requests, io, PIL
from telethon.tl.types import (MessageEntityBold, MessageEntityItalic,
							   MessageEntityMention, MessageEntityTextUrl,
							   MessageEntityCode, MessageEntityMentionName,
							   MessageEntityHashtag, MessageEntityCashtag,
							   MessageEntityBotCommand, MessageEntityUrl,
							   MessageEntityStrike, MessageEntityUnderline,
							   MessageEntityPhone, ChannelParticipantsAdmins,
							   ChannelParticipantCreator, ChannelParticipantAdmin, User)
							
logger = logging.getLogger(__name__)


@loader.tds
class QuotesMod(loader.Module):
	"""Цитата из сообщения"""
	"""тут был украинец/Слава Україні!"""
	strings = {
	    "name": "Quotes",
	    "processing": "<b>Обработка...</b>",
	    "processing_api": "<b>О б р а б о т к а . . .</b>",
	    "no_reply": "<b>Нет реплая</b>",
	    "mediaType_photo": "Фотография",
        "mediaType_video": "Видео",
        "mediaType_videomessage": "Видеосообщение",
        "mediaType_voice": "Голосовое сообщение",
        "mediaType_audio": "Аудио",
        "mediaType_poll": "Голосование",
        "mediaType_quiz": "Викторина",
        "mediaType_location": "Геолокация",
        "mediaType_gif": "GIF",
        "mediaType_sticker": "Стикер",
        "mediaType_file": "Файл: ",
        "diceType_dice": "Кубик", 
        "diceType_dart": "Дартс",
        "ball_thrown": "Бросок мяча",
        "dart_thrown": "Бросок дротика",
        "dart_almostthere": "близко к цели!",
        "dart_missed": "мимо!",
        "dart_bullseye": "в яблочко!"
	}

	async def client_ready(self, client, db):
		self.client = client

	@loader.unrestricted
	@loader.ratelimit
	async def qcmd(self, message):
		args = utils.get_args(message)
		reply = await message.get_reply_message()
		if not reply:
			await utils.answer(message, self.strings('no_reply', message))
			return
		await utils.answer(message, self.strings('processing', message))
		
			
		if not args or not args[0].isdigit():
			count = 1
		else:
			count = int(args[0].strip()) +1
		byfile = False
		if "file" in args:
			byfile = True
		msgs = []
		cur = reply.id
		cyr = cur + count
		while cur != cyr:
			msg = await message.client.get_messages(message.to_id, ids=cur)
			if msg:
				msgs.append(msg)
			cur += 1
			
		messages = []
		avatars = {}
		for reply in msgs:
			text = reply.raw_text
			entities = parse_entities(reply)
			if reply.fwd_from:
				id = reply.fwd_from.from_id or reply.fwd_from.channel_id
				if not id:
					id = 1234567890
					name = reply.fwd_from.from_name
					pfp = None
				else:
					sender = await message.client.get_entity(id)
					name = telethon.utils.get_display_name(sender)
					pfp = avatars.get(id, None)
					if not pfp:
						pfp = await message.client.download_profile_photo(id, bytes)
						if pfp:
							pfp = 'https://telegra.ph'+requests.post('https://telegra.ph/upload', files={'file': ('file', pfp, None)}).json()[0]['src']
							avatars[id] = pfp
			else:
				id = reply.from_id
				sender = await message.client.get_entity(id)
				name = telethon.utils.get_display_name(sender)
				pfp = avatars.get(id, None)
				if not pfp:
					pfp = await message.client.download_profile_photo(id, bytes)
					if pfp:
						pfp = 'https://telegra.ph'+requests.post('https://telegra.ph/upload', files={'file': ('file', pfp, None)}).json()[0]['src']
						avatars[id] = pfp
			
			image = await check_media(message, reply)
			
			rreply = await reply.get_reply_message()
			if rreply:
				rtext = rreply.raw_text
				if rreply.media:
				    rtext = await get_media_caption(rreply)
				rsender = rreply.sender
				rname = telethon.utils.get_display_name(rsender)
				rreply = {'author': rname, 'text': rtext}
				
			admintitle = ""
			if message.chat:
				admins = await message.client.get_participants(message.to_id, filter=ChannelParticipantsAdmins)
				if reply.sender in admins:
					admin = admins[admins.index(reply.sender)].participant
					if not admin:
					    admintitle = " "
					else:
					    admintitle = admin.rank
					if not admintitle:
						if type(admin) == ChannelParticipantCreator:
							admintitle = "creator" 
						else:
							admintitle = "admin"
			messages.append({
					"text": text,
					"picture": image,
					"reply": rreply,
					"entities": entities,
					"author": {
							"id": id,
							"name": name,
							"adminTitle": admintitle,
							"picture": pfp
								}
							})
					
			
		data = {"messages": messages,
						"maxWidth": 550,
						"scaleFactor": 5,
						"squareAvatar": False,
						"textColor": "white",
						"replyLineColor": "white",
						"adminTitleColor": "#969ba0",
						"messageBorderRadius": 10,
						"pictureBorderRadius": 8,
						"backgroundColor": "#162330"
						}
		await utils.answer(message, self.strings('processing_api', message))
		r = requests.post("https://mishase.me/quote", json=data)
		output = r.content
		out = io.BytesIO()
		if not byfile:
			out.name = "quote.webp"
			im = PIL.Image.open(io.BytesIO(output))
			im.thumbnail((512, 512))
			im.save(out, "WEBP")
		else:
			out.write(output)
			out.name = "quote.png"
		out.seek(0)
		await message.client.send_file(message.to_id, out, force_document=byfile, reply_to=await message.get_reply_message())
		await message.delete()


async def get_media_caption(reply_message):
    if reply_message and reply_message.media:
        if reply_message.photo:
            return QuotesMod.strings["mediaType_photo"]
        dice = False
        try:
            dice = True if reply_message.dice else False
        except AttributeError:
            try:
                dice = True if type(reply_message.media) == telethon.tl.types.MessageMediaDice else False
            except AttributeError:
                pass
        if dice:
            dice_type = ""
            dice_text = reply_message.media.value
            if reply_message.media.emoticon == "🎲":
                dice_type = QuotesMod.strings["diceType_dice"]
                return "{} {}: {}".format(reply_message.media.emoticon,
                                                      dice_type,
                                                      dice_text)
            elif reply_message.media.emoticon == "🎯":
               if dice_text == 1:
                   dice_text = QuotesMod.strings["dart_missed"]
               elif dice_text == 5:
                   dice_text = QuotesMod.strings["dart_almostthere"]
               elif dice_text == 6:
                   dice_text = QuotesMod.strings["dart_bullseye"]
               else:
                    return "{} {}".format(reply_message.media.emoticon,
                                                      QuotesMod.strings["dart_thrown"])
               dice_type = QuotesMod.strings["diceType_dart"]
               return "{} {}: {}".format(reply_message.media.emoticon,
                                                     dice_type,
                                                     dice_text)
            elif reply_message.media.emoticon == "🏀":
                return "{} {}".format(reply_message.media.emoticon,
                                                  QuotesMod.strings["ball_thrown"])
            else:
                 return "Unsupported dice type ({}): {}"\
                    .format(reply_message.media.emoticon,
                            reply_message.media.value)
        elif reply_message.poll:
            try:
                if reply_message.media.poll.quiz is True:
                    return QuotesMod.strings["mediaType_quiz"]
            except Exception:
                pass
            return QuotesMod.strings["mediaType_poll"]
        elif reply_message.geo:
             return QuotesMod.strings["mediaType_location"]
        elif reply_message.document:
            if reply_message.gif :
                return QuotesMod.strings["mediaType_gif"]
            elif reply_message.video:
                if reply_message.video.attributes[0].round_message:
                    return QuotesMod.strings["mediaType_videomessage"]
                else:
                    return QuotesMod.strings["mediaType_video"]
            elif reply_message.audio:
                return QuotesMod.strings["mediaType_audio"]
            elif reply_message.voice:
                return QuotesMod.strings["mediaType_voice"]
            elif reply_message.file:
                if reply_message.file.mime_type == "application/x-tgsticker":
                        emoji = ""
                        try:
                            emoji = reply_message.media.document.attributes[0].alt
                        except AttributeError:
                            try:
                                emoji = reply_message.media.document.attributes[1].alt
                            except AttributeError:
                                emoji = ""
                        caption = "{} {}".format(emoji, QuotesMod.strings["mediaType_sticker"]) if emoji != "" else QuotesMod.strings["mediaType_sticker"]
                        return caption
                else:
                    if reply_message.sticker:
                        emoji = ""
                        try:
                            emoji = reply_message.file.emoji
                            logger.debug(len(emoji))
                        except TypeError:
                            emoji = ""
                        caption = "{} {}".format(emoji, QuotesMod.strings["mediaType_sticker"]) if emoji != "" else QuotesMod.strings["mediaType_sticker"]
                        return caption
                    else:
                        return QuotesMod.strings["mediaType_file"] + reply_message.media.document.attributes[-1].file_name
        else:
            return ""
    else:
        return ""
   
    return ""

def parse_entities(reply):
	entities = []
	if not reply.entities:
		return []
	for entity in reply.entities:
		entity_type = type(entity)
		start = entity.offset
		end = entity.length
		if entity_type is MessageEntityBold:
			etype = 'bold'
		elif entity_type is MessageEntityItalic:
			etype = 'italic'
		elif entity_type in [MessageEntityUrl, MessageEntityPhone]:
			etype = 'url'
		elif entity_type is MessageEntityCode:
			etype = 'monospace'
		elif entity_type is MessageEntityStrike:
			etype = 'strikethrough'
		elif entity_type is MessageEntityUnderline:
			etype = 'underline'
		elif entity_type in [MessageEntityMention, MessageEntityTextUrl,
							 MessageEntityMentionName, MessageEntityHashtag,
							 MessageEntityCashtag, MessageEntityBotCommand]:
			etype = 'bluetext'
		entities.append({'type': etype, 'offset': start, 'length': end})
	return entities
	

async def check_media(message, reply):
	if reply and reply.media:
		if reply.photo:
			data = reply.photo
		elif reply.document:
			if reply.gif or reply.video or reply.audio or reply.voice:
				return None
			data = reply.media.document
		else:
			return None
	else:
		return None
	if not data or data is None:
		return None
	else:
		data = await message.client.download_file(data, bytes)
		img = io.BytesIO()
		img.name = "img.png"
		try:
			PIL.Image.open(io.BytesIO(data)).save(img, "PNG")
			link = 'https://telegra.ph'+requests.post('https://telegra.ph/upload', files={'file': ('file', img.getvalue(), "image/png")}).json()[0]['src']
			return link
		except:
			return None
		
