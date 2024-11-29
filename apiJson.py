# Team FaaaM,
# Opdracht: Steam
# Bronen: W3school, more ...

from flask import Flask, render_template, abort, url_for
from sqlalchemy import create_engine, text

app = Flask(__name__)

# Database connection details
DB_HOST = '40.114.250.29'
DB_PORT = '5432'
DB_NAME = 'steamdb'
DB_USER = 'teammember1'
DB_PASSWORD = 'ASDFG'

# SQLAlchemy connection string
DATABASE_URI = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URI)

def get_steam_game_info(gameid):
    """
    Fetch information about a specific Steam game from the PostgreSQL database.
    """
    with engine.connect() as connection:
        query = text("SELECT * FROM games_data WHERE appid = :gameid")
        result = connection.execute(query, gameid=gameid).fetchone()
        if result:
            # Extract the data in a cleaner way and handle JSON-like structures
            return {
                "appid": result['appid'],
                "name": result['name'],
                "release_date": result['release_date'],
                "developer": result['developer'],
                "publisher": result['publisher'],
                "price": result['price'],
                "platforms": f"Windows: {'Yes' if result['platforms']['windows'] else 'No'}, "
                             f"Mac: {'Yes' if result['platforms']['mac'] else 'No'}, "
                             f"Linux: {'Yes' if result['platforms']['linux'] else 'No'}" if isinstance(result['platforms'], dict) else result['platforms'],
                "categories": ", ".join([category['description'] if isinstance(category, dict) else category for category in result['categories']]) if result['categories'] else "No Categories Available",
                "genres": ", ".join([genre['description'] if isinstance(genre, dict) else genre for genre in result['genres']]) if result['genres'] else "No Genres Available",
                "owners": result['owners'],
                "median_playtime": result['median_playtime'],
                "average_playtime": result['average_playtime'],
                "positive_ratings": result['positive_ratings'],
                "negative_ratings": result['negative_ratings'],
                "achievements": len(result['achievements']) if result['achievements'] else "No Achievements Available",
                "steamspy_tags": result['steamspy_tags'],
                "required_age": result['required_age'],
                "english": "Yes" if result['english'] == 1 else "No"
            }
    return None

@app.route('/profile/<int:appid>')
def profile(appid):
    # Find the profile that matches the appid from the database
    user_profile = get_steam_game_info(appid)

    if user_profile:
        return render_template('profile.html', user_profile=user_profile)
    else:
        abort(404)  # Return a 404 error if the profile is not found

# Home route to display a list of games for navigation
@app.route('/')
def home():
    with engine.connect() as connection:
        query = text("SELECT appid, name FROM games_data LIMIT 10")
        results = connection.execute(query).fetchall()
        games_list = [dict(game) for game in results]
    return render_template('home.html', games=games_list)  # Display the first 10 games as an example

if __name__ == '__main__':
    app.run(debug=True)
