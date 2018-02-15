import discord
from discord.ext import commands
from cryptocompare_helper import *
from coinmarketcap_helper import *
from tradingview_helper import *
from secret import DISCORD_KEY

'''
    TODO:
        -color of Embed should depends on price change
        -catch some more errors
'''
SYMBOL_UP=u"\u25B2"
SYMBOL_DOWN=u"\u25BD"

client = discord.Client()

def getToCoin(args):
    if len(args.split("/")) == 2:
        return args.upper().split("/")[1:]
    else:
        return ['BTC', 'USD', 'ETH']
    
def getFromCoin(args):
    if len(args.split("/")) == 2:
        fromCoin = args.upper().split("/")[0]
    else:
        fromCoin = args.upper()
    return coinToSymbol(fromCoin)

def getExchange(args):
    if len(args) == 2:
        exchange = args[1]
    else:
        exchange = "CCCAGG"
    return exchange

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return
    #print("{} server={} channel={} user={} massage={}".format(message.timestamp, message.server, message.channel, message.author.name, message.content))
    if message.content.startswith('!help'):
        em = discord.Embed(title="Help", colour=0xFFFFFF)
        em.add_field(name="!list exchanges", value="show all possible exchanges.", inline=False)
        em.add_field(name="!list coins", value="show all possible coins.\n!VERY LONG ANSWER!", inline=False)
        em.add_field(name="!<COIN>", value="show a short, text based price info for the given coin. \nUse cryptocompare as data source\nExample: !LTC\n", inline=False)
        em.add_field(name="!<COIN> <EXCHANGE>", value="show a short, text based price info for the given coin. \nUse given exchange as data source\nExample: !LTC bittrex\n", inline=False)
        em.add_field(name="!!<COIN>", value="more details price info for the given coin. \nUse cryptocompare as data source\n  Example: !!LTC\n", inline=False)
        em.add_field(name="!!<COIN> <EXCHANGE>", value="more details price info for the given coin. \nUse given exchange as data source\nExample: !!LTC bittrex\n", inline=False)
        em.add_field(name="!!!<COIN>", value="full details price info for the given coin. \nUse cryptocompare as data source\n  Example: !!!LTC\n", inline=False)
        em.add_field(name="!!!<COIN> <EXCHANGE>", value="full details price info for the given coin. \nUse given exchange as data source\nExample: !!!LTC bittrex\n", inline=False)
        em.add_field(name="!!!!<COIN>", value="Technical analyses taken from tradingview.com\nExample: !!!!BTC/USD\n", inline=False)
        em.add_field(name="Details COINS", value="A coin can be a simple coin like, BTC or LTC. You can also pass the coinname like bitcoin.\nBy default we answer the price for BTC, ETH and USD\nIf you want the answer for a coin pair like BTC/ETC, then you use a coinpair as COIN", inline=False)
        em.add_field(name="Details EXCHANGE", value="@bittrex means that the price was taken from the exchange bittrex. If the coinpair is not listed at the given exchange, then CCCAGG will be taken.\nCCCAGG stands for CCCAGG = CryptoCompare Current Aggregate.\n", inline=False)        
        
        await client.send_message(message.author, embed=em)
    elif message.content.startswith('!list coins'):
        msg = "we support the following coins:\n"
        await client.send_message(message.author, msg)
        generator = (i for i in getAllCoins())
        head = list(next(generator) for _ in range(300))
        while len(head) > 0:
            msg = ", ".join(head)
            head = list(next(generator) for _ in range(300))
            await client.send_message(message.author, msg)

    elif message.content.startswith('!list exchanges'):
        await client.send_message(message.author, "we support the following exchanges:\n" + ", ".join(getAllExchanges()))
    elif message.content.startswith('!!!!'):
        args = message.content.replace("!!!!", "").strip().split(" ")
        fromCoin = getFromCoin(args[0])
        toCoin = getToCoin(args[0])
        for x in toCoin:
            if fromCoin == x:
                continue
            url = gettechnicalsUrl(fromCoin,x)
            await client.send_message(message.channel, "\n\nwait for technical analyses for "+fromCoin+"/"+x+" taken from <"+url+">")
            try:
                gettechnicals(fromCoin,x)
                await client.send_file(message.channel, 'tech.jpg')
            except:
                await client.send_message(message.author, "sorry i can't find a technical analyses for "+fromCoin+"/"+x+" on tradingview.com")
    elif message.content.startswith('!!!'):
        args = message.content.replace("!!!", "").strip().split(" ")
        fromCoin = getFromCoin(args[0])
        toCoin = getToCoin(args[0])
        exchange = getExchange(args)
        try:    
            thumbnail_url, info_url, coinid, fullname, score = getCoinInfo(fromCoin)        
        except:
            thumbnail_url, info_url, coinid, fullname, score = getCoinInfoCC(fromCoin)
        em = discord.Embed(title="Price " + fromCoin, colour=0xFF0000)
        em.set_thumbnail(url=thumbnail_url)
        for x in toCoin:
            if fromCoin == x:
                continue
            try:
                price_now, diff_h, diff_d, diff_7d, ex =  getCoin(fromCoin, x, exchange=exchange)
            except:
                try:
                    price_now, diff_h, diff_d, diff_7d, ex =  getCoinCC(fromCoin, x)
                except:
                    await client.send_message(message.author, "invalid or unknown coin pair "+fromCoin+"/"+x)
                    continue
            symbol_h = SYMBOL_DOWN if diff_h < 0 else SYMBOL_UP
            symbol_d = SYMBOL_DOWN if diff_d < 0 else SYMBOL_UP
            symbol_7d = SYMBOL_DOWN if diff_7d < 0 else SYMBOL_UP
            msg = "{0:5.8f} @ {1} \n{2}\nRank {3}".format(price_now, ex, fullname, score)
            em.add_field(name=fromCoin+"/"+x, value=msg, inline=True)
            msg = "1h={0:8.2f}% {1} \n1d={2:8.2f}% {3} \n7d={4:8.2f}% {5}".format(diff_h, symbol_h, diff_d, symbol_d, diff_7d, symbol_7d)
            em.add_field(name="Changes", value=msg, inline=True)
            em.set_footer(text="use !help for more infos")
        if len(em.fields):
            await client.send_message(message.channel, embed=em)
    elif message.content.startswith('!!'):
        args = message.content.replace("!!", "").strip().split(" ")
        fromCoin = getFromCoin(args[0])
        toCoin = getToCoin(args[0])
        exchange = getExchange(args)

        em = discord.Embed(title="Price " + fromCoin, colour=0xFF0000)
        for x in toCoin:
            if fromCoin == x:
                continue
            try:
                price_now, diff_h, diff_d, diff_7d, ex =  getCoin(fromCoin, x, exchange=exchange)
            except:
                try:
                    price_now, diff_h, diff_d, diff_7d, ex =  getCoinCC(fromCoin, x)
                except:
                    await client.send_message(message.author, "invalid or unknown coin pair "+fromCoin+"/"+x)
                    continue
                    
            symbol_h = SYMBOL_DOWN if diff_h < 0 else SYMBOL_UP
            symbol_d = SYMBOL_DOWN if diff_d < 0 else SYMBOL_UP
            symbol_7d = SYMBOL_DOWN if diff_7d < 0 else SYMBOL_UP
            msg = "{0:5.8f} @ {1} \n".format(price_now, ex)
            em.add_field(name=fromCoin+"/"+x, value=msg, inline=True)
            msg = "1h={0:8.2f}% {1} 1d={2:8.2f}% {3} 7d={4:8.2f}% {5}\n".format(diff_h, symbol_h, diff_d, symbol_d, diff_7d, symbol_7d)
            em.add_field(name="Changes", value=msg, inline=True)
        em.set_footer(text="use !help for more infos")
        if len(em.fields):
            await client.send_message(message.channel, embed=em)
    elif message.content.startswith('!'):
        args = message.content.replace("!", "").strip().split(" ")
        fromCoin = getFromCoin(args[0])
        toCoin = getToCoin(args[0])
        exchange = getExchange(args)
        msg = ""
        em = discord.Embed(colour=0xFF0000)
                    
        for x in toCoin:
            if fromCoin == x:
                continue
            try:
                price_now, diff_h, diff_d, diff_7d, ex =  getCoin(fromCoin, x, exchange=exchange)
            except:
                try:
                    price_now, diff_h, diff_d, diff_7d, ex =  getCoinCC(fromCoin, x)
                except:
                    await client.send_message(message.author, "invalid or unknown coin pair "+fromCoin+"/"+x)
                    continue
            msg += "{0}/{1} {2:5.8f} 1h={3:8.2f}% 1d={4:8.2f}% 7d={5:8.2f}% @{6}\n".format(fromCoin, x, price_now, diff_h, diff_d, diff_7d, ex)
        if len(msg):
            em.add_field(name="Price", value=msg, inline=True)
            em.set_footer(text="use !help for more infos")
            await client.send_message(message.channel, embed=em)
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    await client.change_presence(game=discord.Game(name='!help for Help'))

client.run(DISCORD_KEY)
