import requests, os
import util.common

# not available in sandbox
_QUOTE_PATH = '/beta/markets/fundamentals/statistics?symbols={symbol}'


def get_statistics(symbol):
	param_option={'symbol': symbol}

	response = requests.get(util.common.URL_BASE_TRADIER + _QUOTE_PATH.format(**param_option),
	    data={},
	    headers=util.common.get_auth_header_tradier()
	)

	json_response = response.json()
	return json_response[0]['results'][0]['tables']['price_statistics']


def get_price_move_1month(symbol):
	statistics = get_statistics(symbol)
	return statistics['period_1m']['high_price'] - statistics['period_1m']['low_price']
