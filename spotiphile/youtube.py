import youtube_dl
from apiclient.discovery import build


class YouTubeHandler:

    def __init__(self, YOUTUBE_DEV_KEY):

        self.YOUTUBE_DEV_KEY = YOUTUBE_DEV_KEY

    def download(self, url, out_file):

        ydl_opts = {
            'format': 'bestaudio/best',
            'extractaudio': True,
            'noplaylist': True,
            'outtmpl': "{0}.%(ext)s".format(out_file),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '320',
            }],
            'logger': YTDLogger()
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

    def find_track(self, metadata):

        # Generate query to search
        if not metadata['explicit']:
            query = "{0} {1} audio".format(
                metadata['title'], metadata['primary_artist']
            )
        else:
            query = "{0} {1} explicit audio".format(
                metadata['title'], metadata['primary_artist']
            )

        YOUTUBE_API_SERVICE_NAME = "youtube"
        YOUTUBE_API_VERSION = "v3"
        youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                        developerKey=self.YOUTUBE_DEV_KEY)
        # TODO : Improve searching further
        search_resp = youtube.search().list(
            q=query, type="video", part="id,snippet", maxResults=10
        ).execute()

        for result in search_resp['items']:
            # TODO : Check if title contains blocked words (construct a list)
            return "https://www.youtube.com/watch?v={}".format(
                result['id']['videoId']
            )


class YTDLogger:

    def debug(self, msg):
        pass

    def warning(self, msg):
        print("[youtube_dl][warning] {}".format(msg))

    def error(self, msg):
        print("[youtube_dl][error] {}".format(msg))
