from flask import Flask, render_template, abort, url_for, request, redirect, session, jsonify
import psycopg2
from psycopg2 import sql
import requests
import logging
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Set up logging
logging.basicConfig(level=logging.DEBUG, filename='app.log', filemode='a',
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Database connection details
DB_HOST = '40.114.250.29'
DB_PORT = '5432'
DB_NAME = 'postgres'
DB_USER = 'teammember1'
DB_PASSWORD = 'ASDFG'

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
            return {
                "appid": games_data[0],
                "name": games_data[1],
                "release_date": str(games_data[2]),
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
    except psycopg2.Error as e:
        logging.error(f"Database error: {e.pgcode} - {e.pgerror}")
    except Exception as e:
        logging.error(f"Error fetching data from database: {str(e)}")
    return None

@app.route('/autocomplete', methods=['GET'])
def autocomplete():
    term = request.args.get('term', '')
    suggestions = []

    try:
        connection = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = connection.cursor()
        query = """
            SELECT appid, name
            FROM games_data
            WHERE CAST(appid AS TEXT) LIKE %s OR name ILIKE %s
            LIMIT 10;
        """
        cursor.execute(query, (f'%{term}%', f'%{term}%'))
        results = cursor.fetchall()
        cursor.close()
        connection.close()

        suggestions = [{"label": f"{row[1]} (ID: {row[0]})", "value": row[1]} for row in results]
    except Exception as e:
        logging.error(f"Error fetching autocomplete suggestions: {str(e)}")

    return json.dumps(suggestions)



def get_game_data_by_id_or_name(identifier):
    """
    Fetch game data by appid or name from the database.
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

        # Query to search by appid or name
        query = """
        SELECT * FROM games_data
        WHERE CAST(appid AS TEXT) = %s OR LOWER(name) = LOWER(%s);
        """
        cursor.execute(query, (identifier, identifier))
        game_data = cursor.fetchone()
        cursor.close()
        connection.close()
        if game_data:
            return {
                "appid": game_data[0],
                "name": game_data[1],
                "release_date": str(game_data[2]),
                "developer": game_data[4] or "No Developer Available",
                "publisher": game_data[5] or "No Publisher Available",
                "platforms": {
                    "windows": 'windows' in (game_data[6] or '').lower(),
                    "mac": 'mac' in (game_data[6] or '').lower(),
                    "linux": 'linux' in (game_data[6] or '').lower()
                },
                "required_age": game_data[7] or "N/A",
                "categories": game_data[8].split(';') if game_data[8] else [],
                "genres": game_data[9].split(';') if game_data[9] else [],
                "steamspy_tags": game_data[10].split(';') if game_data[10] else [],
                "achievements": game_data[11] or "N/A",
                "positive_ratings": game_data[12] or "N/A",
                "negative_ratings": game_data[13] or "N/A",
                "average_playtime": game_data[14] or "N/A",
                "median_playtime": game_data[15] or "N/A",
                "owners": game_data[16] or "N/A",
                "price": game_data[17] or "N/A"
            }

    except Exception as e:
        logging.error(f"Error fetching data: {str(e)}")
        return None

@app.route('/search_suggestions', methods=['GET'])
def search_suggestions():
    """
    Fetch search suggestions for appid or game name.
    """
    term = request.args.get('term', '').lower()
    suggestions = []
    try:
        connection = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = connection.cursor()

        # Query to fetch matching appids or names
        query = """
        SELECT appid, name FROM games_data
        WHERE CAST(appid AS TEXT) LIKE %s OR LOWER(name) LIKE %s
        LIMIT 10;
        """
        cursor.execute(query, (f"%{term}%", f"%{term}%"))
        results = cursor.fetchall()
        cursor.close()
        connection.close()
        suggestions = [{"appid": row[0], "name": row[1]} for row in results]
    except Exception as e:
        logging.error(f"Error fetching suggestions: {str(e)}")
    return jsonify(suggestions)

def get_user_credentials():
    """
    Fetch user credentials from the user_credentials table in the Azure PostgreSQL database.
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
        query = "SELECT username, password FROM user_credentials"
        cursor.execute(query)
        user_credentials = cursor.fetchall()
        cursor.close()
        connection.close()
        return {username: password for username, password in user_credentials}
    except psycopg2.Error as e:
        logging.error(f"Database error: {e.pgcode} - {e.pgerror}")
    except Exception as e:
        logging.error(f"Error fetching user credentials: {str(e)}")
    return {}




def get_friends_list():
    """
    Fetch friends list from the local friends_data.json file.
    """
    try:
        with open('friends_data.json', 'r') as file:
            friends_data = json.load(file)
            return friends_data.get('friends', [])
    except Exception as e:
        logging.error(f"Error reading friends data from JSON file: {str(e)}")
    return []

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        identifier = request.form.get('search_input')
        api_key = request.form.get('api_key')

        if not identifier or not api_key:
            return render_template('home.html', error="Both App ID/Game Name and API Key are required.")

        game_data = get_game_data_by_id_or_name(identifier)
        if game_data:
            return redirect(url_for('profile', appid=game_data['appid']))
        else:
            return render_template('home.html', error="Game not found. Please check the input.")

    return render_template('home.html')

@app.route('/profile', methods=['GET'])
def profile():
    appid = request.args.get('appid')

    if not appid:
        abort(400, description="App ID is required.")

    game_data = get_game_data_by_id_or_name(appid)
    if game_data:
        return render_template('profile.html', user_profile=game_data)
    else:
        abort(404, description="Game not found.")

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

@app.route('/login_page', methods=['GET', 'POST'])
def login_page():
    user_credentials = get_user_credentials()
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username in user_credentials and user_credentials[username] == password:
            session['logged_in'] = True
            session['username'] = username
            if username == 'Igris_x':
                return redirect(url_for('user_Igris_x'))
            elif username == 'fufucela':
                return redirect(url_for('user_fufucela'))
            elif username == 'achie':
                return redirect(url_for('user_achie'))
            elif username == 'addybaddy':
                return redirect(url_for('user_addybaddy'))
            elif username == 'morid':
                return redirect(url_for('user_morid'))
        else:
            error_message = "Invalid username or password."
            return render_template('login_page.html', error=error_message)
    return render_template('login_page.html')

@app.route('/user_Igris_x', methods=['GET'])
def user_Igris_x():
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('login_page'))

    user_id = 1
    purchased_games = []

    try:
        connection = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = connection.cursor()
        query = "SELECT * FROM purchased_games WHERE user_id = %s"
        cursor.execute(query, (user_id,))
        purchased_games = cursor.fetchall()
        cursor.close()
        connection.close()
    except psycopg2.Error as e:
        logging.error(f"Database error: {e.pgcode} - {e.pgerror}")
    except Exception as e:
        logging.error(f"Error fetching purchased games: {str(e)}")

    return render_template('user_Igris_x.html', purchased_games=purchased_games)

@app.route('/user_fufucela', methods=['GET'])
def user_fufucela():
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('login_page'))

    user_id = 1
    purchased_games = []

    try:
        connection = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = connection.cursor()
        query = "SELECT * FROM purchased_games WHERE user_id = %s"
        cursor.execute(query, (user_id,))
        purchased_games = cursor.fetchall()
        cursor.close()
        connection.close()
    except psycopg2.Error as e:
        logging.error(f"Database error: {e.pgcode} - {e.pgerror}")
    except Exception as e:
        logging.error(f"Error fetching purchased games: {str(e)}")

    return render_template('user_fufucela.html', purchased_games=purchased_games)

