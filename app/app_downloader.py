import os
import subprocess
import database_config as cfg
import app


class AppUtil:

    def __init__(self):
        self.dir_path = os.getcwd()
        self.dir_lib = os.path.join(self.dir_path, 'lib', 'youtube-dl')
        self.dir_download = app.app_tool.get_download_path()

    def getAudio(self, url):
        # FNULL = open(os.devnull, 'w')  # use this if you want to suppress output to stdout from the subprocess
        args = self.dir_lib + "/youtube-dl.exe -f bestaudio --extract-audio --audio-quality 0 --audio-format mp3 " \
                         "-o " + self.dir_download + '/%(title)s-%(id)s.%(ext)s' + ' ' + url

        # subprocess.call(args, stdout=FNULL, stderr=FNULL, shell=False)
        subprocess.Popen(args, shell=False)

    def getVideo(self, url):
        # FNULL = open(os.devnull, 'w')  # use this if you want to suppress output to stdout from the subprocess
        args = self.dir_lib + "/youtube-dl.exe " \
                         "-o " + self.dir_download + '/%(title)s-%(id)s.%(ext)s' + ' ' + url
        subprocess.Popen(args, shell=False)
