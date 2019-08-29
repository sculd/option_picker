import requests, os, pickle, time
import util.common
import option_expiration

_ACCESS_TOKEN = os.environ['TRADIER_ACCESS_TOKEN']
_FILENAME_SAVED_OPTION_CHAINS = 'option_chains.pickle'

_OPTION_CHAINS_PATH = '/v1/markets/options/chains?symbol={symbol}&expiration={expiration}'

_request_cnt = 0

def get_option_chains(symbol):
    global _request_cnt
    chains_loaded = {}
    try:
        with open(_FILENAME_SAVED_OPTION_CHAINS, 'rb') as handle:
            chains_loaded.update(pickle.load(handle))
            if symbol in chains_loaded:
                return chains_loaded[symbol]
    except Exception as e:
        pass
    res = []
    def _get_empty_chain():
        return {
            'call': [],
            'put': []
        }

    expirations = option_expiration.get_option_expiration(symbol)
    for expiration in expirations:
        exp_date = expiration['date']
        param_option = {
            'symbol': symbol,
            'expiration': exp_date
        }

        if _request_cnt > 53:
            time.sleep(60)
            _request_cnt = 0
            with open(_FILENAME_SAVED_OPTION_CHAINS, 'wb') as handle:
                pickle.dump(chains_loaded, handle, protocol=pickle.HIGHEST_PROTOCOL)

        response = requests.get(util.common.URL_BASE + _OPTION_CHAINS_PATH.format(**param_option),
            data={},
            headers=util.common.get_auth_header()
        )
        _request_cnt += 1
        print('_request_cnt: %d, symbol: %s, expiration: %s, status_code: %d' %
              (_request_cnt, symbol, expiration['date'], response.status_code))
        respoonse_js = response.json()
        chain = _get_empty_chain()
        js = respoonse_js['options']['option']
        for entry in js:
            if entry['volume'] == 0:
                continue
            blob = {
                'strike': entry['strike'],
                'bid': entry['bid'],
                'ask': entry['ask'],
                'volume': entry['volume']
            }
            if entry['option_type'] == 'call':
                chain['call'].append(blob)
            elif entry['option_type'] == 'put':
                chain['put'].append(blob)
        res.append({
                'expiration': exp_date,
                'chain': chain
            })

    chains_loaded[symbol] = res
    with open(_FILENAME_SAVED_OPTION_CHAINS, 'wb') as handle:
        pickle.dump(chains_loaded, handle, protocol=pickle.HIGHEST_PROTOCOL)

    return res





