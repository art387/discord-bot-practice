import os
import database_config as cfg
from discord.ext import tasks, commands

print('Engine is starting...')

bot = commands.Bot(command_prefix='.', description='initiating bot')


@bot.command()
async def ping(ctx):
    await ctx.send('pong')


for file in os.listdir("cogs"):
    if file.endswith(".py"):
        name = file[:-3]
        bot.load_extension(f"cogs.{name}")


bot.run(cfg.YOUR_DISCORD_TOKEN)
