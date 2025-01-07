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

def calculate_mean(data):
    """
    Calculate the mean (average) of a list of numbers.
    """
    if len(data) == 0:
        return 0
    total = sum(data)
    return total / len(data)

def calculate_median(data):
    """
    Calculate the median of a list of numbers.
    """
    if len(data) == 0:
        return 0
    sorted_data = sorted(data, reverse=True)  # Correct the order to match graph
    n = len(sorted_data)
    mid = n // 2
    if n % 2 == 0:
        return (sorted_data[mid - 1] + sorted_data[mid]) / 2  # Average of middle two
    return sorted_data[mid]  # Middle value for odd-length list

def plot_most_played_games():
    """
    Generate a bar chart for the most-played games with descriptive statistics.
    """
    # Fetch data from the database
    data = get_most_played_games()
    if not data:
        print("No data available to plot.")
        return

    # Extract game names and playtimes
    game_names = [row[0] for row in data]
    average_playtimes = [row[1] for row in data]

    # Calculate mean and median
    mean_playtime = calculate_mean(average_playtimes)
    median_playtime = calculate_median(average_playtimes)

    # Create the bar chart
    plt.figure(figsize=(12, 8))
    plt.barh(game_names[::-1], average_playtimes[::-1], color='skyblue')  # Reverse for correct order
    plt.axvline(mean_playtime, color='red', linestyle='--', label=f'Mean: {mean_playtime:.2f} mins')
    plt.axvline(median_playtime, color='green', linestyle='--', label=f'Median: {median_playtime:.2f} mins')
    plt.xlabel('Average Playtime (minutes)', fontsize=12)
    plt.ylabel('Game Names', fontsize=12)
    plt.title('Most Played Games by Average Playtime with Descriptive Statistics', fontsize=14)
    plt.legend(loc='lower right')
    plt.tight_layout()

    # Save the graph to the current directory
    plt.savefig('most_played_games_stats_corrected.png')
    plt.close()
    print("Graph saved as 'most_played_games_stats_corrected.png'")

if __name__ == '__main__':
    plot_most_played_games()
