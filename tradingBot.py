import os
import jwt
import uuid
import hashlib
import json
import keyboard
import time

import userInfo
import printFunctions as PF 
import chartFunctions as CF 
import tradeFunctions as TF 
import walletFunctions as WF 
from makeToken import makeToken 

from urllib.parse import urlencode

import requests

def getAccountInfo():
	infos = userInfo.getUserInfo()
	print("Available accounts are below: ")
	for i in infos:
		print(i,end = "  ")
	user = input("\nWhich account you want to use? ")
	userinfo = infos[user]
	access_key = userinfo['access_key']
	secret_key = userinfo['secret_key']
	return (access_key, secret_key)


if __name__ == "__main__":
	userInfo.saveUserInfo()	
	(access_key, secret_key) = getAccountInfo()
	server_url = 'https://api.upbit.com'
	while True:
		PF.printMenu()
		selected = input('').lower()
		if selected == 'wallet':
			WF.walletInfo(access_key, secret_key)
		elif selected == 'allmarkets':
			url = "https://api.upbit.com/v1/market/all"
			querystring = {"isDetails":"false"}
			res = requests.request("GET", url, params=querystring).json()
			for item in res:
				if item['market'][:3] == 'KRW':
					PF.printJson(item)
		elif selected == 'buy':
			print("Not yet")
		elif selected == 'sell':
			print("Not yet")
		elif selected == 'market':
			print("Not yet")

		elif selected == 'autotrade':
			market = input("Which market do you want to trade? ")
			market = 'KRW-'+market
			print("You selected ", market)
			while True:
				TF.MACross(market,'15min', 15, 50, access_key, secret_key)
				time.sleep(800)

		elif selected == 'updateaccount':
			(access_key, secret_key) = getAccountInfo()
			print('Update done.\n')
			continue

		elif selected == 'quit':
			print("Exit the program.")
			break

		else: 
			print("Invalid request")

		input("Press Enter to continue...")

	# rfr_order_query = {
	# 	'market': 'KRW-RFR',
	# 	'side': 'ask',
	# 	'volume': '100',
	# 	'price': '100.0',
	# 	'ord_type': 'limit',
	# }
	# headers = makeToken(access_key, secret_key, rfr_order_query)
	#res_ordered = requests.post(server_url + "/v1/orders", params=rfr_order_query, headers=headers)
	#printJson(res_ordered.json())
	#RFR_PRICE = get_price_info('KRW-RFR', '15min', 100)
	#crossed(RFR_PRICE, 15, 50)
