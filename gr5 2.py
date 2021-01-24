import time

from optibook.synchronous_client import Exchange

import logging

logger = logging.getLogger('client')
logger.setLevel('ERROR')

print("Setup was successful.")

# compare the bid and ask prices of the two instruments


e = Exchange()
a = e.connect()


instrument_limit = 190
instrument_limit1=100
orderBatch = 0


def get_info():
    #print("in get_info")
    #positions = e.get_positions()
    print(e.get_positions())
    #print(abs(positions['PHILIPS_B']) )
    positions = e.get_positions()
    for p in positions:
        print(p, positions[p])
        print(abs(positions['PHILIPS_B']))
        print(abs(positions['PHILIPS_A']))
    pnl = e.get_pnl()
    print("current pnl is", pnl)
    for instrument_id in ['PHILIPS_A', 'PHILIPS_B']:
        outstanding = e.get_outstanding_orders(instrument_id)
        for o in outstanding.values():
            print(f"Outstanding order: order_id({o.order_id}), instrument_id({o.instrument_id}), price({o.price}), volume({o.volume}), side({o.side}) 10")
            print("aaa : ",o.instrument_id )
            #closedOutstanding = e.delete_orders(o.instrument_id)
            #print(closedOutstanding)
    positions1 = e.get_positions()
    
"""
    if  ((abs(positions1['PHILIPS_B']) + abs(positions1['PHILIPS_A'])) > 100 or abs(positions1['PHILIPS_B']) > instrument_limit or abs(positions1['PHILIPS_A']) > instrument_limit):
        #time.sleep(1)
        print(e.get_positions())
        
        for s, p in e.get_positions().items():
            if p > 0:
                e.insert_order(s, price=1, volume=round(p/4,0), side='ask', order_type='ioc')
            elif p < 0:
                e.insert_order(s, price=100000, volume=-round(p/4,0), side='bid', order_type='ioc')
        print(e.get_positions())
  
"""    
    
print("POS : ",e.get_positions())

positions1 = e.get_positions()

if  ((abs(positions1['PHILIPS_B']) + abs(positions1['PHILIPS_A'])) > 250 or abs(positions1['PHILIPS_B']) > instrument_limit or abs(positions1['PHILIPS_A']) > instrument_limit):
    time.sleep(1)
    print(e.get_positions())
    
    for s, p in e.get_positions().items():
        if p > 0:
            e.insert_order(s, price=1, volume=round(p/4,0), side='ask', order_type='ioc')
        elif p < 0:
            e.insert_order(s, price=100000, volume=-round(p/4,0), side='bid', order_type='ioc')
    print(e.get_positions())
  




get_info()
# retreives the best bid/ask price from exchange. If the best bid price for B is greater than the best ask for A, sell to B and buy from A.

