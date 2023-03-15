# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 01:07:09 2023

@author: Steven Ho
"""

import os
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
            
            if ( 'ret_code' in response ) and ( response['ret_code'] == 0 ):
                result = True
        
        except Exception as e:
            print("bybit_usdc_future.setLeverage(), Exception = " + str(e))
            
            if 'ErrCode: 34036' in response:
                print("bybit_usdc_future.setLeverage(), leverage not modified!")
                result = True
                    
        return result, response
    
    def get_min_trade_qty(self, asset):
        minTradeQty = -1
        
        try:
            response = self.session_unauth.query_symbol(symbol=asset, limit = 1)
            
            if ( 'retCode' in response ) and ( response['retCode'] == 0 ):
                
                results = response['result']
                for result in results:
                    if asset == result['symbol']:
                        minTradeQty = response['result'][0]['minTradingQty']
                        break
            
        except Exception as e:
            print("bybit_usdc_future.get_min_trade_qty(), Exception = " + str(e))            
        
        return float(minTradeQty)
    
if __name__ == '__main__':
    
    #============================== Future ======================================
    
    myBybitUsdcFut = bybit_usdc_future(testing=True) #testnet
    #myBybitFut = bybit_usdc_future(testing=False) #real    
    
    # result = myBybitUsdcFut.get_min_trade_qty('BTCPERP')
    # print(result)
    
    result = myBybitUsdcFut.set_leverage('BTCPERP', 20)
    print(result)
    
    #fixme: incomplete
    #myBybitUsdcFut.trade('BTC-PERP', 'Sell', 'Market', 0, 0.001)

        