@app.route('/user_achie', methods=['GET'])
def user_achie():
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('login_page'))
    return render_template('user_achie.html')

@app.route('/user_addybaddy', methods=['GET'])
def user_addybaddy():
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('login_page'))
    return render_template('user_addybaddy.html')

@app.route('/user_morid', methods=['GET'])
def user_morid():
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('login_page'))
    return render_template('user_morid.html')

@app.route('/friends_list', methods=['GET'])
def friends_list():
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('login_page'))
    friends = get_friends_list()
    return render_template('friends_list.html', friends=friends)

@app.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return redirect(url_for('home'))

@app.route('/bought_games', methods=['GET'])
def bought_games():
    fixed_game_ids = [825930, 1178150, 20200, 1097880, 1659180]
    bought_games = []

    try:
        connection = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = connection.cursor()

        # Fetch the games with fixed app IDs
        query = "SELECT appid, name, price FROM games_data WHERE appid = ANY(%s)"
        cursor.execute(query, (fixed_game_ids,))
        results = cursor.fetchall()
        for result in results:
            bought_games.append({
                "appid": result[0],
                "name": result[1],
                "price": f"${result[2]:.2f}" if result[2] else "Free"
            })

        cursor.close()
        connection.close()
    except psycopg2.Error as e:
        logging.error(f"Database error: {e.pgcode} - {e.pgerror}")
    except Exception as e:
        logging.error(f"Error fetching bought games: {str(e)}")

    return render_template('bought_games.html', bought_games=bought_games)
def get_friends_list():
    """
    Fetch friends list from the local friends_data.json file.
    """
    try:
        with open('friends_data.json', 'r') as file:
            friends_data = json.load(file)
            return friends_data  # List of friends directly from JSON
    except Exception as e:
        logging.error(f"Error reading friends data from JSON file: {str(e)}")
    return []

@app.route('/most_played_games', methods=['GET'])
def most_played_games():
    try:
        connection = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = connection.cursor()
        query = """
        SELECT appid, name
        FROM games_data
        ORDER BY average_playtime DESC
        LIMIT 10;
        """
        cursor.execute(query)
        games = cursor.fetchall()
        cursor.close()
        connection.close()

        most_played_games = [{"appid": game[0], "name": game[1]} for game in games]
        return render_template('most_played_games.html', most_played_games=most_played_games)
    except Exception as e:
        logging.error(f"Error fetching most played games: {str(e)}")
        abort(500)


@app.route('/profile_redirect', methods=['GET'])
def profile_redirect():
    if 'logged_in' not in session:
        return redirect(url_for('login_page'))
    if session['username'] == 'Igris_x':
        return redirect(url_for('user_Igris_x'))
    elif session['username'] == 'fufucela':
        return redirect(url_for('user_fufucela'))
    elif session['username'] == 'achie':
        return redirect(url_for('user_achie'))
    elif session['username'] == 'addybaddy':
        return redirect(url_for('user_addybaddy'))
    elif session['username'] == 'mourid':
        return redirect(url_for('user_morid'))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
