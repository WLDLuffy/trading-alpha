import time
from datetime import datetime
from binance.client import Client
import pandas as pd

# Step 1: Data Collection and Order Book Monitoring

# Binance API setup

# Set up API keys (replace with your own)
api_key = 'Wch2r1tMoafuUVuml3SCWYOGzaNYCzo0sv9Z4jssqmnFbHfXXTsJ19KFBDj5wUM2'
api_secret = 'i0UcrW0c5ZIcaeWQfWo0P9Qs8s39v79oF1F6DbpGjijUDpv1Fy16AoReG5nLKbTI'

# Create Binance client
client = Client(api_key, api_secret)

# Fetch the order book data for BTC/USDT
symbol = 'BTCUSDT'

# Fetch the order book data for BTC/USDT
order_book = client.get_order_book(symbol=symbol)

# Get current timestamp
timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# Print the order book
print(order_book)

print("""Order Book Preview""")

# Get current timestamp
timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# Prepare the bid and ask data
bids = order_book['bids']
asks = order_book['asks']

# Create lists to hold bid and ask data for the DataFrame
bid_data = []
ask_data = []

# Add bid data to the list
for bid in bids:
    try:
        price = float(bid[0])  # Price of the bid
        volume = float(bid[1])  # Volume of the bid
        if volume > 0:  # Ensure there is a valid volume
            bid_data.append(
                {'Timestamp': timestamp, 'Price Level': price, 'Bid Volume': volume})
    except Exception as e:
        print(f"Error processing bid: {bid}, error: {e}")

# Add ask data to the list
for ask in asks:
    try:
        price = float(ask[0])  # Price of the ask
        volume = float(ask[1])  # Volume of the ask
        if volume > 0:  # Ensure there is a valid volume
            ask_data.append(
                {'Timestamp': timestamp, 'Price Level': price, 'Ask Volume': volume})
    except Exception as e:
        print(f"Error processing ask: {ask}, error: {e}")

# Combine bid and ask data into one list
order_book_data = bid_data + ask_data

# Create a pandas DataFrame to display the order book
df = pd.DataFrame(order_book_data)

# Display the table
print("order book data", df)


# Analyze order book
# Set up your API keys (replace with your own)
api_key = 'Wch2r1tMoafuUVuml3SCWYOGzaNYCzo0sv9Z4jssqmnFbHfXXTsJ19KFBDj5wUM2'
api_secret = 'i0UcrW0c5ZIcaeWQfWo0P9Qs8s39v79oF1F6DbpGjijUDpv1Fy16AoReG5nLKbTI'

# Initialize the Binance client
client = Client(api_key, api_secret)

# Function to fetch the order book data for BTC/USDT


def fetch_order_book():
    order_book = client.get_order_book(symbol='BTCUSDT')
    return order_book


best_bid = float(order_book['bids'][0][0])  # Highest bid
best_ask = float(order_book['asks'][0][0])  # Lowest ask
spread = best_ask - best_bid

# 1: Analyze Bid Ask Spread
print("""#1: Analyze Bid Ask Spread""")
print(f"Best Bid: {best_bid}, Best Ask: {best_ask}, Spread: {spread}")

# Define the number of top bids/asks to display
n = 5  # You can change this value as needed

# Assuming 'order_book' is your data structure with bids and asks
top_bids = order_book['bids'][:n]  # Top n bid prices and quantities
top_asks = order_book['asks'][:n]  # Top n ask prices and quantities

# Print the top n bids and asks
print(f"Top {n} Bids:")
for bid in top_bids:
    print(f"Price: {bid[0]}, Quantity: {bid[1]}")

print(f"\nTop {n} Asks:")
for ask in top_asks:
    print(f"Price: {ask[0]}, Quantity: {ask[1]}")

# 2: Analyze Volume
print("""\n#2: Analyze Volume""")

bid_volume = sum([float(bid[1]) for bid in order_book['bids']])
ask_volume = sum([float(ask[1]) for ask in order_book['asks']])
print(f"Total Bid Volume: {bid_volume}, Total Ask Volume: {ask_volume}")


# 3: Filter Large Orders = Order volume > threshold x average order size
# Define threshold
threshold = 5
print("""\n#3: Filter Large Orders = Order volume > threshold x average order size""")


def filter_large_orders(order_book, threshold):

    print(f"Using threshold value: {threshold}")
    all_bids = [float(bid[1]) for bid in order_book['bids']]
    all_asks = [float(ask[1]) for ask in order_book['asks']]
    avg_order_size = (sum(all_bids) + sum(all_asks)) / \
        (len(all_bids) + len(all_asks))

    large_buy_orders = []
    large_sell_orders = []
    # Filter for orders larger than the threshold x average order size
    for bid in order_book['bids']:
        price = float(bid[0])
        quantity = float(bid[1])
        if quantity > avg_order_size * threshold:  # Threshold multiplier
            large_buy_orders.append({'price': price, 'quantity': quantity})

    for ask in order_book['asks']:
        price = float(ask[0])
        quantity = float(ask[1])
        if quantity > avg_order_size * threshold:  # Threshold multiplier
            large_sell_orders.append({'price': price, 'quantity': quantity})

    return large_buy_orders, large_sell_orders


# 4: Filter aggressive market orders
print("""#4: Filter aggressive market orders""")


def detect_aggressive_orders(order_book):
    # Get the best bid (highest buy) and best ask (lowest sell)

    # Aggressive Buy Orders: These are buy orders that bid at or above the best ask price (the lowest available sell order).
    # Aggressive Sell Orders: These are sell orders that ask at or below the best bid price (the highest available buy order).
    highest_bid = float(order_book['bids'][0][0])
    lowest_ask = float(order_book['asks'][0][0])

    # If the price of the order is greater than or equal to the lowest ask price. If it is, it's an aggressive buy order.
    aggressive_buy_orders = []
    # Loop through the asks (sell orders), and check if the price of the order is less than or equal to the highest bid price. If it is, it's an aggressive sell order.
    aggressive_sell_orders = []

    # Iterate through bids (buy side)
    for bid in order_book['bids']:
        price = float(bid[0])
        quantity = float(bid[1])
        if price >= lowest_ask:  # Aggressive buy orders
            aggressive_buy_orders.append(
                {'price': price, 'quantity': quantity})

# Iterate through asks (sell side)
    for ask in order_book['asks']:
        price = float(ask[0])
        quantity = float(ask[1])
        if price <= highest_bid:  # Aggressive sell orders
            aggressive_sell_orders.append(
                {'price': price, 'quantity': quantity})

    return aggressive_buy_orders, aggressive_sell_orders


print()
# Main execution loop
interval = 50  # Define the interval in seconds
y = 3  # Set the number of times to run the main loop

print(
    f"#5: Detects aggressive market orders and large orders every {interval} seconds {y} times")


def main():
    for i in range(y):
        # Fetch the latest order book
        order_book = fetch_order_book()

        # Print the timestamp for each run
        print(f"\n--- Timestamp: {datetime.now()} ---")

        # Detect aggressive market orders
        aggressive_buy_orders, aggressive_sell_orders = detect_aggressive_orders(
            order_book)
        print("Aggressive Buy Orders:", aggressive_buy_orders)
        print("Aggressive Sell Orders:", aggressive_sell_orders)

        # Filter large orders using the threshold
        large_buy_orders, large_sell_orders = filter_large_orders(
            order_book, threshold)
        print("Large Buy Orders:", large_buy_orders)
        print("Large Sell Orders:", large_sell_orders)

        # Wait before fetching the order book again
        time.sleep(interval)


# # Run the main loop
# if name == 'main':
main()
