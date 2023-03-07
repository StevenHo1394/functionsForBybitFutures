# functionsForBybitFutures

(A) We create three functions to trade futures on Bybit as follows:

1) short_token_usdt(symbol="BTC", leverage=5, collateral=100, order_type="market")
2) long_token_usdt(symbol="BTC", leverage=5, collateral=100, order_type="market")
3) close_position(position_id="ABC", "market")

(B) Usage:

1) Please input your testnet API keys to "keys/bybit_keys_test.key", and your real API keys to "bybit_keys_real.key".
2) Create your bybitFut instance by "bybit_future(testing=True)" if running on testnet, or "bybit_future(testing=False)" if running for real.
3) Just call the functions from the bybitFut instance.

