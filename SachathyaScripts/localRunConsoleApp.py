#For Sachathya

import requests
import json

def readUrl(url):
	webContent = requests.get(url,verify=True).text
	return webContent

src = 'eur'
dst = 'inr'

url = 'https://cdn.jsdelivr.net/gh/fawazahmed0/currency-api@1/latest/currencies/{}/{}.json'.format(src,dst)
resp = readUrl(url)

data = json.loads(resp)

val = data[dst]
reqdate = data['date']

print()
print('Currency rate on {} for one {} is {} {}'.format(reqdate, src, val, dst))
print()
