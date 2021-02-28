import json

marketPath = "./marketinfo.json"


def saveMarketInfoToTrade():
    marketInfo = {
        "KRW-BTC": {"time": "15min", "short": 15, "long": 50, "price": 400000},
        "KRW-ETH": {"time": "15min", "short": 15, "long": 50, "price": 300000},
        "KRW-XRP": {"time": "15min", "short": 15, "long": 50, "price": 200000},
        "KRW-XLM": {"time": "15min", "short": 15, "long": 50, "price": 200000},
        "KRW-ADA": {"time": "15min", "short": 15, "long": 50, "price": 200000},
        "KRW-DOT": {"time": "15min", "short": 15, "long": 50, "price": 200000},
        "KRW-QKC": {"time": "15min", "short": 15, "long": 50, "price": 200000},
        "KRW-CRO": {"time": "15min", "short": 15, "long": 50, "price": 200000},
        "KRW-EOS": {"time": "15min", "short": 15, "long": 50, "price": 200000},
        "KRW-CRE": {"time": "15min", "short": 15, "long": 50, "price": 200000},
        "KRW-ZIL": {"time": "15min", "short": 15, "long": 50, "price": 200000},
        "KRW-ETC": {"time": "15min", "short": 15, "long": 50, "price": 200000},
        "KRW-PCI": {"time": "15min", "short": 15, "long": 50, "price": 200000},
        "KRW-DOGE": {"time": "15min", "short": 15, "long": 50, "price": 200000},
    }

    with open(marketPath, "w") as outfile:
        json.dump(marketInfo, outfile)
    print("save done.")


def getMarketInfoToTrade():
    with open(marketPath, "r") as json_file:
        json_data = json.load(json_file)
        return json_data
