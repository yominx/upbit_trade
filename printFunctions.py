from makeToken import makeToken
import requests

def printMenu():
    print(
    "__________MENU__________\n"
    "Select Menu from below (Capitalize-dependent)\n"
    "\"Wallet\" \t: Show your wallet\n"
    "\"Buy\"  \t\t: Buy(bid)  Menu\n"
    "\"Sell\" \t\t: Sell(ask) Menu\n"
    "\"Market\" \t: Show current price of the market\n"
    "\"AutoTrade\"\t: Trade automatically by using MA-cross algorithm\n"
    "\"updateAccount\"\t: Change user account\n"
    "\"Quit\"\t: Exit program\n"
    )

def printJson(json, depth = 0):
    tab = '  ' * depth    
    if type(json) is list:
        print(tab, "_______________________\n")
        for i in json:
            printJson(i, depth + 1)
        print(tab, "_______________________\n")

    elif type(json) is dict:
        for i in json:
            print(tab, i, ": ", json[i])
        print(tab, "____________")
    else: 
        print("unknown type... type is ", type(json))	

    print()


