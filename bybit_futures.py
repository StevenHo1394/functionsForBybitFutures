# -*- coding: utf-8 -*-
"""
Created on Mon Mar  6 16:01:57 2023

@author: Steven Ho
"""

import os
import configparser
from pybit import usdt_perpetual

current_directory = os.path.dirname(os.path.abspath(__file__))
PATH_TEST_KEYS = os.path.join(current_directory, "keys", "bybit_keys_test.key") 
PATH_PRD_KEYS = os.path.join(current_directory, "keys", "bybit_keys_real.key") 

BASE_URL_TEST = 'https://api-testnet.bybit.com' # testnet base url
BASE_URL_PRD = 'https://api.bybit.com' # production base url

TRADE_QTY_ROUNDOFF = 3

class bybit_future:
        
    def set_test_env(self, testing=True):
        
        config = configparser.ConfigParser()
                
        if (testing):            
            config.read(PATH_TEST_KEYS)            
            self.PKEY = config['details']['PKEY_F']
            self.SKEY = config['details']['SKEY_F']
            self.BASE_URL = BASE_URL_TEST
            
        else:
            config.read(PATH_PRD_KEYS)             
            self.PKEY = config['details']['PKEY_F']
            self.SKEY = config['details']['SKEY_F']
            self.BASE_URL = BASE_URL_PRD
                           
        self.session_unauth = usdt_perpetual.HTTP(endpoint = self.BASE_URL)        
        self.session_auth = usdt_perpetual.HTTP(endpoint=self.BASE_URL, api_key=self.PKEY, api_secret=self.SKEY)        
        return
    
    def __init__(self, testing):                
        self.set_test_env(testing) 

    
    def set_leverage(self, asset, leverage):    
        result = False
        response = {}        
        
        try:
            response = self.session_auth.set_leverage(symbol=asset, 
                                                      buy_leverage=int(leverage), 
                                                      sell_leverage=int(leverage))
            
            if ( 'ret_code' in response ) and ( response['ret_code'] == 0 ):
                result = True
        
        except Exception as e:
            print("bybit_future.setLeverage(), Exception = " + str(e))
            
            if 'leverage not modified' or 'ErrCode: 34036' in response:
                print("bybit_future.setLeverage(), leverage not modified!")
                result = True
                    
        return result, response
    
    def trade(self, asset, side, typ, price, quan):   
        
        result = False  
        response = {}
        orderId = ''
        
        try:
            response = self.session_auth.place_active_order(
                symbol = asset,
                side = side,
                order_type = typ,
                qty = quan,
                price = price,
                time_in_force="GoodTillCancel",
                reduce_only=False,
                close_on_trigger=False
            )
                    
            if ( response['ret_code'] == 0 ) and ( response['ext_code'] == "" ):
                result = True
                orderId = response['result']['order_id']
                print("bybit_future.trade(), response = " + str(response) )
        
        except Exception as e:
            print("bybit_future.trade(), Exception = " + str(e))
        
        return result, response, orderId
    
    def get_price(self, asset):
        price = -1
        
        try:
            response = self.session_unauth.public_trading_records(symbol=asset, limit = 1)
            
            if ( 'ret_code' in response ) and ( response['ret_code'] == 0 ):
                price = response['result'][0]['price']
            
        except Exception as e:
            print("bybit_future.get_price(), Exception = " + str(e))            
        
        return float(price)
    
    def get_trade_quantity(self, asset, collateral, leverage):        
        price = self.get_price(asset)
        
        if price <= 0 :
            return -1
        
        trade_quantity = -1
        try:
            trade_quantity = round( (float(collateral)*float(leverage)/price ), TRADE_QTY_ROUNDOFF)
            
        except Exception as e:
            print("bybit_future.get_trade_quantity(), Exception = " + str(e))    
            
        return trade_quantity
        

     #added the parm "order_price" in case of limit orders
    def short_token_usdt(self, symbol="BTC", leverage=5, collateral=100, order_type='Market', order_price=0): 
        
        asset = symbol + 'USDT'
        trade_quantity = self.get_trade_quantity(asset, collateral, leverage)
        
        #set leverage
        leverage_result, leverage_response = self.set_leverage(asset, leverage)
        print("leverage_result=" + str(leverage_result))
            
        if not leverage_result:
            return False, leverage_response, ''
                
        #short the asset
        return self.trade(asset, 'Sell', order_type, order_price, trade_quantity)
        

    #fixme: incomplete
    # def long_token_usdt(self, symbol="BTC", leverage=5, collateral=100, order_type='Market', order_price=0): 
        
    #     asset = symbol + 'USDT'
    #     trade_quantity = self.get_trade_quantity(asset, collateral, leverage)
        
    #     return
    
    # #fixme: incomplete
    # def close_position(self, position_id="ABC", order_type='Market', order_price=0):
    #     return

if __name__ == '__main__':
    
    #============================== Future ======================================
    
    myBybitFut = bybit_future(testing=True) #testnet
    #myBybitFut = bybit_future(testing=False) #real
            
    #get price
    # result = myBybitFut.get_price('BTCUSDT')
    # print(result)
    
    #set leverage
    # result, response = myBybitFut.set_leverage('BTCUSDT', 5)
    # print(result)
    
    #get trade quantity
    # result = myBybitFut.get_trade_quantity('BTCUSDT', 100, 5)
    # print(result)
    
    #short future
    # result, response, orderId = myBybitFut.short_token_usdt('BTC', 5, 100, order_type='Market')
    # print(result)
    # print(orderId)
    
    print('finished')
    
    


