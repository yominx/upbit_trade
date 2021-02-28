import os
import jwt
import uuid
import hashlib
import json
import keyboard
import time

import userInfo
import marketInfo
import logger
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
		print(i, end="  ")
	user = input("\nWhich account you want to use? ")
	userinfo = infos[user]
	access_key = userinfo["access_key"]
	secret_key = userinfo["secret_key"]
	return (access_key, secret_key)


if __name__ == "__main__":
	marketInfo.saveMarketInfoToTrade()
	(access_key, secret_key) = getAccountInfo()
	server_url = "https://api.upbit.com"
	logger.logInit()
	while True:
		PF.printMenu()
		selected = input("").lower()
		if selected == "wallet":
			WF.walletInfo(access_key, secret_key)
		elif selected == "allmarkets":
			url = "https://api.upbit.com/v1/market/all"
			querystring = {"isDetails": "false"}
			res = requests.request("GET", url, params=querystring).json()
			for item in res:
				if item["market"][:3] == "KRW":
					PF.printJson(item)
		elif selected == "buy":
			print("Not yet")
		elif selected == "sell":
			print("Not yet")
		elif selected == "market":
			print("Not yet")

		elif selected == "autotrade":
			# market = input("Which market do you want to trade? ")
			# market = "KRW-" + market
			# print("You selected ", market)
			tradeMarketInfo = marketInfo.getMarketInfoToTrade()
			while True:
				t = time.localtime()
				current_time = time.strftime("%H:%M:%S", t)
				logger.logPrint("Check Tradability")
				TF.tradeMarket(tradeMarketInfo, access_key, secret_key)
				time.sleep(30)

		elif selected == "updateaccount":
			(access_key, secret_key) = getAccountInfo()
			print("Update done.\n")
			continue
		elif selected == "showorder":
			TF.showOrderInfo(access_key, secret_key)
		elif selected == "quit":
			print("Exit the program.")
			break

		else:
			print("Invalid request")

		input("Press Enter to continue...")