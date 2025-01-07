import psycopg2
import matplotlib.pyplot as plt
from collections import defaultdict

# Database connection details
DB_HOST = '40.114.250.29'
DB_PORT = '5432'
DB_NAME = 'postgres'
DB_USER = 'teammember1'
DB_PASSWORD = 'ASDFG'

def fetch_games_per_year():
    """
    Fetch the number of games released per year from the database.
    Returns a dictionary with years as keys and game counts as values.
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

        # Query to fetch release year and count games
        query = """
            SELECT EXTRACT(YEAR FROM release_date) AS year, COUNT(*) AS game_count
            FROM games_data
            WHERE release_date IS NOT NULL
            GROUP BY year
            ORDER BY year;
        """
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        connection.close()

        # Convert results to a dictionary
        data = defaultdict(int)
        for row in results:
            year = int(row[0])
            game_count = row[1]
            data[year] = game_count

        return data
    except psycopg2.Error as e:
        print(f"Database error: {e.pgcode} - {e.pgerror}")
    except Exception as e:
        print(f"Error fetching data from database: {str(e)}")
    return {}

def calculate_mean(data):
    """
    Calculate the mean (average) of a list of numbers manually.
    """
    if len(data) == 0:
        return 0
    total = 0
    for num in data:  # Sum manually
        total += num
    return total / len(data)

def calculate_median(data):
    """
    Calculate the median of a list of numbers manually.
    """
    if len(data) == 0:
        return 0
    n = len(data)
    # Manual sorting using bubble sort
    for i in range(n):
        for j in range(0, n - i - 1):
            if data[j] > data[j + 1]:
                data[j], data[j + 1] = data[j + 1], data[j]
    mid = n // 2
    return (data[mid - 1] + data[mid]) / 2 if n % 2 == 0 else data[mid]

def plot_games_per_year(data):
    """
    Plot the number of games released per year with descriptive statistics.
    Args:
        data (dict): A dictionary with years as keys and game counts as values.
    """
    if not data:
        print("No data available to generate the graph.")
        return

    # Extract years and counts
    years, counts = [], []
    for year, count in data.items():
        years.append(year)
        counts.append(count)

    # Calculate mean and median
    mean_count = calculate_mean(counts)
    median_count = calculate_median(counts)

    # Plot the data
    plt.figure(figsize=(14, 7))
    plt.bar(years, counts, color='skyblue', label='Games Released')
    plt.axhline(mean_count, color='red', linestyle='--', label=f'Mean: {mean_count:.2f}')
    plt.axhline(median_count, color='green', linestyle='--', label=f'Median: {median_count:.2f}')
    plt.xlabel('Year', fontsize=14)
    plt.ylabel('Number of Games Released', fontsize=14)
    plt.title('Number of Games Released Per Year with Descriptive Statistics', fontsize=16)
    plt.legend(loc='upper left')
    plt.tight_layout()

    # Save the graph
    plt.savefig('games_per_year_with_stats.png')
    print("Graph saved as 'games_per_year_with_stats.png'")
    plt.show()

if __name__ == '__main__':
    # Fetch data and generate the graph
    data = fetch_games_per_year()
    plot_games_per_year(data)
