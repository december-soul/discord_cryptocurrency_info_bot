from crycompare import *
import json
import time
import sys
import datetime

p = Price()
h = History()

exchanges = ['Cryptsy', 'BTCChina', 'Bitstamp', 'BTER', 'OKCoin', 'Coinbase', 'Poloniex', 'Cexio', 'BTCE', 'BitTrex', 'Kraken', 'Bitfinex', 'Yacuna', 'LocalBitcoins', 'Yunbi', 'itBit', 'HitBTC', 'btcXchange', 'BTC38', 'Coinfloor', 'Huobi', 'CCCAGG', 'LakeBTC', 'ANXBTC', 'Bit2C', 'Coinsetter', 'CCEX', 'Coinse', 'MonetaGo', 'Gatecoin', 'Gemini', 'CCEDK', 'Cryptopia', 'Exmo', 'Yobit', 'Korbit', 'BitBay', 'BTCMarkets', 'Coincheck', 'QuadrigaCX', 'BitSquare', 'Vaultoro', 'MercadoBitcoin', 'Bitso', 'Unocoin', 'BTCXIndia', 'Paymium', 'TheRockTrading', 'bitFlyer', 'Quoine', 'Luno', 'EtherDelta', 'bitFlyerFX', 'TuxExchange', 'CryptoX', 'Liqui', 'MtGox', 'BitMarket', 'LiveCoin', 'Coinone', 'Tidex', 'Bleutrade', 'EthexIndia', 'Bithumb', 'CHBTC', 'ViaBTC', 'Jubi', 'Zaif', 'Novaexchange', 'WavesDEX', 'Binance', 'Lykke', 'Remitano', 'Coinroom', 'Abucoins', 'BXinth', 'Gateio', 'HuobiPro', 'OKEX', 'coinmakretcap']  #coimmakretcap is not true, be this will work

def getCoinInfo(coin):
    try:
        coininfo = p.coinList()['Data'][coin]
        return "https://www.cryptocompare.com"+coininfo['ImageUrl'], "https://www.cryptocompare.com"+coininfo['Url'], coininfo['Id'], coininfo['FullName'], coininfo['SortOrder']
    except:
        raise ValueError('Invalid coin info for ' + coin)

def getAllCoins():
    return list(p.coinList()['Data'].keys())

def getAllExchanges():
    return exchanges

def diff(from_prise, to_prise):
    return 100/to_prise*from_prise-100

def getCoin(from_coin, to_coin='USD', exchange='CCCAGG', usefallback=True ):
        if exchange.upper() not in map(lambda x:x.upper(),exchanges):
                raise ValueError('unsupported exchange')
        from_coin = from_coin.upper()
        timestamp_now = int(time.time())
        timestamp_hour = timestamp_now - 3600 # 1houre
        timestamp_day = timestamp_now - (60*60*24) # 1day
        timestamp_7days = timestamp_now - (60*60*24*7) +500 # 7days (we need to cheat a littel because crycompare hold the date only for 7 days)
        try:
                price_now=p.price(from_coin, to_coin, e=exchange)[to_coin]
                #print( "{0} now {1}/{2} {3:5.8f} @{4}".format(datetime.datetime.fromtimestamp( int(timestamp_now) ).strftime('%Y-%m-%d %H:%M:%S'), from_coin, to_coin, price_now, exchange))
                price_hour=h.histoMinute(from_coin,to_coin, e=exchange, limit=1, toTs=timestamp_hour)['Data'][0]['close']
                #print( "{0} 1h  {1}/{2} {3:5.8f} @{4}".format(datetime.datetime.fromtimestamp( int(timestamp_hour) ).strftime('%Y-%m-%d %H:%M:%S'), from_coin, to_coin, price_hour, exchange))
                price_day=h.histoMinute(from_coin,to_coin, e=exchange, limit=1, toTs=timestamp_day)['Data'][0]['close']
                #print( "{0} 1d  {1}/{2} {3:5.8f} @{4}".format(datetime.datetime.fromtimestamp( int(timestamp_day) ).strftime('%Y-%m-%d %H:%M:%S'), from_coin, to_coin, price_day, exchange))
                price_7days=h.histoMinute(from_coin,to_coin, e=exchange, limit=1, toTs=timestamp_7days)['Data'][0]['close']
                #print( "{0} 7d  {1}/{2} {3:5.8f} @{4}".format(datetime.datetime.fromtimestamp( int(timestamp_7days) ).strftime('%Y-%m-%d %H:%M:%S'), from_coin, to_coin, price_7days, exchange))
                return (price_now, diff(price_now, price_hour), diff(price_now, price_day), diff(price_now,price_7days), exchange)

        except Exception as inst:
                if usefallback:
                        print(from_coin + "/" + to_coin +" not found at " + exchange + ", use fallback")
                        return getCoin(from_coin, to_coin, usefallback=False) 
                else:
                        raise ValueError('Invalid coin pair ' + from_coin + "/" + to_coin)
