# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 01:07:09 2023

@author: Steven Ho
"""

import os
import time
import configparser
from pybit import usdc_perpetual

current_directory = os.path.dirname(os.path.abspath(__file__))
PATH_TEST_KEYS = os.path.join(current_directory, "keys", "bybit_keys_test.key") 
PATH_PRD_KEYS = os.path.join(current_directory, "keys", "bybit_keys_real.key") 

BASE_URL_TEST = 'https://api-testnet.bybit.com' # testnet base url
BASE_URL_PRD = 'https://api.bybit.com' # production base url

TRADE_QTY_ROUNDOFF = 3


class bybit_usdc_future:
        
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
                           
        self.session_unauth = usdc_perpetual.HTTP(endpoint = self.BASE_URL)        
        self.session_auth = usdc_perpetual.HTTP(endpoint=self.BASE_URL, api_key=self.PKEY, api_secret=self.SKEY)        
        return
    
    
    def __init__(self, testing):                
        self.set_test_env(testing) 
        
        
    def set_leverage(self, asset, leverage):    
        result = False
        response = {}        
        
        try:
            response = self.session_auth.set_leverage(symbol=asset, 
                                                      leverage=str(leverage))
            print(response)
            
            if ( 'retCode' in response ) and ( response['retCode'] == 0 ):
                result = True
        
        except Exception as e:            
            
            if 'ErrCode: 34036' in str(e):
                result = True
            else:
                print("bybit_usdc_future.setLeverage(), Exception = " + str(e))
                    
        return result, response
        
    
    def trade(self, asset, side, typ, price, quan, order_filter = 'Order', reduce_only=False, close_on_trigger=False):   
        
        result = False  
        response = {}
        orderId = ''
        
        try:
            response = self.session_auth.place_active_order(
                symbol = asset,
                orderType = typ,
                orderFilter = order_filter,
                side = side,
                orderPrice = str(price), 
                orderQty = str(quan),
                timeInForce='GoodTillCancel',
                reduceOnly = reduce_only,
                closeOnTrigger = close_on_trigger
            )
                                
            if ( 'retCode' in response ) and ( response['retCode'] == 0 ):
                orderId = response['result']['orderId']
                result = True
        
        except Exception as e:
            print("bybit_usdc_future.trade(), Exception = " + str(e))
        
        return result, response, orderId
    
    
    def get_price(self, asset):
        price = -1
        
        try:
            response = self.session_unauth.latest_information_for_symbol(symbol = asset)
            
            if ( 'retCode' in response ) and ( response['retCode'] == 0 ):
                price = response['result']['markPrice']
            
        except Exception as e:
            print("bybit_usdc_future.get_price(), Exception = " + str(e))            
        
        return float(price)
    
    
    def get_trade_quantity(self, asset, collateral, leverage):        
        price = self.get_price(asset)
        
        if price <= 0 :
            return -1
        
        trade_quantity = -1
        try:
            trade_quantity = round( (float(collateral)*float(leverage)/price ), TRADE_QTY_ROUNDOFF)
            
        except Exception as e:
            print("bybit_usdc_future.get_trade_quantity(), Exception = " + str(e))    
            
        return trade_quantity
    
    
    def short_token_usdc(self, symbol="BTC", leverage=5, collateral=100, order_type='Market'): 
        
        asset = symbol + 'PERP'
        trade_quantity = self.get_trade_quantity(asset, collateral, leverage)
        
        #set leverage
        leverage_result, leverage_response = self.set_leverage(asset, leverage)
            
        if not leverage_result:
            print("bybit_usdc_future.short_token_usdc(), leverage_result =" + str(leverage_result))
            return False, leverage_response, ''
                
        #short the asset
        return self.trade(asset, 'Sell', order_type, 0, trade_quantity)
    
    
    def long_token_usdc(self, symbol="BTC", leverage=5, collateral=100, order_type='Market'): 
        
        asset = symbol + 'PERP'
        trade_quantity = self.get_trade_quantity(asset, collateral, leverage)
        
        #set leverage
        leverage_result, leverage_response = self.set_leverage(asset, leverage)        
            
        if not leverage_result:
            print("bybit_usdc_future.long_token_usdc(), leverage_result =" + str(leverage_result))
            return False, leverage_response, ''
        
        #long the asset
        return self.trade(asset, 'Buy', order_type, 0, trade_quantity)   
    
    
    def my_position(self, **kwargs):
        
        suffix = "/option/usdc/openapi/private/v1/query-position"
        
        return self.session_auth._submit_request(
            method="POST",
            path=self.session_auth.endpoint + suffix,
            query=kwargs,
            auth=True
        )
    
    
    #position_id is not required as we cannot have both long and short positions for USDC futures
    def close_position(self, symbol="BTC", order_type='Market'):        
        
        asset = symbol + 'PERP'
        
        try:
            time.sleep(1) #sleep for 1 seond to ensure that we get the latest position
            
            position_response = self.session_auth.my_position(category = 'PERPETUAL', symbol = asset)
                    
            if ( 'retCode' in position_response ) and ( position_response['retCode'] == 0 ):
                positions = position_response['result']['dataList']
                
                for position in positions:
                    
                    if asset == position['symbol'] :
                        quantity = abs(float(position['size']))
                                                    
                        if 'Buy' == position['side']:
                            return self.trade(asset, 'Sell', order_type, 0, quantity, 'StopOrder', True, True)                        
                        else:
                            return self.trade(asset, 'Buy', order_type, 0, quantity, 'StopOrder', True, True)
                        
        except Exception as e:
            print("bybit_usdc_future.close_position(), Exception = " + str(e))                            
                            
        return False, {}, ''
    
if __name__ == '__main__':
    
    #============================== Future ======================================
    
    myBybitUsdcFut = bybit_usdc_future(testing=True) #testnet
    #myBybitFut = bybit_usdc_future(testing=False) #real    
            
    # short USDC future
    result, response, orderId = myBybitUsdcFut.short_token_usdc('APE', 5, 100, order_type='Market')
    print("short_token_usdc, result = " + str(result))
    
    # long USDC future
    result, response, orderId = myBybitUsdcFut.long_token_usdc('APE', 5, 200, order_type='Market')
    print("long_token_usdc, result = " + str(result))
        
    # close position
    result, response, orderId = myBybitUsdcFut.close_position(symbol='APE', order_type='Market')
    print("close_position, result = " + str(result))
    
    
    
    


        