import ccxt
import time

# Configura la API (falsas por ahora, después puedes cambiar)
exchange = ccxt.coinex({
    'apiKey': '42559D64746449C8978421D015A32C4A',
    'secret': 'B9B24D590D56C366086E058D7ECDE4A88267C27314D23010',
    'enableRateLimit': True,
})

symbol = 'BTC/USDT'   # par de trading
usdt_amount = 10       # capital inicial
take_profit = 1.01     # +1% de ganancia
stop_loss = 0.98       # -2% máximo de pérdida

buy_price = None
btc_amount = None

while True:
    try:
        ticker = exchange.fetch_ticker(symbol)
        price = ticker['last']

        # Comprar si no hay posición abierta
        if buy_price is None:
            btc_amount = usdt_amount / price
            exchange.create_market_buy_order(symbol, btc_amount)
            buy_price = price
            print(f'Comprado a {buy_price}')

        # Revisar si vender por ganancia o stop loss
        else:
            if price >= buy_price * take_profit:
                exchange.create_market_sell_order(symbol, btc_amount)
                print('Vendido con ganancia')
                buy_price = None

            elif price <= buy_price * stop_loss:
                exchange.create_market_sell_order(symbol, btc_amount)
                print('Stop loss activado')
                buy_price = None

        time.sleep(300)  # espera 5 minutos

    except Exception as e:
        print('Error:', e)
        time.sleep(60)
