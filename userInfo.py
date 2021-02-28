import json

path = "./userinfo.json"


def saveUserInfo():
    # Suhwan
    userinfo = {
        "suhwan": {
            "access_key": "NkzgxS8hSrkvAfW6eclczNbHdtpEzAhKXzjxnLjd",
            "secret_key": "3JI0lHlDZgmwIcXdbdB9FNvv4tmxYjTQ4x5Gij9W",
        },
        "shyun": {
            "access_key": "AyQGGQ3WyyHA0kBFF5yFY4ljgYCxbi16g4GHhdEV",
            "secret_key": "3YU1VVUAjd7lRHmaMi7oOxANmDONgIL1wnLfwsIz",
        },
    }

    with open(path, "w") as outfile:
        json.dump(userinfo, outfile)
    print("save done.")


def getUserInfo():
    with open(path, "r") as json_file:
        json_data = json.load(json_file)
        return json_data
