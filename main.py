from tabulate import tabulate
import discord, asyncio, time
from discord.ext import tasks, commands
from todoist import TodoistAPI
from apscheduler.schedulers.blocking import BlockingScheduler

from app import app_downloader, app_tool, app_todoist
import database_config as cfg
import logging


async def do_logging():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger('discord')
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
    handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
    logger.addHandler(handler)


client = discord.Client()
current_task = []
bot = commands.Bot(command_prefix='!')


@bot.command()
async def ping(ctx):
    await ctx.send('pong')


def update_log(message):
    try:
        with open("bot_log.txt", "a") as f:
            f.write(f"Time: {int(time.time())}, Author: {message.author} Messages: {message.content}\n")
    except Exception as e:
        print(e)


@client.event
async def on_message(message):
    if message.author.id != cfg.YOUR_DISCORD_USER_ID and message.author.id != cfg.YOUR_CLIENT_BOT_ID:
        print("Boo someone is hacking")
        return
    else:
        update_log(message)

    if message.content.find("asu") != -1:
        await message.channel.send("asu")  # If the user says !hello we will send back hi

    if message.content.startswith("!audio-dl"):
        client_app = client_downloader
        client_app.getAudio(app_tool.get_url_from_message(message))
        await message.channel.send('Download is complete O.o')

    if message.content.startswith("!video-dl"):
        client_app = client_downloader
        client_app.getVideo(app_tool.get_url_from_message(message))
        await message.channel.send('Download is complete o.O')

    if message.content.startswith("!todo all"):
        client_app = client_todoist
        tasks_list = client_app.getAllTask()
        await message.channel.send(
            "\n".join(["{}. {}".format(i + 1, task['content']) for i, task in enumerate(tasks_list)]))

    if message.content.startswith("!todo today"):
        client_app = client_todoist
        tasks_list = client_app.getTodayTask()
        await message.channel.send('Here is your uncompleted schedule for today, <@%s>!' % cfg.YOUR_DISCORD_USER_ID)
        table = list()
        for i, task in enumerate(tasks_list):
            table.append([i + 1, task['content']])
        print(tabulate(table, headers=["No", "Task"]))
        await message.channel.send(tabulate(table, headers=["No", "Task"]))

    if message.content.startswith("!todo future"):
        client_app = client_todoist
        tasks_list = client_app.getFutureTask()
        await message.channel.send(
            "\n".join(["{}. {}".format(i + 1, task['content']) for i, task in enumerate(tasks_list)]))

    if message.content.startswith("!todo do"):
        id_content = message.content[2]
        client_app = client_todoist
        response = client_app.setTaskComplete(id_content)
        await message.channel.send(response + '\n')
        tasks_list = client_app.getTodayTask()
        await message.channel.send(
            "\n".join(["{}. {}".format(i + 1, task['content']) for i, task in enumerate(tasks_list)]))


# @tasks.loop(seconds=10)
# async def scheduler_job():
#     await client.wait_until_ready()
#     ch = client.get_channel(672511716646584324)
#     client_app = client_todoist
#     client_app.resync_todoist()
#     tasks_list = client_app.getTodayTask()
#     await ch.send(
#         "\n".join(["{}. {}".format(i + 1, task['content']) for i, task in enumerate(tasks_list)]))
#

# scheduler
# scheduler = BlockingScheduler()
bot.run(cfg.YOUR_DISCORD_TOKEN)
client_todoist = app_todoist.todoist_app(cfg.YOUR_TODOIST_TOKEN, current_task)
client_downloader = app_downloader.AppUtil()
client.run(cfg.YOUR_DISCORD_TOKEN)
