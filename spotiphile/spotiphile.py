import re
import os
import requests
from .youtube import YouTubeHandler
from .tagger import Tagger
from .exception import InvalidURLError, InvalidFormatError
import json


class Spotiphile:

    def __init__(self, YOUTUBE_DEV_KEY=None):

        self.YOUTUBE_DEV_KEY = YOUTUBE_DEV_KEY

    def get(
        self, url=None, yt_url=None,
        out="Downloads/{artist}/{album}/{title}.mp3"
    ):

        if url is not None:
            self.type, self.id = re.findall(
                "https://open.spotify.com/(\w+)/(\w+)", url
            )[0]
        else:
            raise InvalidURLError("Enter a URL to find a resource")

        # Instantiate a YouTubeHandler object
        yt = YouTubeHandler(self.YOUTUBE_DEV_KEY)

        if self.type == 'track':
            resp = self._request(self.type, self.id)
            metadata = self._generate_track_metadata(resp, out)
            if yt_url is None:
                if self.YOUTUBE_DEV_KEY is None:
                    raise InvalidFormatError(
                        "Automatic search for song requires access \
to YouTube API with search enabled"
                    )
                url = yt.find_track(metadata)
            else:
                url = yt_url
            yt.download(url, metadata['out_file'])
            tagger = Tagger(metadata)
            tagger.tag()

        if self.type == 'album':
            id_queue = [tracks['id'] for tracks in self._request(
                self.type, self.id
            )['tracks']['items']]

            for id in id_queue:
                s = Spotiphile(self.YOUTUBE_DEV_KEY)
                s.get(
                    "https://open.spotify.com/track/{0}".format(id), out=out
                )

    def _request(self, type, id):

        r = requests.get(
            "https://api.spotify.com/v1/{0}s/{1}".format(type, id)
        )
        return json.loads(r.text)

    def _generate_track_metadata(self, track, out):

        # Request remaining data from iTunes using Search API
        payload = {
            'term': re.sub(r'[(].*[)]', "", track['album']['name']).strip(),
            'entity': 'album',
            'media': 'music'
        }
        r = requests.get("https://itunes.apple.com/search", params=payload)
        itunes_track_dict = json.loads(r.text)

        # Extract relevant information from the dictionary
        title = track['name']
        primary_artist = track['artists'][0]['name']
        artists = ', '.join(artist['name'] for artist in track['artists'])
        album = track['album']['name']
        track_no = track['track_number']
        cover = track['album']['images'][0]['url']
        explicit = track['explicit']
        # Extract genre and year from iTunes API and make sure its accurate
        year = ""
        genre = ""
        for result in itunes_track_dict['results']:
            if result['collectionName'].lower() in album.lower():
                year = result['releaseDate'].split('-')[0]
                genre = result['primaryGenreName']
                break
        try:
            out = os.path.abspath(
                    os.path.expanduser((out).format(
                        title=title, artist=primary_artist, album=album)
                    )
            ).split('.')[0]
        except KeyError:
            raise InvalidFormatError("Enter only valid keys in {}")

        return {
            'title': title, 'primary_artist': primary_artist,
            'artists': artists, 'album': album, 'track_no': track_no,
            'cover': cover, 'year': year, 'genre': genre, 'out_file': out,
            'explicit': explicit
        }
