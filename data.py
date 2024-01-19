import pandas as pd
import sqlite3
import logging
logger = logging.getLogger()
logger.setLevel(logging.CRITICAL)

def deleteTable(table_name, db='stock_data.db'):
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect(db)
        cursor = conn.cursor()
        # Ensure the table name is properly formatted to handle special characters
        formatted_table_name = f'"{table_name}"'
        # SQL statement to drop the table
        drop_table_query = f"DROP TABLE IF EXISTS {formatted_table_name}"
        # Execute the query
        cursor.execute(drop_table_query)
        # Commit the changes
        conn.commit()
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the database connection
        conn.close()

def getTables(db='stock_data.db'):
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect(db)
        # Create a cursor object using the cursor() method
        cursor = conn.cursor()
        # Retrieve the list of tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        # Fetch all the rows
        tables = cursor.fetchall()
        # Print the list of tables
        for table in tables:
            print(table[0])
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the database connection
        conn.close()

def getDataFromTable(tableName: str, db='stock_data.db'):
    #\"strat_{strat}_view_{view}_lookback_{lookback}_from_{dateFrom}_to_{dateTO}_stocks_{stringPlaceHolder}"
    #STRAT: 2 VIEW: 1 LOOKBACK: 30 From: 2020-01-01 To: 2024-01-01 Stocks: ['QQQ', 'SPY', 'WMT']
    try:
        conn = sqlite3.connect(db)
        # Query to check the content of a table
        query = f"SELECT * FROM {tableName} LIMIT 500"  # Adjust the table name
        df = pd.read_sql_query(query, conn)
        # Print the result
        print(df)
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the connection
        conn.close()

def writeRaw(data: pd.DataFrame, stock: str):
    #set symbol column
    data = data.copy()
    data.insert(0, 'Symbol', stock)
    try:
        # Assume 'data' is your DataFrame with 10 years of AAPL data
        conn = sqlite3.connect('raw_Data.db')
        cursor = conn.cursor()
        # Create a temporary table
        cursor.execute("""
            CREATE TEMPORARY TABLE temp_stock_data (
                Symbol TEXT, 
                Date TEXT, 
                Open REAL, 
                High REAL, 
                Low REAL, 
                Close REAL, 
                AdjClose REAL, 
                Volume INTEGER
            );
        """)
        conn.commit()
        # Insert new data into the temporary table
        data.to_sql('temp_stock_data', conn, if_exists='append', index=False)
        # Upsert from the temporary table to the main table
        cursor.execute("""
            INSERT INTO stock_prices_daily (Symbol, Date, Open, High, Low, Close, AdjClose, Volume)
            SELECT Symbol, Date, Open, High, Low, Close, AdjClose, Volume FROM temp_stock_data
            WHERE true
            ON CONFLICT(Symbol, Date) 
            DO UPDATE SET
                Date = excluded.Date,
                Open = excluded.Open,
                High = excluded.High,
                Low = excluded.Low,
                Close = excluded.Close,
                AdjClose = excluded.AdjClose,
                Volume = excluded.Volume;
        """)
        conn.commit()

        # Drop the temporary table
        cursor.execute("DROP TABLE temp_stock_data;")
        conn.commit()
    except sqlite3.Error as e:
        logger.critical("SQL WRITE FUNC ERROR")
        print(f"An error occurred: {e}")
    finally:
        conn.close()

#Only use inside another sql function or close connection after
def dataExists(stock: str, start: str, end: str, conn) -> bool:
    """
    Checks if there is at least one entry for each year in the range for a given stock.
    Args:
    stock (str): The stock symbol.
    start (str): The start date in 'YYYY-MM-DD' format.
    end (str): The end date in 'YYYY-MM-DD' format.
    conn: SQLite database connection object.

    Returns:
    bool: True if at least one entry exists for each year, False otherwise.
    """
    start_year = int(start[0:4])
    end_year = int(end[0:4])
    cursor = conn.cursor()
    try:
        for year in range(start_year, end_year + 1):
            start_date = f"{year}-01-03"  # Adjust if necessary to January 1st
            end_date = f"{year}-12-31"
            query = """
            SELECT EXISTS(
                SELECT 1 FROM stock_prices_daily
                WHERE Symbol = ? AND date(Date) BETWEEN date(?) AND date(?)
                LIMIT 1
            );
            """
            cursor.execute(query, (stock, start_date, end_date))
            if cursor.fetchone()[0] == 0:
                # No data found for this year, return False
                return False
        # Data found for all years in the range
        return True
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return False

def getData(stock: str, start_date: str, end_date: str, conn) -> pd.DataFrame:
    """
    Retrieves stock data for a given date range from the database.

    Args:
    stock (str): The stock symbol.
    start_date (str): The start date in 'YYYY-MM-DD' format.
    end_date (str): The end date in 'YYYY-MM-DD' format.
    conn: SQLite database connection object.

    Returns:
    pd.DataFrame: DataFrame containing the requested stock data.
    """
    query = """
    SELECT * FROM stock_prices_daily
    WHERE Symbol = ? AND Date BETWEEN ? AND ?
    ORDER BY Date;
    """
    #logger.critical(f"Trying to get data!")
    df = pd.read_sql_query(query, conn, params=(stock, start_date, end_date))
    debug = df.columns
    #logger.critical(f"TRYING: {debug}")
    df.loc[:, 'Date'] = pd.to_datetime(df.loc[:, 'Date']) # Convert the 'Date' column to datetime objects
    df.set_index('Date', inplace=True)      # Set the 'Date' column as the index of the DataFrame
    df.drop('Symbol', axis=1, inplace=True)
    #logger.critical(f"TRYING: {df}")
    return df