import requests, os, pickle
import util.common

_ACCESS_TOKEN = os.environ['TRADIER_ACCESS_TOKEN']
_FILENAME_SAVED_QUOTES = 'quotes.pickle'

_QUOTE_PATH = '/v1/markets/quotes?symbols={symbol}'

_request_cnt = 0

def get_quote(symbol):
    global _request_cnt
    quotes_loaded = {}
    try:
        with open(_FILENAME_SAVED_QUOTES, 'rb') as handle:
            quotes_loaded.update(pickle.load(handle))
            if symbol in quotes_loaded:
                return quotes_loaded[symbol]
    except Exception as e:
        pass

    param_option={'symbol': symbol}

    if _request_cnt > 53:
        time.sleep(60)
        _request_cnt = 0
        with open(_FILENAME_SAVED_QUOTES, 'wb') as handle:
            pickle.dump(quotes_loaded, handle, protocol=pickle.HIGHEST_PROTOCOL)

    response = requests.get(util.common.URL_BASE + _QUOTE_PATH.format(**param_option),
        data={},
        headers=util.common.get_auth_header()
    )

    json_response = response.json()
    res = json_response['quotes']['quote']

    quotes_loaded[symbol] = res
    with open(_FILENAME_SAVED_QUOTES, 'wb') as handle:
        pickle.dump(quotes_loaded, handle, protocol=pickle.HIGHEST_PROTOCOL)

    return res

