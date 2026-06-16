from telebot.async_telebot import AsyncTeleBot
import telebot.types as tbt
from telebot import apihelper
import asyncio

import websockets as webs
import json

import botconfig as bc
bc.BotConfig()

if bc.BotConfig.cfg.PROXY:
    apihelper.proxy = {'http': bc.BotConfig.cfg.PROXY, 'https': bc.BotConfig.cfg.PROXY}

class TgNotifierBot(AsyncTeleBot):
    def __init__(self, internal_api: str):
        self.api = internal_api
        super().__init__(bc.BotConfig.cfg.TG_TOKEN)
        self.message_handler(func=lambda msg: not msg.sender_chat == None,
                             content_types=["animation", "audio", "document", "photo", "sticker", "video", "voice", "video_note", "poll", "text"]
                             )(self.msg_pwgood)
        
    async def send_ws_msg(self, msg: dict):
        async with webs.connect(self.api) as ws:
            await ws.send(json.dumps({"client": "tg-not", "token": bc.BotConfig.cfg.IAPI_TOKEN}))
            await ws.send(json.dumps(msg))
            await ws.recv()

    async def msg_pwgood(self, msg: tbt.Message):
        if not msg.sender_chat.type == "channel" or not (str(msg.sender_chat.id) == "-1002030266560"): return
        text = ''
        if msg.text: text += msg.text
        if msg.caption: text += msg.caption
        await self.send_message("1130674897", text)
        await self.send_ws_msg({"text": text})

bot = TgNotifierBot(bc.BotConfig.cfg.INTERNAL_API)
asyncio.run(bot.infinity_polling(skip_pending=True))