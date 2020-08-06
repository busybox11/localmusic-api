import config

from flask import Flask, json

from dbus.mainloop.glib import DBusGMainLoop
from mpris2 import get_players_uri
from mpris2 import Player

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
	# Get MPRIS client
	for player in get_players_uri():
		# If the config specifies to ignore Chrome MPRIS
		if config.ignore_chrome_mpris == True:
			# If the first MPRIS client is a Chrome instance
			if player.startswith('org.mpris.MediaPlayer2.chrome'):
				continue

		# Set the MPRIS uri to the active element
		uri = player
		break

	# Initialize player with URI
	player = Player(dbus_interface_info={'dbus_uri': uri})

	# Mandatory fields declaration
	playing_state["title"] = str(player.Metadata[player.Metadata.TITLE])
	playing_state["artist"] = str(player.Metadata[player.Metadata.ARTIST][0])
	playing_state["album"] = str(player.Metadata[player.Metadata.ALBUM])

	# Try to add all additional fields to the playing_state object
	additional_endpoints = ["ART_URI", "LENGTH"]
	add_end_var = ["artwork", "length"]
	for endpoint in additional_endpoints:
		end_var = add_end_var[additional_endpoints.index(endpoint)]
		try:
			playing_state[end_var] = str(player.Metadata[getattr(player.Metadata, endpoint)])

			# Workaround to get working Spotify covers URL
			if endpoint == "ART_URI" and "open.spotify.com" in str(playing_state[end_var]):
				playing_state[end_var] = playing_state[end_var].replace('open.spotify.com', 'o.scdn.co')
		except:
			pass
	
	# Try to add song position to the playing_state object
	try:
		if str(player.Position) != "0":
			playing_state["position"] = str(player.Position)
	except:
		pass

	# Return a stringified JSON object
	return json.dumps(playing_state)

# Initialize API on host 0.0.0.0 and port 5175
# If you want to debug using Flask, just append debug=true to the list of arguments
if __name__ == '__main__':
	api.run(host='0.0.0.0', port=5175)
