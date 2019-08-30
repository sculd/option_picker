from pprint import pprint
import copy
import quote
import statistics
import option_expiration
import option_chains
import analyze_option_chain
from collections import defaultdict

def _filter_out_expiration(expiration):
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
				if _filter_out_expiration(good_call['expiration']):
					continue
				for good_put in good_puts:
					if _filter_out_expiration(good_put['expiration']):
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
				if _filter_out_expiration(good_call['expiration']):
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


def pick_best_put_options():
	puts = []
	for symbol in open('snp100.sample.txt', 'r'):
		symbol = symbol.strip()
		if not symbol:
			print('symbol: %s is not valid thus skipping' % (symbol))
			continue

		try:
			expirations, all_calls, all_puts = analyze_option_chain.analyze_chains(symbol)

			good_puts = all_puts[0][:]

			print('getting quote for symbol: %s' % (symbol))
			qt = quote.get_quote(symbol)
			week_52_relative = quote.get_week_52_relative(symbol)
			if week_52_relative > 0.5:
				continue
			price = (qt['bid'] + qt['ask']) / 2.0
			quote_spread = qt['ask'] - qt['bid']
			for good_put in good_puts:
				if _filter_out_expiration(good_put['expiration']):
					continue
				margin = good_put['margin']
				# price_move_1month = statistics.get_price_move_1month(symbol)
				puts.append({
					'symbol': symbol,
					'put': good_put,
					'margin': margin,
					'margin_normalized': margin / price,
					'instrument_price': price,
					'instrument_spread': quote_spread,
					'instrument_name': qt['description']
				})

		except Exception as e:
			pass

	return sorted(puts, key=lambda e: -e['margin_normalized'])


def pick_best_call_option_quote(symbol):
	def _filter_out_expiration(expiration):
		return expiration[:7] in set(['2019-08'])

	best_by_expiration = {}
	try:
		expirations, all_calls, all_puts = analyze_option_chain.analyze_chains(symbol)

		good_calls = all_calls[0][:]

		print('getting quote for symbol: %s' % (symbol))
		by_expiration = defaultdict(list)
		for call in good_calls:
			by_expiration[call['expiration']].append(call)
		qt = quote.get_quote(symbol)
		for expiration, calls in by_expiration.items():
			if _filter_out_expiration(expiration):
				continue
			good_call = sorted(calls, key=lambda e: -e['margin'])[0]
			best_by_expiration[expiration] = good_call
	except Exception as e:
		pass

	return best_by_expiration


def pick_best_put_option_quote(symbol):
	def _filter_out_expiration(expiration):
		return expiration[:7] in set(['2019-08'])

	best_by_expiration = {}
	try:
		expirations, all_calls, all_puts = analyze_option_chain.analyze_chains(symbol)

		good_puts = all_puts[0][:]

		print('getting quote for symbol: %s' % (symbol))
		by_expiration = defaultdict(list)
		for put in good_puts:
			by_expiration[put['expiration']].append(put)
		qt = quote.get_quote(symbol)
		for expiration, puts in by_expiration.items():
			if _filter_out_expiration(expiration):
				continue
			good_put = sorted(puts, key=lambda e: -e['margin'])[0]
			best_by_expiration[expiration] = good_put
	except Exception as e:
		pass

	return best_by_expiration
