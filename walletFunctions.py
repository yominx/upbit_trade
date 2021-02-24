from makeToken import makeToken
import requests
import printFunctions as PF 

server_url = 'https://api.upbit.com'

def checkWalletNetInput(access_key, secret_key):
	headers = makeToken(access_key,secret_key)
	res = requests.get(server_url + "/v1/deposits", headers=headers).json()
	deposit = 0
	for tx in res:
		if tx['currency'] == 'KRW' and tx['state'] == 'ACCEPTED':
			deposit = deposit + float(tx['amount'])
	print('You deposited ', deposit, 'Won')

	headers = makeToken(access_key,secret_key)
	res = requests.get(server_url + "/v1/withdraws", headers=headers).json()
	withdraw = 0
	for tx in res:
		if tx['currency'] == 'KRW' and tx['state'] == 'DONE':
			withdraw = withdraw + float(tx['amount'])
	print('You withdrawed ', withdraw, 'Won')
	print('Net input: you deposited ', (deposit-withdraw)/10000,'×10⁴ Won')

def walletInfo(access_key, secret_key):
    candleUrl = "https://api.upbit.com/v1/candles/days"
    headers = makeToken(access_key,secret_key)
    wallet_info = requests.get(server_url + "/v1/accounts", headers=headers).json()
    for elem in wallet_info:
        del elem['locked']
        del elem['avg_buy_price']
        del elem['avg_buy_price_modified']
        del elem['unit_currency']
        if elem['currency'] == 'KRW':
            continue
        querystring = {"market":"KRW-"+elem['currency'],"count":"1"}
        curPrice = requests.request("GET",candleUrl, params=querystring).json()[0]['trade_price'] 
        elem['price'] = curPrice
        elem['est. KRW'] = format(int(curPrice * float(elem['balance'])), ',')
        #print(curPrice)
        
    PF.printJson(wallet_info)

def marketValidInfo(access_key, secret_key, market):
    query = {'market': market}
    headers = makeToken(access_key, secret_key, query)
    res = requests.get(server_url + "/v1/orders/chance", params=query, headers=headers).json()
    return res

