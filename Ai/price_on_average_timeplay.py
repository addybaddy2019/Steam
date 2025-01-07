import psycopg2
import matplotlib.pyplot as plt

# Database connection details
DB_HOST = '40.114.250.29'
DB_PORT = '5432'
DB_NAME = 'postgres'
DB_USER = 'teammember1'
DB_PASSWORD = 'ASDFG'

def fetch_data_for_regression(query):
    """
    Fetch and sort data for regression analysis from the database.
    Returns two sorted lists: x and y.
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
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        connection.close()

        # Sort data by x-values (the first column)
        sorted_results = sorted(results, key=lambda row: row[0])
        x = [float(row[0]) for row in sorted_results]
        y = [float(row[1]) for row in sorted_results]
        return x, y
    except psycopg2.Error as e:
        print(f"Database error: {e.pgcode} - {e.pgerror}")
    except Exception as e:
        print(f"Error fetching data from database: {str(e)}")
    return [], []

def calculate_mean(data):
    """Calculate the mean of a list of numbers."""
    return sum(data) / len(data) if data else 0

def calculate_median(data):
    """Calculate the median of a list of numbers."""
    n = len(data)
    if n == 0:
        return 0
    mid = n // 2
    if n % 2 == 0:
        return (data[mid - 1] + data[mid]) / 2
    return data[mid]

def linear_regression_lsm(x, y):
    """Linear regression using the least squares method."""
    x_mean = calculate_mean(x)
    y_mean = calculate_mean(y)
    numerator = sum((xi - x_mean) * (yi - y_mean) for xi, yi in zip(x, y))
    denominator = sum((xi - x_mean) ** 2 for xi in x)
    b1 = numerator / denominator
    b0 = y_mean - b1 * x_mean
    return b0, b1

def gradient_descent(x, y, num_iterations=1000, learning_rate=0.0001):
    """Linear regression using gradient descent."""
    b, a = 0, 0  # Initialize coefficients

    for _ in range(num_iterations):
        for xi, yi in zip(x, y):
            error = (a + b * xi) - yi
            a -= learning_rate * error
            b -= learning_rate * xi * error

    return a, b

def plot_regression(x, y, coefficients_lsm, coefficients_gd, xlabel, ylabel, title, filename):
    """Plot the regression results."""
    plt.figure(facecolor='#1b2838')
    # Scatter plot of the data
    plt.scatter(x, y, color='#354f52', label='Data Points')

    # Line for least squares regression
    plt.plot(x, [coefficients_lsm[0] + coefficients_lsm[1] * xi for xi in x],
             color='red', label=f'LSM: b0={coefficients_lsm[0]:.2f}, b1={coefficients_lsm[1]:.2f}')

    # Line for gradient descent regression
    plt.plot(x, [coefficients_gd[0] + coefficients_gd[1] * xi for xi in x],
             color='green', alpha=0.7, label=f'GD: b0={coefficients_gd[0]:.2f}, b1={coefficients_gd[1]:.2f}')

    plt.xlabel(xlabel, color='white')
    plt.ylabel(ylabel, color='white')
    plt.title(title, color='white')
    plt.legend()
    plt.xticks(color='white')
    plt.yticks(color='white')
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()
    print(f"Graph saved as '{filename}'")

if __name__ == '__main__':
    # First graph: Average Rating vs Price
    query1 = """
        SELECT (positive_ratings * 1.0 / (positive_ratings + negative_ratings)) AS average_rating, price
        FROM games_data
        WHERE positive_ratings + negative_ratings > 0 AND price IS NOT NULL
    """
    x1, y1 = fetch_data_for_regression(query1)

    print("Descriptive Statistics for Average Rating vs Price:")
    print(f"Mean (Average Rating): {calculate_mean(x1):.2f}")
    print(f"Median (Average Rating): {calculate_median(x1):.2f}")
    print(f"Mean (Price): {calculate_mean(y1):.2f}")
    print(f"Median (Price): {calculate_median(y1):.2f}")

    coefficients_lsm1 = linear_regression_lsm(x1, y1)
    coefficients_gd1 = gradient_descent(x1, y1)

    plot_regression(x1, y1, coefficients_lsm1, coefficients_gd1,
                    xlabel='Average Rating', ylabel='Price ($)',
                    title='Linear Regression: Average Rating vs Price',
                    filename='../static/Images/rating_price_graph.png')

    # Second graph: Playtime vs Achievements
    query2 = """
        SELECT average_playtime, achievements
        FROM games_data
        WHERE average_playtime IS NOT NULL AND achievements IS NOT NULL
    """
    x2, y2 = fetch_data_for_regression(query2)

    print("Descriptive Statistics for Playtime vs Achievements:")
    print(f"Mean (Playtime): {calculate_mean(x2):.2f}")
    print(f"Median (Playtime): {calculate_median(x2):.2f}")
    print(f"Mean (Achievements): {calculate_mean(y2):.2f}")
    print(f"Median (Achievements): {calculate_median(y2):.2f}")

    coefficients_lsm2 = linear_regression_lsm(x2, y2)
    coefficients_gd2 = gradient_descent(x2, y2)

    plot_regression(x2, y2, coefficients_lsm2, coefficients_gd2,
                    xlabel='Playtime (minutes)', ylabel='Achievements',
                    title='Linear Regression: Playtime vs Achievements',
                    filename='../static/Images/playtime_achievements_graph.png')
