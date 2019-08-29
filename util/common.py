import requests, os

_ACCESS_TOKEN = os.environ['TRADIER_ACCESS_TOKEN']

URL_BASE = 'https://sandbox.tradier.com'

def get_auth_header():
    return {
	    "Authorization":"Bearer " + _ACCESS_TOKEN, 
	    'Accept': 'application/json'
    }
