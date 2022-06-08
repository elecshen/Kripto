from datetime import timedelta

# pip install python-decouple
import decouple

# pip install telethon
from telethon.sync import TelegramClient
from telethon.tl import functions
from telethon.tl.types import *
# from telethon.tl.functions.upload import GetFileRequest

import asyncio

from .models import Sources, Patterns
from django.templatetags.static import static


def parse_patterns(days=1):
    session_path = static('config_files/Patterns.session')
    # env_config = decouple.Config(decouple.RepositoryEnv(static('config_files/env.env')))
    api_id = 11417482 # env_config.get('api_id')
    api_hash = 'f140971234c7e898d08f2d7d5e7eb223' # env_config.get('api_hash')

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    with TelegramClient('D:\\source\\pythonProjects\\patterns\\Patterns', api_id, api_hash, loop=loop) as client:
        # Get chat by chat id
        chat_obj = client(functions.channels.GetChannelsRequest(id=[1706211720]))
        group = chat_obj.chats[0]

        last_article = Patterns.objects.all().last().datetime

        # Parse messages
        for message in client.iter_messages(group):
            # Parse from now to yesterday
            if message.date < last_article + timedelta(minutes=5):
                break
            # Skip ads message
            if message.reply_markup is not None or message.message.find('https://t.me/') > 0:
                continue

            # Create an url object in the database or set the default
            url = Sources.objects.get(type="noImg", url="#")
            if message.media is not None:
                if isinstance(message.media, MessageMediaWebPage):
                    url, cond = Sources.objects.get_or_create(type="img", url=message.media.webpage.url)
                # message.download_media(file="static/img/article_" + date.strftime('%Y.%m.%d %H-%M-%S') + '.jpg')

            # Insert formatting tags
            text = message.message
            for entity in reversed(message.entities):
                if isinstance(entity, MessageEntityBold):
                    text = text[:(entity.offset + entity.length)] + '</b>' + text[(entity.offset + entity.length):]
                    text = text[:entity.offset] + '<b>' + text[entity.offset:]
                elif isinstance(entity, MessageEntityItalic):
                    text = text[:(entity.offset + entity.length)] + '</i>' + text[(entity.offset + entity.length):]
                    text = text[:entity.offset] + '<i>' + text[entity.offset:]
            text = text.replace('\u200b', '')
            text = text.replace('\n', '<br>')
            title = "noTitle"
            if 0 < text.find("</b>") < 200:
                title = text[:text.find("</b>") + 4]
                text = text[text.find("</b>")+4:]
            title = title.replace('<br>', '')
            title = title.replace('.', '. ')
            title = title.replace('.  ', '. ')

            patt = Patterns(datetime=message.date, title=title, content=text)
            patt.save()
            patt.imgSource.add(url)
            patt.save()
