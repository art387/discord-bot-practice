import json

import discord
from app import app_downloader, app_tool, app_todoist
import database_config as cfg
import logging

if cfg.is_logging:
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger('discord')
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
    handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
    logger.addHandler(handler)

client = discord.Client()


@client.event
async def on_message(message):
    if message.author.id != cfg.YOUR_USER_ID and message.author.id != cfg.YOUR_CLIENT_BOT_ID:
        print("Boo someone is hacking")
        return

    if message.content.find("asu") != -1:
        await message.channel.send("asu")  # If the user says !hello we will send back hi

    if message.content.startswith("!audio-dl"):
        client_app = app_downloader.AppUtil()
        try:
            client_app.getAudio(app_tool.get_url_from_message(message))
            await message.channel.send('Download is complete O.o')
        except:
            await message.channel.send('Something is wrong')

    if message.content.startswith("!video-dl"):
        client_app = app_downloader.AppUtil()
        try:
            client_app.getVideo(app_tool.get_url_from_message(message))
            await message.channel.send('Download is complete o.O')
        except:
            await message.channel.send('Something is wrong')

    if message.content.startswith("!todo all"):
        client_app = app_todoist.todoist_app()
        try:
            tasks_all = client_app.getAllTask()
            await message.channel.send(
                "\n".join(["{}. {}".format(i, task['content']) for i, task in enumerate(tasks_all)]))
        except:
            await message.channel.send('failed')

    if message.content.startswith("!todo today"):
        client_app = app_todoist.todoist_app()
        tasks_today = client_app.getTodayTask()
        await message.channel.send(
            "\n".join(["{}. {}".format(i, task['content']) for i, task in enumerate(tasks_today)]))

    if message.content.startswith("!todo future"):
        client_app = app_todoist.todoist_app()
        tasks_future = client_app.getFutureTask()
        await message.channel.send(
            "\n".join(["{}. {}".format(i, task['content']) for i, task in enumerate(tasks_future)]))


client.run(cfg.YOUR_DISCORD_TOKEN)
