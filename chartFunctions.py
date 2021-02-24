import requests
import json

def getPriceInfo(market: str, minute: str, count: int):
    url = "https://api.upbit.com/v1/candles/minutes/" + minute[:-3]
    querystring = {"market":market, "count": str(count)}
    response = requests.request("GET", url, params=querystring).json()
    price_info = []
    for res in response:
        price_info.append(float(res['trade_price']))
    return price_info

def crossed(priceinfo: list, avg1, avg2):
    assert(avg1<avg2 and avg2 < 100)
    ### Return true if AVG_15 price have passed AVG_50. 
    AVG_15_RECENT = sum(priceinfo[:15])/15
    AVG_50_RECENT = sum(priceinfo[:50])/50

    AVG_15_PAST = sum(priceinfo[1:16])/15
    AVG_50_PAST = sum(priceinfo[1:51])/50

    print("____________")
    print(priceinfo)
    print(AVG_50_RECENT-AVG_15_RECENT)
    print(AVG_50_PAST-AVG_15_PAST)
    if AVG_50_PAST> AVG_15_PAST and AVG_50_RECENT < AVG_15_RECENT:
        return 1
    elif AVG_50_PAST < AVG_15_PAST and AVG_50_RECENT > AVG_15_RECENT:
        return -1
    else: 
        return 0
