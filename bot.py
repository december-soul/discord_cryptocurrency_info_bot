import discord
from cryptocompare_helper import *
from secret import DISCORD_KEY


client = discord.Client()

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content.startswith('!help'):
        msg = "call \n!list coins\n or \!list exchanges"
        await client.send_message(message.author, msg)
    elif message.content.startswith('!list coins'):
        await client.send_message(message.channel, help_coins(0,2000))
        await client.send_message(message.channel, help_coins(2000,4000))
        await client.send_message(message.channel, help_coins(4000,6000))
        await client.send_message(message.channel, help_coins(6000,8000))
        await client.send_message(message.channel, help_coins(8000,-1))
    elif message.content.startswith('!list exchanges'):
        await client.send_message(message.author, help_exchanges())
        #await client.send_message(message.channel, help_exchanges())
    elif message.content.startswith('!!!'):
        msg = 'Hello {0.author.mention} this will be a chart (maybe)'.format(message)
        #msg = coin(message.content.replace("!!!", ""))
        await client.send_message(message.channel, msg)
    elif message.content.startswith('!!'):
        msg = 'Hello {0.author.mention} this will be a long message'.format(message)
        #msg = coin(message.content.replace("!!", ""))
        await client.send_message(message.channel, msg)
    elif message.content.startswith('!'):
        #msg = 'Hello {0.author.mention} this will be a chart (maybe)'.format(message)
        args = message.content.replace("!", "").split(" ")
        if len(args) == 2:
            price_now, diff_h, diff_d, diff_7d, ex =  getCoin(args[0], "BTC", exchange=args[1])
            msg = "{0}/{1} {2:5.8f} 1h={3:8.2f}% 1d={4:8.2f}% 7d={5:8.2f}% @{6}\n".format(args[0], "BTC", price_now, diff_h, diff_d, diff_7d, ex)
            price_now, diff_h, diff_d, diff_7d, ex =  getCoin(args[0], "USD", exchange=args[1])
            msg += "{0}/{1} {2:5.8f} 1h={3:8.2f}% 1d={4:8.2f}% 7d={5:8.2f}% @{6}\n".format(args[0], "USD", price_now, diff_h, diff_d, diff_7d, ex)
        else:
            price_now, diff_h, diff_d, diff_7d, ex =  getCoin(args[0], "BTC")
            msg = "{0}/{1} {2:5.8f} 1h={3:8.2f}% 1d={4:8.2f}% 7d={5:8.2f}% @{6}\n".format(args[0], "BTC", price_now, diff_h, diff_d, diff_7d, ex)
            price_now, diff_h, diff_d, diff_7d, ex =  getCoin(args[0], "USD")
            msg += "{0}/{1} {2:5.8f} 1h={3:8.2f}% 1d={4:8.2f}% 7d={5:8.2f}% @{6}\n".format(args[0], "USD", price_now, diff_h, diff_d, diff_7d, ex)
            
        await client.send_message(message.channel, msg)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(DISCORD_KEY)
