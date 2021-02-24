import time
import chartFunctions as CF 
import walletFunctions as WF 
import printFunctions as PF 
from makeToken import makeToken 
import requests


def buyMarketQuery(market, order_price):
 	return { 'market': market, 'side': 'bid', 'price': str(order_price), 'ord_type': 'price',  }
def sellMarketQuery(market, volume):
	return { 'market': market, 'side': 'ask', 'volume': str(volume),     'ord_type': 'market', }

def buy_all(access_key, secret_key, market) :
	marketInfo = WF.marketValidInfo(access_key,secret_key,market)['bid_account']
	walletKRW = float(marketInfo['balance'])
	query = buyMarketQuery(market, int(0.99 * walletKRW))
	headers = makeToken(access_key,secret_key,query)
	res = requests.post('https://api.upbit.com/v1/orders', params=query, headers=headers).json()
	PF.printJson(res)
	
def sell_all(access_key, secret_key, market) :
	marketInfo = WF.marketValidInfo(access_key,secret_key,market)['ask_account']
	volume = float(marketInfo['balance'])
	query = buyMarketQuery(market, int(0.99 * volume))
	headers = makeToken(access_key,secret_key,query)
	res = requests.post('https://api.upbit.com/v1/orders', params=query, headers=headers).json()
	PF.printJson(res)

def MACross(market: str, minute: str, shortMA: int, longMA: int, access_key, secret_key):
	price = CF.getPriceInfo(market, minute, longMA+10)
	cross = CF.crossed(price, shortMA, longMA)


	sell_all(access_key, secret_key, market)
	
	
	if cross == 1: # buy
		print("Upward cross! Buy.")
		buy_all(access_key, secret_key, market)
	elif cross == -1 : #sell
		print("Downward cross! Sell.")
		sell_all(access_key, secret_key, market)
	else:
		None