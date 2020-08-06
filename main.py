from flask import Flask, json

from dbus.mainloop.glib import DBusGMainLoop
from mpris2 import get_players_uri
from mpris2 import Player

DBusGMainLoop(set_as_default=True)

playing_state = {}

api = Flask(__name__)

@api.route('/ping', methods=['GET'])
def get_ping():
	return "Pong"

@api.route('/playing_state', methods=['GET'])
def get_playing_state():
	uri = next(get_players_uri())
	player = Player(dbus_interface_info={'dbus_uri': "org.mpris.MediaPlayer2.spotify"})

	playing_state["title"] = str(player.Metadata[player.Metadata.TITLE])
	playing_state["artist"] = str(player.Metadata[player.Metadata.ARTIST][0])
	playing_state["album"] = str(player.Metadata[player.Metadata.ALBUM])

	additional_endpoints = ["ART_URI", "LENGTH"]
	add_end_var = ["artwork", "length"]
	for endpoint in additional_endpoints:
		end_var = add_end_var[additional_endpoints.index(endpoint)]
		try:
			playing_state[end_var] = str(player.Metadata[getattr(player.Metadata, endpoint)])
			if endpoint == "ART_URI" and "open.spotify.com" in str(playing_state[end_var]):
				playing_state[end_var] = playing_state[end_var].replace('open.spotify.com', 'o.scdn.co')
		except:
			pass
	
	try:
		playing_state["position"] = str(player.Position)
	except:
		pass

	return json.dumps(playing_state)

if __name__ == '__main__':
	api.run(host='0.0.0.0', port=5175)
