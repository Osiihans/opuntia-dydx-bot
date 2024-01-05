from constants import ABORT_ALL_POSITIONS, FIND_COINTEGRATED
from func_connections import connect_dydx
from funct_private import abort_all_positions
from func_public import construct_market_prices

if __name__ == "__main__":
    
    # # Connect to client
    try:
        print("Connecting to client")
        client = connect_dydx()
    except Exception as e:    
        print("Error connecting to client: ", e )
        exit(1)
    
    #Abort all positions    
    if ABORT_ALL_POSITIONS:
        try:
           print("Clossing all open positions")
           close_orders = abort_all_positions(client)
        except Exception as e:
            print("Error clossing all positions: ", e )
            exit(1)
            
    # Find Cointergrated Pairs
    if FIND_COINTEGRATED:
        
        #Construct Market Prices
        try:
           print("Fetching market prices, please allow 3mins...")
           df_market_prices = construct_market_prices(client)
        except Exception as e:
            print("Error constructing market prices: ", e )
            exit(1)