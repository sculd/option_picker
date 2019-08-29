import requests, os

_ACCESS_TOKEN = os.environ['TRADIER_ACCESS_TOKEN']

_URL_BASE = 'https://sandbox.tradier.com'
#_URL_BASE = 'https://api.tradier.com'
_AUTH_PATH = '/v1/oauth/accesstoken'

'''
response = requests.post(_URL_BASE + _AUTH_PATH,
    data={
    	'grant_type': 'authorization_code', 
    	'code': 'PRpnf1o7'
    	},
    headers={
	    "Authorization":"Bearer " + _ACCESS_TOKEN, 
	    'Accept': 'application/json'
    }
)

json_response = response.json()
print(response.status_code)
print(json_response)
'''

_QUOTE_PATH = '/v1/markets/quotes?symbols=spy'

response = requests.get(_URL_BASE + _QUOTE_PATH,
    data={
    	},
    headers={
	    "Authorization":"Bearer " + _ACCESS_TOKEN, 
	    'Accept': 'application/json'
    }
)
json_response = response.json()
print(response.status_code)
print(json_response)





_OPTION_CHAINS_PATH = '/v1/markets/options/chains?symbol={symbol}&expiration={expiration}'

param_option = {
	'symbol': 'BND',
	'expiration': '2019-09-21'
}

response = requests.get(_URL_BASE + _OPTION_CHAINS_PATH.format(**param_option),
    data={
    	},
    headers={
	    "Authorization":"Bearer " + _ACCESS_TOKEN, 
	    'Accept': 'application/json'
    }
)
json_response = response.json()
print(response.status_code)
print(json_response)






