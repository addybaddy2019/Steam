import psycopg2
import matplotlib.pyplot as plt

# Database connection details
DB_HOST = '40.114.250.29'
DB_PORT = '5432'
DB_NAME = 'postgres'
DB_USER = 'teammember1'
DB_PASSWORD = 'ASDFG'

def get_most_played_games():
    """
    Fetch the most-played games based on average playtime from the database.
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

        # Query to fetch game names and average playtime
        query = """
            SELECT name, average_playtime
            FROM games_data
            WHERE average_playtime IS NOT NULL
            ORDER BY average_playtime DESC
            LIMIT 10;
        """
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        connection.close()
        return results  # List of tuples [(name, average_playtime), ...]
    except psycopg2.Error as e:
        print(f"Database error: {e.pgcode} - {e.pgerror}")
    except Exception as e:
        print(f"Error fetching data from database: {str(e)}")
    return []

def plot_most_played_games():
    """
    Generate a bar chart for the most-played games based on average playtime.
    """
    # Fetch data from the database
    data = get_most_played_games()
    if not data:
        print("No data available to plot.")
        return

    # Extract game names and playtimes
    game_names = [row[0] for row in data]
    average_playtimes = [row[1] for row in data]

    # Create the bar chart
    plt.figure(figsize=(10, 6))
    plt.barh(game_names, average_playtimes, color='skyblue')
    plt.xlabel('Average Playtime (minutes)')
    plt.ylabel('Game Names')
    plt.title('Most Played Games by Average Playtime')
    plt.gca().invert_yaxis()  # Invert y-axis to show the top game first
    plt.tight_layout()

    # Save the graph to the current directory
    plt.savefig('most_played_games.png')
    plt.close()
    print("Graph saved as 'most_played_games.png'")

if __name__ == '__main__':
    plot_most_played_games()
# Bronen:
# https://canvas.hu.nl/courses/44597/pages/ai6-algoritmiek-lineaire-regressie
# https://youtu.be/zcUliVmptHY?feature=shared
# https://www.khanacademy.org/data/more-on-regression/v/regression-line-example
# https://chatgpt.com/share/67649710-c464-8001-b3d1-bcd8e5397911
# https://www-jetbrains-com.translate.goog/?hist=true#session
