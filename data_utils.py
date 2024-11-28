import pandas as pd
from sqlalchemy import create_engine

# Database connection parameters
DB_CONFIG = {
    "host": "40.114.250.29",
    "port": "5432",
    "database": "steamdb",
    "user": "teammember1",
    "password": "ASDFG"
}

# SQLAlchemy connection string
DATABASE_URI = f'postgresql://{DB_CONFIG["user"]}:{DB_CONFIG["password"]}@{DB_CONFIG["host"]}:{DB_CONFIG["port"]}/{DB_CONFIG["database"]}'

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URI)

def db_to_pandas(query):
    """
    Function Description:
        This function loads data from the PostgreSQL database and converts it into a Pandas DataFrame.
    Parameters:
        query: SQL query to execute.
    Return:
        Pandas DataFrame containing the data.
    """
    with engine.connect() as connection:
        return pd.read_sql_query(query, connection)

def laad_eerste_game(df):
    """
    Function Description:
        This function selects the first game from a Pandas DataFrame.
    Parameters:
        df: Pandas DataFrame.
    Return:
        The first game as a Pandas Series.
    """
    return df.iloc[0, :]

def sorteer_data(df, column, ascending_bool, extra_column=None):
    """
    Function Description:
        This function sorts data in a Pandas DataFrame based on the given parameters.
    Parameters:
        df: Pandas DataFrame.
        column: Column to sort on.
        ascending_bool: Sort order (True for ascending, False for descending).
        extra_column (optional): Additional column to sort by.
    Return:
        Sorted Pandas DataFrame.
    """
    if extra_column:
        sorted_df = df.sort_values(by=[column, extra_column], ascending=ascending_bool)
    else:
        sorted_df = df.sort_values(by=column, ascending=ascending_bool)
    return sorted_df

def pandas_naar_database(df, table_name):
    """
    Function Description:
        This function inserts data from a Pandas DataFrame into a PostgreSQL table.
    Parameters:
        df: Pandas DataFrame.
        table_name: Name of the table to save the data.
    Return:
        None.
    """
    with engine.connect() as connection:
        df.to_sql(table_name, con=connection, if_exists='append', index=False)

if __name__ == "__main__":
    # Example usage: Load data from the database to a DataFrame
    query = "SELECT * FROM games LIMIT 10"
    df = db_to_pandas(query)
    print(df)

    # Sort the DataFrame
    sorted_df = sorteer_data(df, 'name', True)
    print(sorted_df)
