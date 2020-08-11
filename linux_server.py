#! /usr/bin/python3

from flask import Flask, json, Response

from dbus.mainloop.glib import DBusGMainLoop
from mpris2 import get_players_uri, Player

import platform

import config

uri = None # pylint: disable=invalid-name
player = None # pylint: disable=invalid-name

api_info = {}
playing_state = {}

DBusGMainLoop(set_as_default=True)

api = Flask(__name__)

def api_info_update():
    temp_api_info = {}
    temp_api_info["platform"] = platform.system()
    temp_api_info["version"] = config.VERSION
    temp_api_info["python_version"] = platform.python_version()

    global api_info # pylint: disable=invalid-name
    api_info = temp_api_info
    return api_info

def init_player():
    try:
        # Get MPRIS client
        for client in get_players_uri():
            # If the config specifies to ignore Chrome MPRIS
            if config.IGNORE_CHROME_MPRIS:
                # If the first MPRIS client is a Chrome instance
                if client.startswith('org.mpris.MediaPlayer2.chrome'):
                    continue

            # Set the MPRIS uri to the active element
            global uri # pylint: disable=invalid-name
            uri = client
            break

        # Initialize player with URI
        global player # pylint: disable=invalid-name
        player = Player(dbus_interface_info={'dbus_uri': uri}) # pylint: disable=unexpected-keyword-arg

        # Everything worked, the player has been successfully initialized
        return True
    except:
        e = sys.exc_info()[0]
        # Something went wrong, the player has not been initialized
        # Returns information about the error
        return e

# Route for API info endpoint
@api.route('/api_info', methods=['GET'])
def get_api_info():
    # Return a stringified JSON object from the output of the function
    return Response(json.dumps(api_info_update()), mimetype='application/json')

# Route for Ping endpoint
@api.route('/ping', methods=['GET'])
def get_ping():
    return "Pong"

# Route for playing endpoint
@api.route('/playing_state', methods=['GET'])
def get_playing_state():
    if not init_player(): # If the player cannot be initialized
        return Response(json.dumps(playing_state), mimetype='application/json', status=504)

    # Add URI and platform to playing_state
    playing_state["uri"] = uri
    playing_state["platform"] = "Linux"

    # Try to add all fields to the playing_state object of the Metadata of the player
    endpoints_meta = ["TITLE", "ARTIST", "ALBUM", "ART_URI", "LENGTH"]
    ends_var_meta = ["title", "artist", "album", "artwork", "length"]
    for endpoint in endpoints_meta:
        end_var = ends_var_meta[endpoints_meta.index(endpoint)]
        try:
            if endpoint == "ARTIST":
                playing_state[end_var] = str(player.Metadata[getattr(player.Metadata, endpoint)][0])
                continue

            playing_state[end_var] = str(player.Metadata[getattr(player.Metadata, endpoint)])

            # Workaround to get working Spotify covers URL
            if endpoint == "ART_URI" and "open.spotify.com" in str(playing_state[end_var]):
                playing_state[end_var] = playing_state[end_var].replace('open.spotify.com', 'i.scdn.co')
        except:
            pass

    # Try to add all fields to the playing_state object of the player
    endpoints_player = ["Position", "PlaybackStatus", "Volume"]
    ends_var_player = ["position", "status", "volume"]
    for endpoint in endpoints_player:
        end_var = ends_var_player[endpoints_player.index(endpoint)]
        try:
            if str(player.Position) == "0":
                continue

            playing_state[end_var] = str(getattr(player, endpoint))
        except:
            pass

    # Add all player abilities to the playing_state object
    playing_state["config"] = [{}]
    configs_player = ["CanPause", "CanPlay", "CanSeek"]
    conf_var_player = ["canPause", "canPlay", "canSeek"]
    for config_item in configs_player:
        conf_var = conf_var_player[configs_player.index(config_item)]
        try:
            playing_state["config"][0][conf_var] = bool(getattr(player, config_item))
        except:
            pass

    # Return a stringified JSON object
    return Response(json.dumps(playing_state), mimetype='application/json')

@api.route('/control/next', methods=['POST'])
def next_song():
    init_player()

    try:
        player.Next()

        return Response(json.dumps({"success": True}), mimetype='application/json', status=201)
    except:
        return Response(json.dumps({"success": False}), mimetype='application/json', status=502)

@api.route('/control/previous', methods=['POST'])
def previous_song():
    init_player()

    try:
        player.Previous()

        return Response(json.dumps({"success": True}), mimetype='application/json', status=201)
    except:
        return Response(json.dumps({"success": False}), mimetype='application/json', status=502)

@api.route('/control/play', methods=['POST'])
def resume_song():
    init_player()

    try:
        player.Play()

        return Response(json.dumps({"success": True}), mimetype='application/json', status=201)
    except:
        return Response(json.dumps({"success": False}), mimetype='application/json', status=502)

@api.route('/control/pause', methods=['POST'])
def pause_song():
    init_player()

    try:
        player.Pause()

        return Response(json.dumps({"success": True}), mimetype='application/json', status=201)
    except:
        return Response(json.dumps({"success": False}), mimetype='application/json', status=502)

@api.route('/control/playpause', methods=['POST'])
def playpause_song():
    init_player()

    try:
        player.PlayPause()

        return Response(json.dumps({"success": True}), mimetype='application/json', status=201)
    except:
        return Response(json.dumps({"success": False}), mimetype='application/json', status=502)

# Initialize API on host 0.0.0.0 and port 5175
# If you want to debug using Flask, edit the config file
api.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)
