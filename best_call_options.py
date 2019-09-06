from quotes import quote
from best_options import filter_out_expiration
from option_chains import analyze_option_chain
from collections import defaultdict


def pick_best_call_options():
    calls = []
    for symbol in open('snp100.sample.txt', 'r'):
        symbol = symbol.strip()
        if not symbol:
            print('symbol: %s is not valid thus skipping' % (symbol))
            continue

        try:
            expirations, all_calls, all_puts = analyze_option_chain.analyze_chains(symbol)

            good_calls = all_calls[0][:]

            print('getting quote for symbol: %s' % (symbol))
            qt = quote.get_quote(symbol)
            week_52_relative = quote.get_week_52_relative(symbol)
            if week_52_relative < 0.5:
                continue
            price = (qt['bid'] + qt['ask']) / 2.0
            quote_spread = qt['ask'] - qt['bid']
            for good_call in good_calls:
                if filter_out_expiration(good_call['expiration']):
                    continue
                margin = good_call['margin']
                # price_move_1month = statistics.get_price_move_1month(symbol)
                calls.append({
                    'symbol': symbol,
                    'call': good_call,
                    'margin': margin,
                    'margin_normalized': margin / price,
                    'instrument_price': price,
                    'instrument_spread': quote_spread,
                    'instrument_name': qt['description']
                })

        except Exception as e:
            pass

    return sorted(calls, key=lambda e: -e['margin_normalized'])


def pick_best_call_option_quote_at_expiration(symbol, expiration, limit=1):
    def filter_out_expiration(call_expiration):
        if not expiration:
            return call_expiration[:7] in set(['2019-08'])
        else:
            return expiration != call_expiration

    best_by_expiration = {}
    try:
        expirations, all_calls, all_puts = analyze_option_chain.analyze_chains(symbol)

        good_calls = all_calls[0][:]

        print('getting quote for symbol: %s' % (symbol))
        by_expiration = defaultdict(list)
        for call in good_calls:
            if filter_out_expiration(call['expiration']):
                continue
            by_expiration[call['expiration']].append(call)

        for expiration, calls in by_expiration.items():
            good_call = sorted(calls, key=lambda e: -e['margin'])[:limit]
            best_by_expiration[expiration] = good_call
    except Exception as e:
        pass

    return best_by_expiration


def pick_best_call_option_quote(symbol):
    return pick_best_call_option_quote_at_expiration(symbol, None)

