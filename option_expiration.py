import requests, os
import util.common

_ACCESS_TOKEN = os.environ['TRADIER_ACCESS_TOKEN']

_OPTION_EXPIRATION_PATH = '/v1/markets/options/expirations?symbol={symbol}&includeAllRoots=true&strikes=true'


def get_option_expiration(symbol):
	param_option={'symbol': symbol}

	response = requests.get(util.common.URL_BASE + _OPTION_EXPIRATION_PATH.format(**param_option),
	    data={},
	    headers=util.common.get_auth_header()
	)

	json_response = response.json()
	return json_response['expirations']['expiration']
