import psycopg2
from sqlalchemy import create_engine
from binance.client import Client
import os
from dotenv import load_dotenv
import schedule
from datetime import datetime
import pandas as pd


# Define constants
ticker = 'BTCUSDT'
currency = 'USD'
source = 'BINANCE'

# connect to DB


def connect_db():

    load_dotenv()
    host = os.getenv('DB_HOSTNAME')
    port = os.getenv('DB_PORT')
    user = os.getenv('DB_USERNAME')
    password = os.getenv('DB_PASSWORD')

    # Creating Postgres DB Client
    try:
        connection = psycopg2.connect(
            host=host,
            port=port,
            user=user,
            password=password,
        )
        print("successfully connected to DB", connection)

    except Exception as e:
        print("error connecting to DB", e)

    # Setup DB cursor
    return connection.cursor()


# Create Binance client
def connect_binance() -> Client:
    api_key = os.getenv('BINANCE_API_KEY')
    api_secret = os.getenv('BINANCE_SECRET_KEY')
    return Client(api_key, api_secret)


# Fetch the order book data for BTC/USDT
def fetch_order_book_data(binance_client: Client) -> pd.DataFrame:
    order_book = binance_client.get_order_book(symbol=ticker)
    print("""Order Book Preview""")
    print(order_book)

    # Get current timestamp
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Prepare the bid and ask data
    bids = order_book['bids']
    asks = order_book['asks']

    # Initialize lists to hold bid and ask data for the PD DataFrame
    bid_data = []
    ask_data = []

    # Add bid data to the list
    for bid in bids:
        try:
            price = bid[0]  # Price of the bid in string
            volume = bid[1]  # Volume of the bid in string
            if float(volume) > 0:  # Ensure there is a valid volume
                bid_data.append(
                    {'created_at': timestamp, 'price': price, 'currency': currency, 'ticker': ticker, 'bid_volume': volume, 'source': source})
        except Exception as e:
            print(f"Error processing bid: {bid}, error: {e}")

    # Add ask data to the list
    for ask in asks:
        try:
            price = ask[0]  # Price of the ask in string
            volume = ask[1]  # Volume of the ask in string
            if float(volume) > 0:  # Ensure there is a valid volume
                ask_data.append(
                    {'created_at': timestamp, 'price': price, 'currency': currency, 'ticker': ticker, 'ask_volume': volume, 'source': source})
        except Exception as e:
            print(f"Error processing ask: {ask}, error: {e}")

    # Combine bid and ask data into one list
    order_book_data = bid_data + ask_data

    print("length of order book", len(order_book_data))

    # Create a pandas DataFrame to display the order book
    df = pd.DataFrame(order_book_data)

    # Display the table
    print("order book data", df)
    return df


def save_order_book_to_db(order_book_df: pd.DataFrame):
    # create postgres engine
    load_dotenv()
    db_engine_str = "postgresql://" + str(os.getenv("DB_USERNAME")) + ":" + str(os.getenv(
        "DB_PASSWORD")) + "@" + str(os.getenv("DB_HOSTNAME")) + ":" + str(os.getenv("DB_PORT")) + "/"
    engine = create_engine(db_engine_str)

    try:
        order_book_df.to_sql('order_book', engine,
                             if_exists="append", index=False)
        print("successfully saved to DB")
    except Exception as e:
        print("error while saving to DB:", e)


def run_cron(binance_client):
    order_book_dataframe = fetch_order_book_data(binance_client)
    save_order_book_to_db(order_book_dataframe)
    return


def main():
    binance_client = connect_binance()


if __name__ == '__main__':
    main()
