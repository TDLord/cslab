import requests

url = 'https://api.bithumb.com/public/ticker/btc'

resp = requests.get(url)

content = resp.json()

btc_close_price = content["data"]["closing_price"]
#close_price = content["data"]["closing_price"]

#print(content)
print("비트코인 마감 시세 :", btc_close_price)
