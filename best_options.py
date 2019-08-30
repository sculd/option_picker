from pprint import pprint
import copy
import quote
import statistics
import option_expiration
import option_chains
import analyze_option_chain
from collections import defaultdict

def filter_out_expiration(expiration):
	return expiration[:4] in set(['2019']) # or expiration[:7] in set(['2020-01', '2020-03'])


def pick_best_options():
	options = []

	symbol_stats = {}
	for symbol in open('snp100.sample.txt', 'r'):
		symbol = symbol.strip()
		if not symbol:
			print('symbol: %s is not valid thus skipping' % (symbol))
			continue

		try:
			expirations, all_calls, all_puts = analyze_option_chain.analyze_chains(symbol)

			good_calls = all_calls[0][:]
			good_puts = all_puts[0][:]

			print('getting quote for symbol: %s' % (symbol))
			qt = quote.get_quote(symbol)
			price = (qt['bid'] + qt['ask']) / 2.0
			quote_spread = qt['ask'] - qt['bid']
			for good_call in good_calls:
				if filter_out_expiration(good_call['expiration']):
					continue
				for good_put in good_puts:
					if filter_out_expiration(good_put['expiration']):
						continue

					thresholds_gap = good_call['threshold'] - good_put['threshold'] + quote_spread
					# price_move_1month = statistics.get_price_move_1month(symbol)
					options.append({
						'symbol': symbol,
						'call': good_call,
						'put': good_put,
						'thresholds_gap': thresholds_gap,
						'thresholds_gap_normalized': thresholds_gap / price,
						'instrument_price': price,
						'instrument_spread': quote_spread,
						'instrument_name': qt['description']
					})

		except Exception as e:
			pass

	return sorted(options, key=lambda e: e['thresholds_gap_normalized'])
