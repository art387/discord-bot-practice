from discord.ext import tasks, commands
import os
import subprocess
from google_drive_downloader import GoogleDriveDownloader as gdd
import urllib.parse as urlparse
from urllib.parse import parse_qs

from utils import tools


class FileDownloader(commands.Cog):
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
            subprocess.Popen(args, shell=False).wait()
            await ctx.send("Download Success")
        except Exception as e:
            print(e)
            await ctx.send("Download Failed.")

    @commands.command()
    async def video(self, ctx, url):
        try:
            args = self.dir_lib + "/youtube-dl.exe " \
                                  "-o " + self.dir_download + '/%(title)s-%(id)s.%(ext)s' + ' ' + url
            subprocess.Popen(args, shell=False).wait()
            await ctx.send("Download Success")
        except Exception as e:
            print(e)
            await ctx.send("Download Failed.")

    # TODO: Fix the google drive downloader
    # @commands.command()
    # async def dl_google(self, ctx, url):
    #     parsed_url = urlparse.urlparse(url)
    #     file_id_gooogle = parse_qs(parsed_url.query)['id'][0]
    #     gdd.download_file_from_google_drive(file_id=file_id_gooogle, dest_path='F:\\nana.zip', unzip=True)


def setup(bot):
    bot.add_cog(FileDownloader(bot))
