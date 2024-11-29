# Team FaaaM,
# Opdracht: Steam
# Bronen: W3school, more to come.

from flask import Flask, render_template, abort, url_for, request, redirect




import psycopg2
from psycopg2 import sql
import requests
import json

app = Flask(__name__)

# Database connection details
DB_HOST = '40.114.250.29'
DB_PORT = '5432'
DB_NAME = 'steamdb'
DB_USER = 'teammember1'
DB_PASSWORD = 'ASDFG'

# Load the friends data from JSON file
with open('friends_data.json', 'r') as file:
    friends_data = json.load(file)

def get_json_api(api, *keys):
    """
    Fetch data from an API and navigate through nested keys.
    """
    response = requests.get(api)
    if response.status_code == 200:
        api_json_data = response.json()
        result = api_json_data
        for key in keys:
            result = result.get(key, {})
        return result
    return None

def steam_game_info(gameid, api_key):
    """
    Fetch information about a specific Steam game.
    """
    api_url = f"https://store.steampowered.com/api/appdetails?appids={gameid}&key={api_key}"
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()
    return None

def get_game_data_from_db(appid):
    """
    Fetch game data from the Azure PostgreSQL database.
    """
    try:
        connection = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = connection.cursor()
        query = sql.SQL("SELECT * FROM games_data WHERE appid = %s")
        cursor.execute(query, (appid,))
        games_data = cursor.fetchone()
        cursor.close()
        connection.close()
        if games_data:
            # Correctly map each value to its corresponding column
            return {
                "appid": games_data[0],
                "name": games_data[1],
                "release_date": str(games_data[2]),  # Convert to string for template
                "english": games_data[3],
                "developer": games_data[4] if games_data[4] else "No Developer Available",
                "publisher": games_data[5] if games_data[5] else "No Publisher Available",
                "platforms": {
                    "windows": 'windows' in (games_data[6] or '').lower(),
                    "mac": 'mac' in (games_data[6] or '').lower(),
                    "linux": 'linux' in (games_data[6] or '').lower()
                },
                "required_age": games_data[7] if games_data[7] else "N/A",
                "categories": games_data[8].split(';') if games_data[8] else [],
                "genres": games_data[9].split(';') if games_data[9] else [],
                "steamspy_tags": games_data[10].split(';') if games_data[10] else [],
                "achievements": games_data[11] if games_data[11] is not None else "N/A",
                "positive_ratings": games_data[12] if games_data[12] is not None else "N/A",
                "negative_ratings": games_data[13] if games_data[13] is not None else "N/A",
                "average_playtime": games_data[14] if games_data[14] else "N/A",
                "median_playtime": games_data[15] if games_data[15] else "N/A",
                "owners": games_data[16] if games_data[16] else "N/A",
                "price": str(games_data[17]) if games_data[17] is not None else "N/A"
            }
    except Exception as e:
        print(f"Error fetching data from database: {e}")
    return None





@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        appid = request.form.get('appid')
        api_key = request.form.get('api_key')
        if appid and api_key:
            return redirect(url_for('profile', appid=appid, api_key=api_key))
        return render_template('home.html', error="App ID and API Key are required.")
    return render_template('home.html', friends=friends_data)

@app.route('/profile', methods=['GET'])
def profile():
    appid = request.args.get('appid')
    api_key = request.args.get('api_key')

    if not appid or not api_key:
        abort(400)

    user_profile = get_game_data_from_db(appid)
    if user_profile:
        return render_template('profile.html', user_profile=user_profile)
    else:
        api_profile = steam_game_info(appid, api_key)
        if api_profile and str(appid) in api_profile and api_profile[str(appid)]["success"]:
            return render_template('profile.html', user_profile=api_profile[str(appid)]["data"])
    abort(404)

@app.route('/game/<int:appid>', methods=['GET'])
def game_details(appid):
    games_data = get_game_data_from_db(appid)
    if games_data:
        return render_template('game.html', game={appid: {"data": games_data}})
    else:
        abort(404)

@app.route('/stats', methods=['GET'])
def stats():
    return render_template('stats.html')

@app.route('/owned_games', methods=['GET'])
def owned_games():
    games_list = [
            {"appid": 12345, "game_info": {"gameName": "Game 1"}},
        {"appid": 67890, "game_info": {"gameName": "Game 2"}},
    ]
    return render_template('owned_games.html', game_name=games_list)

@app.route('/friends_list', methods=['GET'])
def friends_list():
    return render_template('friends_list.html', friends=friends_data)

if __name__ == '__main__':
    app.run(debug=True)
