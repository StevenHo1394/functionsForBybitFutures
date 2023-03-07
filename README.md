# functionsForBybitFutures

(A) We will create three functions as follows:

short_token_usdt(symbol="BTC", leverage=5, collateral=100, order_type="market")

long_token_usdt(symbol="BTC", leverage=5, collateral=100, order_type="market")

close_position(position_id="ABC", "market")

(B) Usage:

1) Please input your testnet API keys to "keys/bybit_keys_test.key", and your real API keys to "bybit_keys_real.key".
2) Create your myBybitFut instance by "bybit_future(testing=True)" if running on testnet, or "bybit_future(testing=False)" if running for real.
3) Just call the functions from the myBybitFut instance.

