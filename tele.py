from http import client
from telethon import TelegramClient
import asyncio

## Run the following 2 lines if using Google Colab
import nest_asyncio

nest_asyncio.apply()

api_id = "24801927"
api_hash = "41186a49f8b96a0ac566cf3c349d2506"
session_name = "session1"
bot_token = "7546011083:AAGnh8t0x1YbG1kVPzRGrNnS2LRaGEuDn6Y"
## must be your channel or have authorization to post
channel_invite_link = "t.me/VCC_final_project"


async def func(img_path, client):
    entity = await client.get_entity(channel_invite_link)
    # Send an image follow by a text.
    await client.send_file(entity, img_path)
    await client.send_message(entity=entity, message=img_path.split("/")[-1])


async def send_image(img_path):
    # connection
    async with TelegramClient(session_name, api_id, api_hash).start(bot_token=bot_token) as client:
        await func(img_path, client)
