import ccxt
import time
import asyncio
import numpy as np
from ccxt.async_support import binance

# API klíče (zajisti si vlastní)
API_KEY = "fCrP4X88k0NAfikTteXatayUg66giapKtwxRF93SiItnejmsNSbmmNkFFE4KISzx"
API_SECRET = "meMrbPxn2aB6X5yfH9SKDEtSPChpiuAHHgyZnkkQfu4Sru7GVXhhPF4TBuaH8Wfu"

# Připojení k Binance
exchange = binance({
    'apiKey': API_KEY,
    'secret': API_SECRET,
    'enableRateLimit': True,
    'options': {
        'defaultType': 'spot',
    },
})

# Maximální počet trojúhelníkových arbitrážních párů
TRIANGULAR_PAIRS = [
    ('BTC/USDT', 'ETH/BTC', 'ETH/USDT'),
    ('BNB/USDT', 'BNB/BTC', 'BTC/USDT'),
    ('ADA/USDT', 'ADA/ETH', 'ETH/USDT'),
    ('XRP/USDT', 'XRP/BTC', 'BTC/USDT'),
    ('LTC/USDT', 'LTC/ETH', 'ETH/USDT'),
    ('DOGE/USDT', 'DOGE/BTC', 'BTC/USDT'),
    ('DOT/USDT', 'DOT/ETH', 'ETH/USDT'),
    ('MATIC/USDT', 'MATIC/BTC', 'BTC/USDT'),
    ('AVAX/USDT', 'AVAX/ETH', 'ETH/USDT'),
    ('SOL/USDT', 'SOL/BTC', 'BTC/USDT'),
    ('LINK/USDT', 'LINK/ETH', 'ETH/USDT'),
    ('UNI/USDT', 'UNI/BTC', 'BTC/USDT'),
    ('FTM/USDT', 'FTM/ETH', 'ETH/USDT'),
    ('TRX/USDT', 'TRX/BTC', 'BTC/USDT'),
    ('NEAR/USDT', 'NEAR/ETH', 'ETH/USDT')
]

async def fetch_prices():
    """ Získání cen v reálném čase """
    while True:
        try:
            tickers = await exchange.fetch_tickers()
            return tickers
        except Exception as e:
            print(f"Chyba při načítání cen: {e}")
            await asyncio.sleep(1)

async def find_arbitrage_opportunity():
    """ Hledání trojúhelníkové arbitráže s nejlepším poměrem zisku """
    while True:
        tickers = await fetch_prices()
        best_opportunity = None
        best_profit = 0
        
        for pair1, pair2, pair3 in TRIANGULAR_PAIRS:
            try:
                price1 = tickers[pair1]['bid']
                price2 = tickers[pair2]['bid']
                price3 = tickers[pair3]['ask']
                
                # Výpočet arbitrážní příležitosti
                profit = (1 / price1) * price2 * price3 - 1
                
                if profit > best_profit:
                    best_profit = profit
                    best_opportunity = (pair1, pair2, pair3)
            except Exception as e:
                print(f"Chyba ve výpočtu: {e}")
        
        if best_opportunity and best_profit > 0.002:  # 0.2% profit threshold
            print(f"Nejlepší arbitrážní příležitost: {best_opportunity} s profitem {best_profit:.4f}")
            await execute_trade(*best_opportunity)
        
        await asyncio.sleep(1)

async def execute_trade(pair1, pair2, pair3):
    """ Exekuce arbitrážních obchodů """
    try:
        amount = 0.01  # Množství pro obchod (upravit dle kapitálu)
        
        order1 = await exchange.create_market_buy_order(pair1, amount)
        order2 = await exchange.create_market_sell_order(pair2, amount)
        order3 = await exchange.create_market_sell_order(pair3, amount)
        
        print("Obchody provedeny:", order1, order2, order3)
    except Exception as e:
        print(f"Chyba při exekuci: {e}")

async def main():
    await find_arbitrage_opportunity()

# Spuštění bota
if __name__ == "__main__":
    asyncio.run(main())

