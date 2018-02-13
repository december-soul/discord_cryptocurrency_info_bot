import imgkit




def gettechnicals(fromcoin, tocoin):
    print("download tech")
    options = { 'crop-y': '612', 'crop-h': '620', 'javascript-delay': 1100 }
    try:
        img = imgkit.from_url("https://en.tradingview.com/symbols/"+fromcoin+tocoin+"/technicals/", "tech.jpg", options=options)
    except:
        raise ValueError('Invalid coin info for ' + fromcoin+tocoin)
    
