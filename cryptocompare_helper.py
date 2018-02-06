from crycompare import *
import json
import time
import sys

p = Price()
h = History()

exchanges = ['Cryptsy', 'BTCChina', 'Bitstamp', 'BTER', 'OKCoin', 'Coinbase', 'Poloniex', 'Cexio', 'BTCE', 'BitTrex', 'Kraken', 'Bitfinex', 'Yacuna', 'LocalBitcoins', 'Yunbi', 'itBit', 'HitBTC', 'btcXchange', 'BTC38', 'Coinfloor', 'Huobi', 'CCCAGG', 'LakeBTC', 'ANXBTC', 'Bit2C', 'Coinsetter', 'CCEX', 'Coinse', 'MonetaGo', 'Gatecoin', 'Gemini', 'CCEDK', 'Cryptopia', 'Exmo', 'Yobit', 'Korbit', 'BitBay', 'BTCMarkets', 'Coincheck', 'QuadrigaCX', 'BitSquare', 'Vaultoro', 'MercadoBitcoin', 'Bitso', 'Unocoin', 'BTCXIndia', 'Paymium', 'TheRockTrading', 'bitFlyer', 'Quoine', 'Luno', 'EtherDelta', 'bitFlyerFX', 'TuxExchange', 'CryptoX', 'Liqui', 'MtGox', 'BitMarket', 'LiveCoin', 'Coinone', 'Tidex', 'Bleutrade', 'EthexIndia', 'Bithumb', 'CHBTC', 'ViaBTC', 'Jubi', 'Zaif', 'Novaexchange', 'WavesDEX', 'Binance', 'Lykke', 'Remitano', 'Coinroom', 'Abucoins', 'BXinth', 'Gateio', 'HuobiPro', 'OKEX'] 


def help_coins(number1, number2):
    msg = "we support the following coins:\n"
    msg += ", ".join(getAllCoins()[number1:number2])
    return msg
    
def help_exchanges():
    msg = "we support the following exchanges:\n"
    msg += ", ".join(exchanges)
    return(msg)

def getCoinInfo(coin):
    coininfo = p.coinList()['Data'][coin]
    return "https://www.cryptocompare.com"+coininfo['ImageUrl'], "https://www.cryptocompare.com"+coininfo['Url'], coininfo['Id'], coininfo['FullName'], coininfo['SortOrder']

def getAllCoins():
    return list(p.coinList()['Data'].keys())

def getAllExchanges():
    return exchanges

def diff(from_prise, to_prise):
    return 100/to_prise*from_prise-100


def getCoin(from_coin, to_coin='USD', exchange='CCCAGG', usefallback=True ):
        if exchange.upper() not in map(lambda x:x.upper(),exchanges):
                raise ValueError('unsupported exchange')
                #return("unsupported exchange")
        from_coin = from_coin.upper()
        timestamp_now = int(time.time())
        timestamp_hour = timestamp_now - 3600 # 1houre
        timestamp_day = timestamp_now - (60*60*24) # 1day
        timestamp_7days = timestamp_now - (60*60*24*7) # 7days
        try:
                price_now=p.price(from_coin, to_coin, e=exchange)[to_coin]
                #price_now=p.priceHistorical(from_coin, to_coin, exchange)[from_coin][to_coin]			
                price_hour=p.priceHistorical(from_coin, to_coin, exchange, ts=timestamp_hour)[from_coin][to_coin]
                price_day=p.priceHistorical(from_coin, to_coin, exchange, ts=timestamp_day)[from_coin][to_coin]
                price_7days=p.priceHistorical(from_coin, to_coin, exchange, ts=timestamp_7days)[from_coin][to_coin]
                return (price_now, diff(price_now, price_hour), diff(price_now, price_day), diff(price_now,price_7days), exchange)
                #print("{0}/{1} {2:5.8f}$ 1h={3:8.8f}$ 1d={4:8.8f}$ 7d={5:8.8f}$ @{6}".format(from_coin, to_coin, price_now, price_hour, price_day, price_7days, exchange))
                #msg += ("{0}/{1} {2:5.8f} 1h={3:8.2f}% 1d={4:8.2f}% 7d={5:8.2f}% @{6}\n".format(from_coin, to_coin, price_now, diff(price_now, price_hour), diff(price_now, price_day), diff(price_now,price_7days), exchange))
        except Exception as inst:
                #msg += ("invalid coin {0}/{1} at {2}: {3}, use fallback CCCAGG\n".format(from_coin, to_coin, exchange, inst))
                if usefallback:
                        return getCoin(from_coin, to_coin, usefallback=False) 
                else:
                        raise ValueError('Invalid coin pair ' + from_coin + "/" + to_coin)
                        #return (-1, -1, -1, -1, "unknown")#msg += ("invalid coin {0}/{1} at {2}: {3}\n".format(from_coin, to_coin, exchange, inst))
