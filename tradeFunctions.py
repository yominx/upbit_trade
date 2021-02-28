import time
import chartFunctions as CF
import walletFunctions as WF
import printFunctions as PF
from makeToken import makeToken
import requests
import logger

THRESHOLD = 11000 #WON

def buyMarketQuery(market, order_price):
	return {
		"market": market,
		"side": "bid",
		"price": str(order_price),
		"ord_type": "price",
	}


def sellMarketQuery(market, volume):
	return {
		"market": market,
		"side": "ask",
		"volume": str(volume),
		"ord_type": "market",
	}


def buy_KRW(access_key, secret_key, market, KRW):
	current_price = CF.getCurrentPrice(market)
	marketInfo = WF.marketValidInfo(access_key, secret_key, market)
	volume = float(marketInfo["ask_account"]["balance"])
	if volume * current_price > THRESHOLD:
		return

	marketInfo = marketInfo["bid_account"]
	walletKRW = float(marketInfo["balance"])
	orderKRW = min(KRW, int(0.995 * walletKRW))
	query = buyMarketQuery(market, min(KRW, orderKRW))
	headers = makeToken(access_key, secret_key, query)
	res = requests.post(
		"https://api.upbit.com/v1/orders", params=query, headers=headers
	).json()
	PF.printJson(res)


def sell_all(access_key, secret_key, market):
    	
	current_price = CF.getCurrentPrice(market)
	marketInfo = WF.marketValidInfo(access_key, secret_key, market)["ask_account"]
	volume = float(marketInfo["balance"])
	if volume * current_price < THRESHOLD:
		return
		
	query = sellMarketQuery(market, float(volume))
	headers = makeToken(access_key, secret_key, query)
	res = requests.post(
		"https://api.upbit.com/v1/orders", params=query, headers=headers
	).json()
	PF.printJson(res)


def MACross(
	market: str,
	minute: str,
	shortMA: int,
	longMA: int,
	KRW: int,
	access_key,
	secret_key,
):
	price = CF.getPriceInfo(market, minute, longMA + 10)
	cross = CF.crossed(price, shortMA, longMA)

	if cross == 1:  # buy
		tradeInfo = "Buy" + market + "  " + str(KRW) + "WON"
		logger.logPrint(tradeInfo)
		buy_KRW(access_key, secret_key, market, KRW)
	elif cross == -1:  # sell
		tradeInfo = "Sell" + market + "  " + str(KRW) + "WON"
		logger.logPrint(tradeInfo)
		sell_all(access_key, secret_key, market)
	else:
		None


def tradeMarket(tradeMarketInfo, access_key, secret_key):
	for market in tradeMarketInfo:
		info = tradeMarketInfo[market]
		duration 	= info['time']
		shortTime 	= int(info['short'])
		longTime 	= int(info['long'])
		price 		= int(info['price'])
		#current_price = CF.getCurrentPrice(market)
		# logger.logPrint("check  " + market + "  " + str(current_price))

		time.sleep(1)
		MACross(market, duration, shortTime, longTime, price, access_key, secret_key)

def showOrderInfo(access_key, secret_key):
	query = {'state': 'wait',}
	headers = makeToken(access_key, secret_key)
	res = requests.get("https://api.upbit.com/v1/orders", params=query, headers=headers)
	PF.printJson(res.json())
