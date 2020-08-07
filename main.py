from flask import Flask, json

from dbus.mainloop.glib import DBusGMainLoop
from mpris2 import get_players_uri, Player

import config

DBusGMainLoop(set_as_default=True)

playing_state = {}

api = Flask(__name__)

# Route for Ping endpoint
@api.route('/ping', methods=['GET'])
def get_ping():
    return "Pong"

# Route for playing endpoint
@api.route('/playing_state', methods=['GET'])
def get_playing_state():
    try:
        # Get MPRIS client
        for player in get_players_uri():
            # If the config specifies to ignore Chrome MPRIS
            if config.IGNORE_CHROME_MPRIS:
                # If the first MPRIS client is a Chrome instance
                if player.startswith('org.mpris.MediaPlayer2.chrome'):
                    continue

            # Set the MPRIS uri to the active element
            uri = player
            break

        # Initialize player with URI
        player = Player(dbus_interface_info={'dbus_uri': uri}) # pylint: disable=unexpected-keyword-arg
    except:
        return json.dumps(playing_state), 504

    # Add URI to playing_state
    playing_state["uri"] = uri

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
                playing_state[end_var] = playing_state[end_var].replace('open.spotify.com', 'o.scdn.co')
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

    # Return a stringified JSON object
    return json.dumps(playing_state)

# Initialize API on host 0.0.0.0 and port 5175
# If you want to debug using Flask, edit the config file
if __name__ == '__main__':
    api.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)
