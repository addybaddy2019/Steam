from flask import request, session, redirect, url_for, jsonify, render_template, Flask
from data_utils import data_naar_pandas, sorteer_data
from visualization import linear_regression_price_rating, kwalitatief_frequentie_genres, kwantitatief_frequentie_prijs
from api import info_for_steam_games, user, amount_owned_games, owned_games_info, friends_list_info
import os

app = Flask(__name__, template_folder='templates')
app.secret_key = 'supersecretkey'

@app.route('/', methods=['GET', 'POST'])
def landing_page():
    """
    Function Description:
        Renders the landing page where the user enters their Steam key and ID.
        After logging in, the user is redirected to their profile.
    """
    if request.method == 'POST':
        session['steamid'] = request.form['steamid']
        session['key'] = request.form['key']
        return redirect(url_for('profile'))
    return render_template('landing_page.html')


@app.route('/profile/', methods=['GET', 'POST'])
def profile():
    """
    Function Description:
        Displays the user's Steam profile page.
        The profile includes user details, owned games, and a friends list.
    """
    if request.method == 'POST':
        steamid = request.form['steamid']
        key = request.form['key']
        session['steamid'] = steamid
        session['key'] = key
    steamid = session.get('steamid')
    key = session.get('key')
    if not steamid or not key:
        return redirect(url_for('landing_page'))
    user_profile = user(key, steamid)
    owned_games = amount_owned_games(key, steamid)
    owned_game_info = owned_games_info(key, steamid, limit=20)
    friend_list_info = friends_list_info(key, steamid, limit=5)
    return render_template('profile.html', user_profile=user_profile, owned_games=owned_games,
                           friend_list_info=friend_list_info, owned_game_info=owned_game_info)


@app.route('/home/')
def home():
    """
    Function Description:
        Displays the home page with information about random Steam games.
    """
    game_info = info_for_steam_games(limit=10)
    return render_template('home.html', game_info=game_info)


@app.route('/game/<appid>')
def game(appid):
    """
    Function Description:
        Displays information for a specific game.
    Parameters:
        appid: The ID of the game.
    """
    games_data = steam_game_info(appid)
    return render_template('game.html', game=games_data)


@app.route('/stats/')
def stats():
    """
    Function Description:
        Renders the statistics page with different visualizations and analysis results.
    """
    df = data_naar_pandas('puntcomma/json/new_steam.json')
    achievements_playtime = None  # Placeholder for playtime graph (add a similar function if needed)
    frequentie_prijs = kwantitatief_frequentie_prijs(df)
    frequentie_genres = kwalitatief_frequentie_genres(df)
    linear_regression_price = linear_regression_price_rating(
        df['price'].tolist(), df['cijfer'].tolist(), a=2.5, b=0.5)  # Adjust a and b as per your regression results

    results = sorteer_data(df, 'cijfer', ascending_bool=True)
    return render_template('stats.html', linear_regression_price=linear_regression_price,
                           frequentie_genres=frequentie_genres, frequentie_prijs=frequentie_prijs,
                           achievements_playtime=achievements_playtime, results=results)


@app.route('/owned_games/')
def owned_games():
    """
    Function Description:
        Displays the owned games for the logged-in user.
    """
    key = session.get('key')
    steamid = session.get('steamid')
    if not steamid or not key:
        return redirect(url_for('landing_page'))
    game_name = owned_games_info(key, steamid, limit=15)
    return render_template('owned_games.html', game_name=game_name)


@app.route('/test_profile/<key>/<user_id>', methods=['POST'])
def test_profile(key, user_id):
    user_profile = user(key, user_id)
    return jsonify(user_profile)


@app.route('/test_games/<key>/<user_id>', methods=['POST'])
def test_games(key, user_id):
    user_games = all_owned_games(key, user_id)
    return jsonify(user_games)


@app.route('/test_amount_of_games/<key>/<user_id>', methods=['POST'])
def test_amount_of_games(key, user_id):
    amount_user_games = amount_owned_games(key, user_id)
    return jsonify(amount_user_games)


if __name__ == '__main__':
    app.run(debug=True, port=5000, host="0.0.0.0")