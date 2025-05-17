from flask import Flask, jsonify
from flask_cors import CORS
import requests
import re

app = Flask(__name__)
CORS(app)

@app.route('/api/character/<name>', methods=['GET'])
def get_character(name):
    api_url = f'https://rickandmortyapi.com/api/character/?name={name}'
    response = requests.get(api_url)

    if response.status_code != 200:
        return jsonify({'error': 'Failed to fetch character'}), 500

    data = response.json()
    results = data.get("results", [])
    if not results:
        return jsonify({'error': 'Character not found'}), 404

    character = results[0]

    # Extract episode IDs
    episode_urls = character.get("episode", [])
    episode_ids = [re.search(r'/(\d+)$', url).group(1) for url in episode_urls]
    batch_url = f"https://rickandmortyapi.com/api/episode/{','.join(episode_ids)}"

    episodes = []
    ep_response = requests.get(batch_url)

    if ep_response.status_code == 200:
        ep_data = ep_response.json()
        if isinstance(ep_data, list):
            episodes = [f"{ep['episode']} - {ep['name']}" for ep in ep_data]
        else:
            # Single episode case
            episodes = [f"{ep_data['episode']} - {ep_data['name']}"]

    return jsonify({
        "name": character["name"],
        "image": character["image"],
        "total_episodes": len(episodes),
        "episodes": episodes
    })

if __name__ == '__main__':
    app.run(debug=True)
