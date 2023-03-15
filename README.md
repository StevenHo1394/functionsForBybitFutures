# functionsForBybitFutures

Part1: USDT futures (bybit_futures.py)
======================================

(A) We create three functions to trade futures on Bybit as follows:

1) short_token_usdt(symbol="BTC", leverage=5, collateral=100, order_type="Market")
2) long_token_usdt(symbol="BTC", leverage=5, collateral=100, order_type="Market")
3) close_position(symbol="BTC", position_id="ABC", "Market") (c.f. part C below)

(B) Usage:

1) Please input your testnet API keys to "keys/bybit_keys_test.key", and your real API keys to "bybit_keys_real.key".
2) Create your bybitFut instance by "bybitFut = bybit_future(testing=True)" if running on testnet, or "bybitFut = bybit_future(testing=False)" if running for real.
3) Just call the functions from the bybitFut instance.

(C) Note

1) Added the new paramter symbol="BTC" in close_position(), as the position_id will be repeated for different symbols.

(D) The trade results on my bybit testnet account

![bybit_trade_samples](https://user-images.githubusercontent.com/75365123/223401584-738ca588-bf54-429b-9953-a5d498551fbd.png)

Part2: USDC futures (bybit_usdc_futures.py)
===========================================

(A) We create three functions to trade USDC futures on Bybit as follows:

1) short_token_usdt(symbol="BTC", leverage=5, collateral=100, order_type="Market")
2) long_token_usdt(symbol="BTC", leverage=5, collateral=100, order_type="Market")
3) close_position(symbol="BTC", position_id="ABC", "Market") 

Note: For 'BTC-PERP', the symbol name in API is 'BTCPERP'. This has been taken care of in the code already.
