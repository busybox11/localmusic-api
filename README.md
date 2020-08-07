# localmusic-api
A Python3 Flask REST API to retrieve currently playing local music 

## Dependencies
```
python3
subprocess
Flask
dbus
mpris2
```

## How to use?
Clone the repo, install all the python dependencies using `pip3`, and launch the server using `python3 main.py`.
It only works with Linux (dbus' MPRIS) for now, but a Win32 compatibility is to come.

The webserver will now be available at the local address (e.g. `localhost`, `127.0.0.1`) with the port `5175` by default.

## Endpoints
### `GET /ping`
Pong

### `GET /playing_state`
Returns a JSON element similar to this one:
```JSON
{
  "album": "a modern tragedy vol. 2",
  "artist": "grandson",
  "artwork": "https://i.scdn.co/image/ab67616d00001e0298561ed4bf6615bfc788bfcc",
  "config": [
    {
      "canPause": "1",
      "canPlay": "1",
      "canSeek": "1"
    }
  ],
  "length": "198693000",
  "position": "3435000",
  "status": "Playing",
  "title": "Apologize",
  "uri": "org.mpris.MediaPlayer2.spotify"
}
```
**Notice**: All **track-related** elements except `album`, `artist`, `title` and `uri` are optional, **except** if the player is blank, then the API will only return the URI.
The **config** element is always present.

All time elements are strings and in microseconds. 

If there is no MPRIS players available, the API will return a `504 GATEWAY TIMEOUT` with a blank JSON. (`{}`)

## Config
Currently, all the config is stored in `config.py`. You can edit this file to meet your needs.

### `IGNORE_CHROME_MPRIS`
**Boolean**, default: `True`

Ignore Chrome MPRIS player.

### `HOST`
**String**, default: `127.0.0.1`

The host domain / IP of the API.

### `PORT`
**Integer**, default: `5175`

The port of the API.

### `DEBUG`
**Boolean**, default: `True`

Enable debug mode on Flask.
