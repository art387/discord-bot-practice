from discord.ext import tasks, commands
import os
import subprocess
from utils import tools


class YoutubeDownloader(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.dir_path = os.getcwd()
        self.dir_lib = os.path.join(self.dir_path, 'library_tool', 'youtube-dl')
        self.dir_download = tools.get_download_path()

    @commands.command()
    async def audio(self, ctx, url):
        # FNULL = open(os.devnull, 'w')  # use this if you want to suppress output to stdout from the subprocess
        try:
            args = self.dir_lib + "/youtube-dl.exe -f bestaudio --extract-audio --audio-quality 0 --audio-format mp3 " \
                                  "-o " + self.dir_download + '/%(title)s-%(id)s.%(ext)s' + ' ' + url

            # subprocess.call(args, stdout=FNULL, stderr=FNULL, shell=False)
            subprocess.Popen(args, shell=False)
            await ctx.send("Download Success")
        except Exception as e:
            print(e)
            await ctx.send("Download Failed.")

    @commands.command()
    async def video(self, ctx, url):
        try:
            args = self.dir_lib + "/youtube-dl.exe " \
                                  "-o " + self.dir_download + '/%(title)s-%(id)s.%(ext)s' + ' ' + url
            subprocess.Popen(args, shell=False)
            await ctx.send("Download Success")
        except Exception as e:
            print(e)
            await ctx.send("Download Failed.")



def setup(bot):
    bot.add_cog(YoutubeDownloader(bot))
