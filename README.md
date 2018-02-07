# discord_cryptocurrency_info_bot


copy secret.py and insert your discord key
```
cp secret_example.py secret.py
vi secret.py
```

start bot
```
python3 bot.py
```

bot will listen to "!"
you should start with 
```
```

```
Help
!list exchanges
show all possible exchanges.
!list coins
show all possible coins.
!VERY LONG ANSWER!
!<COIN>
show a short, text based price info for the given coin. 
Use cryptocompare as data source
Example: !LTC
!<COIN> <EXCHANGE>
show a short, text based price info for the given coin. 
Use given exchange as data source
Example: !LTC bittrex
!!<COIN>
more details price info for the given coin. 
Use cryptocompare as data source
  Example: !!LTC
!!<COIN> <EXCHANGE>
more details price info for the given coin. 
Use given exchange as data source
Example: !!LTC bittrex
!!!<COIN>
full details price info for the given coin. 
Use cryptocompare as data source
  Example: !!!LTC
!!!<COIN> <EXCHANGE>
full details price info for the given coin. 
Use given exchange as data source
Example: !!!LTC bittrex
Details
@bittrex means that the price was taken from the exchange bittrex. If the coinpair is not listed at the given exchange, then CCCAGG will be taken.
CCCAGG stands for CCCAGG = CryptoCompare Current Aggregate.

As default we answer the price for BTC, ETH and USD
```
