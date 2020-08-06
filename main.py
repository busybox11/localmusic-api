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
	# Initialize player to last MPRIS client
	uri = next(get_players_uri())
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