for i in range(0, 10000):

    positions = e.get_positions()
    #print("test")
    try:
        
        #print("B Bid : ", e.get_last_price_book('PHILIPS_B').bids[0].price) 
        #print("A Ask : ", e.get_last_price_book('PHILIPS_A').asks[0].price)
        #print("B Ask : ", e.get_last_price_book('PHILIPS_B').asks[0].price) 
        #print("A Bid : ", e.get_last_price_book('PHILIPS_A').bids[0].price)
        
        #if (e.get_last_price_book('PHILIPS_B').asks[0].price > e.get_last_price_book('PHILIPS_A').asks[0].price and e.get_last_price_book('PHILIPS_B').bids[0].price < e.get_last_price_book('PHILIPS_A').bids[0].price and 
        if( (e.get_last_price_book('PHILIPS_B').asks[0].price > e.get_last_price_book('PHILIPS_A').bids[0].price) and  (e.get_last_price_book('PHILIPS_B').asks[0].price - e.get_last_price_book('PHILIPS_A').bids[0].price) > .30) :
        #if (e.get_last_price_book('PHILIPS_B').asks[0].price > e.get_last_price_book('PHILIPS_A').bids[0].price) :
            #print(f"First set of Conditions for Entry 1-2-3-4")
            volume = e.get_last_price_book('PHILIPS_B').bids[0].volume
            price_B = round(e.get_last_price_book('PHILIPS_B').asks[0].price, 3)
            price_A = round(e.get_last_price_book('PHILIPS_A').bids[0].price, 3)
            #print("Check Spread B-mid : ", price_B - (round((price_A + price_B) / 2 ,3)), " A-mid : ", (round((price_A + price_B) / 2 ,3))-price_A )
            mid_price =round((price_A + price_B) / 2 ,3)
            diff = round( abs(price_A-mid_price), 3)
            if volume > 30:
                volume = 30
            
            #if volume > 10:
                
            if((price_A-mid_price)/2 > (mid_price-price_B)):
                if ((positions['PHILIPS_B'] > -instrument_limit1 or positions['PHILIPS_A'] < instrument_limit1) and abs (positions['PHILIPS_B']) + abs(positions['PHILIPS_A']) < 400 ):
                    print("sell B at:",price_B, " and buy A:",price_A, " for",volume," lots")
                    
                    result = e.insert_order('PHILIPS_B', price=price_B, volume=volume, side='ask', order_type='ioc')
                    print(f"Order Id: {result} 1 B-ask")
                    #if result != None:
                    #result = e.insert_order('PHILIPS_A', price=price_A, volume=volume, side='bid', order_type='ioc')
                    print(f"Order Id: {result} 2 A-bid")
        
                    # clearing of positions using limit order from weighted mid price
    
                    mid_price =round((price_A + price_B) / 2 ,3)
                    diff = round( abs(price_A-mid_price), 3)
                    
                    print(mid_price)
                    print(mid_price+.10)
                    
                    print(diff)
                    print(diff+.10)
                    
                
                    result = e.insert_order('PHILIPS_B', price=round(mid_price, 3), volume=volume, side='bid', order_type='limit')
                    
                    #result = e.insert_order('PHILIPS_B', price=round(price_B-.05, 3), volume=volume, side='bid', order_type='limit')
                    #print(f"Order Id: {result} 3 B-bid")
                    
                    #result = e.insert_order('PHILIPS_B', price=round(price_B-.10, 3), volume=volume, side='bid', order_type='limit')
                    #print(f"Order Id: {result} 3 B-bid")
    
                    #result = e.insert_order('PHILIPS_A', price=round(mid_price, 3), volume=volume, side='ask', order_type='limit')
                    
                    #result = e.insert_order('PHILIPS_A', price=round(price_A+.05, 3), volume=volume, side='ask', order_type='limit')
                    #result = e.insert_order('PHILIPS_A', price=round(price_A-.10, 3), volume=volume, side='ask', order_type='limit')
                    #print(f"Order Id: {result} 4 A-ask")
                    
                    #result = e.insert_order('PHILIPS_A', price=round(price_A+.10, 3), volume=volume, side='ask', order_type='limit')
                    #print(f"Order Id: {result} 4 A-ask")
                    
                    time.sleep(1)
                    get_info()
    


    except IndexError:
        pass

    # does the same thing as above but in the reverse direction
    #Sell Philips on the exchange where the price is higher and buy on the exchange where the price is lower

    try:
        #if (e.get_last_price_book('PHILIPS_B').asks[0].price < e.get_last_price_book('PHILIPS_A').asks[0].price and e.get_last_price_book('PHILIPS_A').bids[0].price > e.get_last_price_book('PHILIPS_B').bids[0].price and 
        #Flag = 0
        if( ( e.get_last_price_book('PHILIPS_B').bids[0].price < e.get_last_price_book('PHILIPS_A').asks[0].price) and (e.get_last_price_book('PHILIPS_A').asks[0].price - e.get_last_price_book('PHILIPS_B').bids[0].price) > .30 ): 
            #and (e.get_last_price_book('PHILIPS_A').asks[0].price - e.get_last_price_book('PHILIPS_B').bids[0].price) > .30 ):
            #if(e.get_last_price_book('PHILIPS_B').bids[0].price < e.get_last_price_book('PHILIPS_A').asks[0].price):
            #print(f"First set of Conditions for Entry 5-6-7-8")
            volume = e.get_last_price_book('PHILIPS_B').asks[0].volume
            price_B = round(e.get_last_price_book('PHILIPS_B').bids[0].price-.10, 3)
            price_A = round(e.get_last_price_book('PHILIPS_A').asks[0].price, 3)
            mid_price = (price_A + price_B) / 2
            diff = abs(price_A-mid_price)
                    
            #print("Check Spread B-mid : ", price_A - (round((price_A + price_B) / 2 ,3)), " A-mid : ", (round((price_A + price_B) / 2 ,3))-price_B )
            
            if volume > 30:
                volume = 30
                
            if((price_B-mid_price)/2 > (mid_price-price_A)):
                if ((positions['PHILIPS_B'] < instrument_limit1 or positions['PHILIPS_A'] > -instrument_limit1) and abs (positions['PHILIPS_B']) + abs(positions['PHILIPS_A']) < 400):
                    print("buy B:",price_B, " and sell A:",price_A, " for",volume," lots")
    
                    #result = e.insert_order('PHILIPS_B', price=price_B, volume=volume, side='bid', order_type='ioc')
                    #print(f"Order Id: {result} 5 B-bid")
    
                    #if result != None:
                    result = e.insert_order('PHILIPS_A', price=price_A, volume=volume, side='ask', order_type='ioc')
                    print(f"Order Id: {result} 6 A-ask")
    
                    # clearing of positions using limit order from weighted mid price
                    # Challenge here is you want to have guard rails on either side of the position to minimise losses you will have to implement some algorithm
                    # and data structure to square off all the limit orders (TBC) 
    
                    
                    #result = e.insert_order('PHILIPS_B', price=round(mid_price,3), volume=volume, side='ask', order_type='limit')
                    #result = e.insert_order('PHILIPS_B', price=round(price_B+.05,3), volume=volume, side='ask', order_type='limit')
                    print(f"Order Id: {result} 3 B-bid")
                    
                    
                    #result = e.insert_order('PHILIPS_B', price=mid_price, volume=volume, side='ask', order_type='limit')
                    #print(f"Order Id: {result} 7 B-ask")
    
                    #result = e.insert_order('PHILIPS_A', price=mid_price, volume=volume, side='bid', order_type='limit')
                    #print(f"Order Id: {result} 8 A-bid")
                    
                    result = e.insert_order('PHILIPS_A', price=round(mid_price,3), volume=volume, side='bid', order_type='limit')
                    #result = e.insert_order('PHILIPS_A', price=round(price_A-.10,3), volume=volume, side='bid', order_type='limit')
                    
                    print(f"Order Id: {result} 4 A-ask")
                    
                    time.sleep(1)
    
                    get_info()
                
    except IndexError:
        pass
    if i % 100 == 0:
        print(int(100 * i / 10000), "% Done")




    

    
    time.sleep(0.2)

get_info()
