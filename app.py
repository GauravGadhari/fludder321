from flask import Flask, request, jsonify
from ytmusicapi import YTMusic
from flask_cors import CORS  # Import CORS

# Initialize YTMusic with authentication headers
ytmusic = YTMusic('headers_auth.json')

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Generic function to handle API responses
def handle_response(api_function, *args, **kwargs):
    try:
        response = api_function(*args, **kwargs)
        if response:
            return jsonify(response), 200
        else:
            return jsonify({'message': 'No data found.'}), 404
    except Exception as e:
        print(f'Error: {e}')
        return jsonify({'message': 'Internal server error.'}), 500

@app.route('/search', methods=['POST'])
def search():
    data = request.get_json()
    return handle_response(
        ytmusic.search,
        data.get('query', ''),
        data.get('filter', ''),
        scope=data.get('scope', None),
        limit=data.get('limit', 10),
        ignore_spelling=data.get('ignoreSpelling', True)
    )

@app.route('/suggestions', methods=['POST'])
def suggestions():
    data = request.get_json()
    return handle_response(
        ytmusic.get_search_suggestions,
        data.get('query', ''),
        data.get('detailed_runs', False)
    )

@app.route('/home', methods=['POST'])
def home():
    data = request.get_json()
    return handle_response(ytmusic.get_home, limit=data.get('limit', 3))

@app.route('/artist', methods=['POST'])
def artist():
    data = request.get_json()
    return handle_response(ytmusic.get_artist, data.get('channelId', ''))

@app.route('/artist_albums', methods=['POST'])
def artist_albums():
    data = request.get_json()
    return handle_response(
        ytmusic.get_artist_albums,
        data.get('channelId', ''),
        data.get('params', ''),
        limit=data.get('limit', 100),
        order=data.get('order', None)
    )

@app.route('/album', methods=['POST'])
def album():
    data = request.get_json()
    return handle_response(ytmusic.get_album, data.get('browseId', ''))

@app.route('/album_browse_id', methods=['POST'])
def album_browse_id():
    data = request.get_json()
    return handle_response(ytmusic.get_album_browse_id, data.get('audioPlaylistId', ''))

@app.route('/user', methods=['POST'])
def user():
    data = request.get_json()
    return handle_response(ytmusic.get_user, data.get('channelId', ''))

@app.route('/song_related', methods=['POST'])
def song_related():
    data = request.get_json()
    return handle_response(ytmusic.get_song_related, data.get('browseId', ''))

@app.route('/lyrics', methods=['POST'])
def lyrics():
    data = request.get_json()
    return handle_response(ytmusic.get_lyrics, data.get('browseId', ''))

@app.route('/tasteprofile', methods=['GET'])
def tasteprofile():
    return handle_response(ytmusic.get_tasteprofile)

@app.route('/mood_categories', methods=['GET'])
def mood_categories():
    return handle_response(ytmusic.get_mood_categories)

@app.route('/mood_playlists', methods=['POST'])
def mood_playlists():
    data = request.get_json()
    return handle_response(ytmusic.get_mood_playlists, data.get('params', ''))

if __name__ == '__main__':
    app.run(debug=True)
