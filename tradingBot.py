import os
import jwt
import uuid
import hashlib
import json

import userInfo
import makeToken 
import printFunctions as PF 
import chartFunctions as CF 
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

def check_wallet_net_input(access_key, secret_key):
	headers = makeToken.makeToken(access_key,secret_key)
	res = requests.get(server_url + "/v1/deposits", headers=headers).json()
	deposit = 0
	for tx in res:
		if tx['currency'] == 'KRW' and tx['state'] == 'ACCEPTED':
			deposit = deposit + float(tx['amount'])
	print('You deposited ', deposit, 'Won')

	headers = makeToken.makeToken(access_key,secret_key)
	res = requests.get(server_url + "/v1/withdraws", headers=headers).json()
	withdraw = 0
	for tx in res:
		if tx['currency'] == 'KRW' and tx['state'] == 'DONE':
			withdraw = withdraw + float(tx['amount'])
	print('You withdrawed ', withdraw, 'Won')
	print('Net input: you deposited ', (deposit-withdraw)/10000,'×10⁴ Won')


# def buy_market_query(market: str, order_price: int):
# 	return { 'market': market, 'side': 'bid', 'price': str(order_price), 'ord_type': 'price', }
# def sell_market_query(market: str, order_price: int):
# 	return { 'market': market, 'side': 'ask', 'volume': 10, 'ord_type': 'market', }


if __name__ == "__main__":
	userInfo.saveUserInfo()	
	(access_key, secret_key) = getAccountInfo()
	server_url = 'https://api.upbit.com'
	while True:
		PF.printMenu()

		selected = input('').lower()
		if selected == 'wallet':
			headers = makeToken.makeToken(access_key,secret_key)
			wallet_info = requests.get(server_url + "/v1/accounts", headers=headers).json()
			for elem in wallet_info:
				del elem['locked']
				del elem['avg_buy_price']
				del elem['avg_buy_price_modified']
				del elem['unit_currency']
			PF.printJson(wallet_info)

		elif selected == 'buy':
			print("Not yet")
		elif selected == 'sell':
			print("Not yet")
		elif selected == 'market':
			print("Not yet")

		elif selected == 'autotrade':
			print("Not yet")
			
		elif selected == 'quit':
			print("Exit the program.")
			break

		elif selected == 'updateaccount':
			print("Not yet")

		else: 
			print("Invalid request")

		input("Press Enter to continue...")


	query = {
		'market': 'KRW-RFR',
	}
	headers = makeToken.makeToken(access_key, secret_key, query)
	res_order_chance = requests.get(server_url + "/v1/orders/chance", params=query, headers=headers)
	headers = makeToken.makeToken(access_key, secret_key)
	res_accounts = requests.get(server_url + "/v1/accounts", headers=headers)
	PF.printJson(res_order_chance.json())
	PF.printJson(res_accounts.json())




	rfr_order_query = {
		'market': 'KRW-RFR',
		'side': 'ask',
		'volume': '100',
		'price': '100.0',
		'ord_type': 'limit',
	}
	headers = makeToken.makeToken(access_key, secret_key, rfr_order_query)
	#res_ordered = requests.post(server_url + "/v1/orders", params=rfr_order_query, headers=headers)
	#printJson(res_ordered.json())
	#RFR_PRICE = get_price_info('KRW-RFR', '15min', 100)
	#crossed(RFR_PRICE, 15, 50)

	''' watch crossing
	cross = crossed(RFR_PRICE, 15, 50)
	if cross == 1: # buy
		buy(MARKET_NAME, 'market', KRW price = ?)
	elif cross == -1 : #sell
		buy(MARKET_NAME, 'market', KRW_price = ?)
	else:
		None

	'''
