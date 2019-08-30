import requests, os, pickle, time
import util.common
import option_expiration

_ACCESS_TOKEN = os.environ['TRADIER_ACCESS_TOKEN']
_FILENAME_SAVED_OPTION_CHAINS = 'option_chains.pickle'

_OPTION_CHAINS_PATH = '/v1/markets/options/chains?symbol={symbol}&expiration={expiration}'

_request_cnt = 0


def _get_empty_chain():
    return {
        'call': [],
        'put': []
    }

def _request_option_chain_for_expiration(symbol, expiration):
    param_option = {
        'symbol': symbol,
        'expiration': expiration
    }

    response = requests.get(util.common.URL_BASE + _OPTION_CHAINS_PATH.format(**param_option),
        data={},
        headers=util.common.get_auth_header()
    )
    print('option chain request for symbol: %s, expiration: %s, response: %d' % (symbol, expiration, response.status_code))
    respoonse_js = response.json()
    chain = _get_empty_chain()
    chain_for_expiration = respoonse_js['options']['option']
    for option_quote in chain_for_expiration:
        if option_quote['open_interest'] == 0:
            continue
        blob = {
            'strike': option_quote['strike'],
            'bid': option_quote['bid'],
            'ask': option_quote['ask'],
            'volume': option_quote['volume'],
            'open_interest': option_quote['open_interest']
        }
        if option_quote['option_type'] == 'call':
            chain['call'].append(blob)
        elif option_quote['option_type'] == 'put':
            chain['put'].append(blob)

    return {
            'expiration': expiration,
            'chain': chain
            }

def _request_option_chain(symbol):
    global _request_cnt
    res = []
    expirations = option_expiration.get_option_expiration(symbol)
    for expiration in expirations:
        chain = _request_option_chain_for_expiration(symbol, expiration['date'])
        _request_cnt += 1
        print('_request_cnt: %d, symbol: %s, expiration: %s' % (_request_cnt, symbol, expiration['date']))
        res.append(chain)
    return res


def update_option_chain(symbol):
    global _request_cnt
    if _request_cnt > 53:
        time.sleep(60)
        _request_cnt = 0

    chains_loaded = {}
    try:
        with open(_FILENAME_SAVED_OPTION_CHAINS, 'rb') as handle:
            chains_loaded.update(pickle.load(handle))
    except Exception as e:
        pass

    res = _request_option_chain(symbol)
    chains_loaded[symbol] = res
    with open(_FILENAME_SAVED_OPTION_CHAINS, 'wb') as handle:
        pickle.dump(chains_loaded, handle, protocol=pickle.HIGHEST_PROTOCOL)

    return res


def get_option_chains(symbol):
    chains_loaded = {}
    try:
        with open(_FILENAME_SAVED_OPTION_CHAINS, 'rb') as handle:
            chains_loaded.update(pickle.load(handle))
            if symbol in chains_loaded:
                return chains_loaded[symbol]
    except Exception as e:
        pass

    return update_option_chain(symbol)



