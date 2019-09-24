from pprint import pprint
import best_call_options


#pprint(quote.get_quote('USMV'))


'''
bests = best_options.pick_best_options()
print('**********')
print('bests')
pprint(bests[:10])
#'''


'''
best_calls = best_call_options.pick_best_call_options()
print('**********')
print('best_calls')
pprint(best_calls[:10])
#'''


'''
best_puts = best_put_options.pick_best_put_options()
print('**********')
print('best_puts')
pprint(best_puts[:10])
#'''

#'''
symbol = 'LXRX'
#option_chains.update_option_chain(symbol)
best_call_quotes = best_call_options.pick_best_call_option_quote(symbol)
print('**********')
print('best_call_quotes')
pprint(best_call_quotes)
#'''

'''
best_call_quotes_at_expiration = best_call_options.pick_best_call_option_quote_at_expiration(symbol, '2020-01-17', limit=30)
print('**********')
print('best_call_quotes_at_expiration')
pprint(best_call_quotes_at_expiration)
#'''





