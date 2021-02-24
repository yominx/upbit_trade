import requests
 
r = requests.get('http://jsonip.com')
ip= r.json()

print(ip)