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
      "canPause": true,
      "canPlay": true,
      "canSeek": true
    }
  ],
  "length": "198693000",
  "position": "45371000",
  "platform": "Linux",
  "status": "Playing",
  "title": "Apologize",
  "uri": "org.mpris.MediaPlayer2.spotify"
}
```
**Notice**: All elements are optional, **except** the `uri`, `platform` and `config`.

All time elements are microseconds strings. 

If there is no MPRIS players available, the API will return a `504 GATEWAY TIMEOUT` with a blank JSON.

## Control endpoints
All control endpoints have the following response:

**On success**: `HTTP CODE 201` with JSON `{"success": true}`.

**On error**: `HTTP CODE 502` with JSON `{"success": false}`.

### `POST /control/next`, no request body
Go to the next song.

### `POST /control/previous`, no request body
Go back the previous song.

### `POST /control/play`, no request body
Play / resume the previous song.

### `POST /control/pause`, no request body
Pause the previous song.

### `POST /control/playpause`, no request body
Play / resume or pause the previous song, based on the current playback state.

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
