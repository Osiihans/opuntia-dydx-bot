from datetime import datetime, timedelta
from func_utils import format_number
import time

from pprint import pprint

#Place market order

def place_market_order(client,market,side,size,price,reduce_only):
    #Get position Id
    account_response = client.private.get_account()
    position_id = account_response.data["account"]["positionId"]

    #Get expiration time
    server_time = client.public.get_time()
    """
        I resolved the error  DydxApiError(status_code=400, response={'errors': [{'msg': 'Order expiration cannot be less than 1 minute(s) in the future'}]})
        by  changing .replace("Z", "") to .replace('Z','+00:00') below
    """
    expiration = datetime.fromisoformat(server_time.data['iso'].replace("Z","+00:00")) + timedelta(seconds=70)

    #Place an order

    placed_order = client.private.create_order(
        position_id=position_id,
        market=market,
        side=side,
        order_type="MARKET",
        post_only=False,
        size=size,
        price=price,
        limit_fee='0.015',
        expiration_epoch_seconds=expiration.timestamp(),
        time_in_force="FOK",
        reduce_only=reduce_only
    )
    
    #Return result
    return placed_order.data

#Abort all open positions
def abort_all_positions(client):
    
    #Cancel all order
    client.private.cancel_all_orders()
    
    #Protect API
    time.sleep(0.5)
    
    #Get markets for refernce of tick size
    markets = client.public.get_markets().data
    
    #Protect API
    time.sleep(0.5)
    
    #GET all open positions
    positions = client.private.get_positions(status="OPEN")
    all_positions = positions.data["positions"]
    
    #Handle open positions
    close_orders = []
    
    if len(all_positions) > 0:
        
        #Loop through each positions
        for position in all_positions:
            
            #Determin the market
            market = position["market"]
            
            #Determine Side
            side = "BUY"
            if position["side"] == "LONG":
                side = "SELL"
                
            # Get price
            price = float(position["entryPrice"])
            accept_price = price * 1.7 if side == "BUY" else price * 0.3
            tick_size = markets["markets"][market]["tickSize"]
            accept_price = format_number(accept_price, tick_size)
            
            # Place order to close
            order = place_market_order(
                client,
                market,
                side,
                position["sumOpen"],
                accept_price,
                True
            )
            
            #Append the result
            close_orders.append(order)
            
            #Protect Api
            time.sleep(0.2)
            
        return close_orders
            