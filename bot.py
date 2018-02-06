import discord
from cryptocompare_helper import *
from secret import DISCORD_KEY

'''
    TODO:
        -color of Embed should depends on price change
        -if coin was not found via cryptocompare, then use coinmarketcap
        -allow to ask for XVG/BTC to define the to_coin
        -leading space ignore

'''
SYMBOL_UP=u"\u25B2"
SYMBOL_DOWN=u"\u25BD"

client = discord.Client()

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

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
        em.add_field(name="Details", value="@bittrex means that the price was taken from the exchange bittrex. If the coinpair is not listed at the given exchange, then CCCAGG will be taken.\nCCCAGG stands for CCCAGG = CryptoCompare Current Aggregate.\n\nAs default we answer the price for BTC, ETH and USD\n\n", inline=False)
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
    elif message.content.startswith('!!!'):
        args = message.content.replace("!!!", "").split(" ")
        if len(args) < 1:
            await client.send_message(message.channel, "missing coin")
            return
        coin = args[0].upper()
        if len(args) == 2:
            exchange = args[1]
        else:
            exchange = "CCCAGG"
        thumbnail_url, info_url, coinid, fullname, score = getCoinInfo(coin)
        em = discord.Embed(title="Price " + coin, colour=0xFF0000)
        #em.set_thumbnail(thumbnail_url)
        em.set_thumbnail(url=thumbnail_url)
        for x in ['BTC', 'USD', 'ETH']:
            try:
                price_now, diff_h, diff_d, diff_7d, ex =  getCoin(coin, x, exchange=exchange)
                symbol_h = SYMBOL_DOWN if diff_h < 0 else SYMBOL_UP
                symbol_d = SYMBOL_DOWN if diff_d < 0 else SYMBOL_UP
                symbol_7d = SYMBOL_DOWN if diff_7d < 0 else SYMBOL_UP
                msg = "{0:5.8f} @ {1}\n{2}\nRank {3}".format(price_now, ex, fullname, score)
                em.add_field(name=coin+"/"+x, value=msg, inline=True)
                msg = "1h={0:8.2f}% {1} \n1d={2:8.2f}% {3} \n7d={4:8.2f}% {5}".format(diff_h, symbol_h, diff_d, symbol_d, diff_7d, symbol_7d)
                em.add_field(name="Diff", value=msg, inline=True)
                em.set_footer(text="use !help for more infos")
            except Exception as inst:
                print("invalid coin pair "+coin+"/"+x)
        await client.send_message(message.channel, embed=em)
    elif message.content.startswith('!!'):
        args = message.content.replace("!!", "").split(" ")
        if len(args) < 1:
            await client.send_message(message.channel, "missing coin")
            return
        coin = args[0].upper()
        if len(args) == 2:
            exchange = args[1]
        else:
            exchange = "CCCAGG"

        em = discord.Embed(title="Price " + coin, colour=0xFF0000)
        for x in ['BTC', 'USD', 'ETH']:
            try:
                price_now, diff_h, diff_d, diff_7d, ex =  getCoin(coin, x, exchange=exchange)
                symbol_h = SYMBOL_DOWN if diff_h < 0 else SYMBOL_UP
                symbol_d = SYMBOL_DOWN if diff_d < 0 else SYMBOL_UP
                symbol_7d = SYMBOL_DOWN if diff_7d < 0 else SYMBOL_UP
                msg = "{0:5.8f} @ {1}\n".format(price_now, ex)
                em.add_field(name=coin+"/"+x, value=msg, inline=True)
                msg = "1h={0:8.2f}% {1} 1d={2:8.2f}% {3} 7d={4:8.2f}% {5}\n".format(diff_h, symbol_h, diff_d, symbol_d, diff_7d, symbol_7d)
                em.add_field(name="Diff", value=msg, inline=True)
            except Exception as inst:
                print("invalid coin pair "+coin+"/"+x)
        em.set_footer(text="use !help for more infos")
        await client.send_message(message.channel, embed=em)
    elif message.content.startswith('!'):
        args = message.content.replace("!", "").split(" ")
        coin = args[0].upper()
        msg = ""
        em = discord.Embed(colour=0xFF0000)
        if len(args) == 2:            
            for x in ['BTC', 'USD', 'ETH']:
                try:
                    price_now, diff_h, diff_d, diff_7d, ex =  getCoin(coin, x, exchange=args[1])
                    msg += "{0}/{1} {2:5.8f} 1h={3:8.2f}% 1d={4:8.2f}% 7d={5:8.2f}% @{6}\n".format(coin, x, price_now, diff_h, diff_d, diff_7d, ex)
                except:
                    pass
        else:
            for x in ['BTC', 'USD', 'ETH']:
                try:
                    price_now, diff_h, diff_d, diff_7d, ex =  getCoin(coin, x)
                    msg += "{0}/{1} {2:5.8f} 1h={3:8.2f}% 1d={4:8.2f}% 7d={5:8.2f}% @{6}\n".format(coin, x, price_now, diff_h, diff_d, diff_7d, ex)
                except:
                    pass
                
        em.add_field(name="Price", value=msg, inline=True)
        em.set_footer(text="use !help for more infos")
        await client.send_message(message.channel, embed=em)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(DISCORD_KEY)
