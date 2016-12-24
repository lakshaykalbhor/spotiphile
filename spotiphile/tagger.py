import mutagen
import requests
from mutagen.mp3 import MP3, HeaderNotFoundError
from mutagen.id3 import TIT2, TALB, TPE1, APIC, TRCK, TCON, TDRC, ID3, USLT


class Tagger:

    def __init__(self, metadata):
        self.metadata = metadata

    def tag(self):
        metadata = self.metadata
        filename = "{}.mp3".format(metadata['out_file'])
        try:
            audio = MP3(filename)
        except HeaderNotFoundError:
            print("Header not found...")
            audio = mutagen.File(filename)
            audio.add_tags()
        audio["TIT2"] = TIT2(encoding=3, text=metadata['title'])
        audio["TALB"] = TALB(encoding=3, text=metadata['album'])
        audio["TPE1"] = TPE1(encoding=3, text=metadata['artists'])
        audio["TCON"] = TCON(encoding=3, text=metadata['genre'])
        audio["TDRC"] = TDRC(encoding=3, text=metadata['year'])
        audio["TRCK"] = TRCK(encoding=3, text=str(metadata['track_no']))
        audio.tags.add(
            APIC(
                encoding=3,
                mime='image/png',
                type=3,
                desc=u'Cover',
                data=requests.get(metadata['cover']).content
            )
        )
        audio.save(filename)

        ''' Using ID3 and USLT to add lyrics '''
        
        audio = ID3(filename)
        uslt_output = USLT(encoding=3, lang=u'eng', desc=u'desc', text=metadata['lyrics'])
        audio["USLT::'eng'"] = uslt_output
        audio.save(filename)
