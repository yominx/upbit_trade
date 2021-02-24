import os
import jwt
import uuid
import hashlib
from urllib.parse import urlencode

import requests

#Account infos
access_key = 'c8KY91Z3cjl5jOubzkExjAy6Mq3jTdjl2AZxtbrw'
secret_key = 'ez1GkoQKZ9NCeHmwvJfZBSO1uJvx5f2uhigYQiGE'
server_url = 'https://api.upbit.com'

def make_token(query=None, txids = None):
	if query != None:
		query_string = urlencode(query).encode()
		if txids!=None:
			txids_query_string = '&'.join(["txids[]={}".format(txid) for txid in txids])

			query['txids[]'] = txids
			query_string = "{0}&{1}".format(query_string, txids_query_string).encode()
		m = hashlib.sha512()
		m.update(query_string)
		query_hash = m.hexdigest()
		payload = {
		    'access_key': access_key,
		    'nonce': str(uuid.uuid4()),
		    'query_hash': query_hash,
		    'query_hash_alg': 'SHA512',
		}
	else: 
		payload = {
		    'access_key': access_key,
		    'nonce': str(uuid.uuid4()),
		}


	encoded_token = jwt.encode(payload, secret_key,'HS512').encode()
	jwt_token = encoded_token.decode('utf-8')
	authorize_token = 'Bearer {}'.format(jwt_token)
	headers = {"Authorization": authorize_token}

	return headers

def print_json(json):
	if type(json) is list:
		print("List_____________________\n")
		for i in json:
			print_json(i)
	elif type(json) is dict:
		print("Dict____________\n")
		for i in json:
			print(i, ": ", json[i])
	else: 
		print("unknown type... type is ", type(json))	
	
	print()

def check_wallet_net_input():
	headers = make_token()
	res = requests.get(server_url + "/v1/deposits", headers=headers).json()
	deposit = 0
	for tx in res:
		if tx['currency'] == 'KRW' and tx['state'] == 'ACCEPTED':
			deposit = deposit + float(tx['amount'])
	print('You deposited ', deposit, 'Won')

	headers = make_token()
	res = requests.get(server_url + "/v1/withdraws", headers=headers).json()
	withdraw = 0
	for tx in res:
		if tx['currency'] == 'KRW' and tx['state'] == 'DONE':
			withdraw = withdraw + float(tx['amount'])
	print('You withdrawed ', withdraw, 'Won')
	print('Net input: you deposited ', (deposit-withdraw)/10000,'×10⁴ Won')

def get_price_info(market: str, minute: str, count: int):
	url = "https://api.upbit.com/v1/candles/minutes/" + minute[:-3]
	querystring = {"market":market,"count": str(count)}
	response = requests.request("GET", url, params=querystring).json()
	price_info = []
	for res in response:
		price_info.append(float(res['trade_price']))

	return price_info

def crossed(priceinfo: list, avg1, avg2) -> int:
	assert(avg1<avg2 and avg2 < 100)
	### Return true if AVG_15 price have passed AVG_50. 
	AVG_15_RECENT = sum(RFR_PRICE[1:16])/15
	AVG_50_RECENT = sum(RFR_PRICE[1:51])/50

	AVG_15_PAST = sum(RFR_PRICE[2:17])/15
	AVG_50_PAST = sum(RFR_PRICE[2:52])/50
	
	print(AVG_15_RECENT)
	print(AVG_50_RECENT)
	print(AVG_15_PAST)
	print(AVG_50_PAST)

	if AVG_50_PAST> AVG_15_PAST and AVG_50_RECENT < AVG_15_RECENT:
		return 1
	elif AVG_50_PAST < AVG_15_PAST and AVG_50_RECENT > AVG_15_RECENT:
		return -1
	else: 
		return 0

def buy_market_query(market: str, order_price: int):
	return { 'market': market, 'side': 'bid', 'volume': null, 'price': str(order_price), 'ord_type': 'price', }
def sell_market_query(market: str, order_price: int):
	return { 'market': market, 'side': 'ask', 'volume': 10, 'price': null, 'ord_type': 'market', }


if __name__ == "__main__":
	while True:
		print(
			"__________MENU__________\n"
			"Select Menu from below (Capitalize-dependent)\n"
			"\"Wallet\" \t: Show your wallet\n"
			"\"Buy\"  \t\t: Buy(bid)  Menu\n"
			"\"Sell\" \t\t: Sell(ask) Menu\n"
			"\"Market\" \t: Show current price of the market\n"
			"\"AutoTrade\"\t: Trade automatically by using MA-cross algorithm\n"
			"\"Quit\"\t: Exit program\n"
			)

		selected = input('').lower()
		if selected == 'wallet':
			headers = make_token()
			res_accounts = requests.get(server_url + "/v1/accounts", headers=headers)
			print_json(res_accounts.json())

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

		else: 
			print("Invalid request")


	{
		'''
		query = {
	    	'market': 'KRW-RFR',
		}
		headers = make_token(query)
		res_order_chance = requests.get(server_url + "/v1/orders/chance", params=query, headers=headers)
		headers = make_token()
		res_accounts = requests.get(server_url + "/v1/accounts", headers=headers)
		print_json(res_order_chance.json())
		print_json(res_accounts.json())
		'''
	}



	rfr_order_query = {
	    'market': 'KRW-RFR',
	    'side': 'ask',
	    'volume': '100',
	    'price': '100.0',
	    'ord_type': 'limit',
	}
	headers = make_token(rfr_order_query)
	#res_ordered = requests.post(server_url + "/v1/orders", params=rfr_order_query, headers=headers)
	#print_json(res_ordered.json())

	#check_wallet_net_input()

	RFR_PRICE = get_price_info('KRW-RFR', '15min', 100)
	crossed(RFR_PRICE, 15, 50)

''' watch crossing
	cross = crossed(RFR_PRICE, 15, 50)
	if cross == 1: # buy
		buy(MARKET_NAME, 'market', KRW price = ?)
	elif cross == -1 : #sell
		buy(MARKET_NAME, 'market', KRW_price = ?)
	else:
		None

'''
