from bs4 import BeautifulSoup
import requests

def getAth(coinname):
    try:
        name = coinname.split(" ")[0].lower()
        url = "https://athcoinindex.com/currencies/%s"%name
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')
        ath = soup.find_all('h4')[0].get_text()
        change = soup.find_all('small')[1].get_text()
        return ath, change
    except:
         raise ValueError('coin is not listed at athcoinindex ' + name)

