## spotiphile

### Introduction

Spotiphile is a package to download MP3 music from Spotify (via YouTube) and add proper ID3 tag data. It is inspired by [spotify_dl](https://github.com/SathyaBhat/spotify-dl).

### Installation

    python setup.py install

### Usage

```
from spotiphile import Spotiphile

sp = Spotiphile(YOUTUBE_DEV_KEY)
sp.get("https://open.spotify.com/track/7BKLCZ1jbUBVqRi2FVlTVw")
```

If you're downloading a track and don't want to depend on search results from YouTube (which may be inaccurate), you can explicitly specify the YouTube URL for the track using `yt_url` keyword argument :

    sp.get("https://open.spotify.com/track/7BKLCZ1jbUBVqRi2FVlTVw", yt_url="https://www.youtube.com/watch?v=zQEfHMPEO6w")

You can also specify the output file to create using `out` keyword argument :

    sp.get("https://open.spotify.com/track/7BKLCZ1jbUBVqRi2FVlTVw", out="/path/to/file")

The `out` argument string can also contains special keywords which are automatically substituted -

```
{album} : Name of the album
{artist} : Name of performing artist
{title} : Title of the track
```
**Note :** _Extensions if given are ignored in favor of `.mp3`_

**Warning: ** _Make sure that out has {title} for filename when downloading albums otherwise every song will have same name and overwrite previously downloaded song._


### Command Line Tool (Linux)

`setup.py` adds `bin/spotiphile` to your $PATH which is implementation of spotiphile package and comes with argument parsing (Check `spotiphile --help` for more).

To make the command line tool work without manually providing YouTube URL (-y option), you need to add a config file with a valid YouTube Developer Key with search API enabled.

Open `$XDG_CONFIG_HOME/spotiphile/.config` and add the following:

```
[YOUTUBE]
DEV_KEY = YOUR_KEY_HERE
```

### TO-DO
* Logging
* Exception handling
* Documentation
* Playlist support
