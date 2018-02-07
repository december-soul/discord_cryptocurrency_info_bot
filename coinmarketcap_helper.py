from pymarketcap import Pymarketcap

coinmarketcap = Pymarketcap()



def getCoinInfoCC(coin):
    try:
        coininfo = coinmarketcap.ticker(coin)
        return "https://files.coinmarketcap.com/static/img/coins/64x64/"+coininfo['id']+".png", "", coininfo['id'], coininfo['name'], coininfo['rank']
    except:
        return "https://ornashine.com/wp-content/uploads/2016/08/GOLD-COIN-BACK1-AND-2-GRM.jpg", "", 0, coin, -1


def getAllCoinsCC():
    return coinmarketcap.symbols

def getAllExchangesCC():
    return []

def getCoinCC(from_coin, to_coin='USD', exchange='coinmarketcup'):
    from_coin = from_coin.upper()
    to_coin = to_coin.lower()
    info = coinmarketcap.ticker(from_coin, convert="ETH")
    try:
        price_now=info["price_"+to_coin]
        price_hour=info['percent_change_1h']
        price_day=info['percent_change_24h']
        price_7days=info['percent_change_7d']
        return (price_now, price_hour, price_day, price_7days, exchange)
    except Exception as inst:
        raise ValueError('Invalid coin pair ' + from_coin + "/" + to_coin)
