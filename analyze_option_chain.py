import copy
import quote
import option_chains

def analyze_chains(symbol):
	res = {
		'expirations': [],
		'all_calls': [],
		'all_puts': []
	}
	qt = quote.get_quote(symbol)
	chains = option_chains.get_option_chains(symbol)
	for chain in chains:
		call_margins = []
		for call in chain['chain']['call']:
			# the option chain in practice does not show strike price too far away
			if 1.0 * abs(qt['bid'] - call['strike']) / qt['bid'] > 0.4:
				continue
			call_margin = round((qt['bid'] - call['strike']) - call['ask'], 3)
			if call_margin > 0.5:
				continue
			call_margins.append({
				'margin': call_margin,
				'strike': call['strike'],
				'threshold': call['strike'] + call['ask']
			})

		put_margins = []
		for put in chain['chain']['put']:
			# the option chain in practice does not show strike price too far away
			if 1.0 * abs(call['strike'] - qt['ask']) / qt['ask'] > 0.4:
				continue
			put_margin = round((-qt['ask'] + put['strike']) - put['ask'], 3)
			if put_margin > 0.5:
				continue
			put_margins.append({
				'margin': put_margin,
				'strike': put['strike'],
				'threshold': put['strike'] - put['ask']
			})

		blob = {
			'call': sorted(call_margins, key=lambda e: -e['margin']),
			'put': sorted(put_margins, key=lambda e: -e['margin'])
		}

		res['expirations'].append({
			'expiration': chain['expiration'],
			'chain': blob
			})

		calls = []
		for expiration in res['expirations']:
			for call_blob in expiration['chain']['call']:
				call_blob_ = copy.copy(call_blob)
				call_blob_['expiration'] = expiration['expiration']
				calls.append(call_blob_)

		puts = []
		for expiration in res['expirations']:
			for put_blob in expiration['chain']['put']:
				put_blob_ = copy.copy(put_blob)
				put_blob_['expiration'] = expiration['expiration']
				puts.append(put_blob_)

		res['all_calls'] = sorted(calls, key=lambda e: -e['margin'])[:],
		res['all_puts'] = sorted(puts, key=lambda e: -e['margin'])[:],

	return res['expirations'], res['all_calls'], res['all_puts'],
