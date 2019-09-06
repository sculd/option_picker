import best_call_options
import pprint

with open('top_high_symbols.txt') as infile, open('top_high_symbol_call_options.txt', 'w') as outfile:
    for symbol in infile:
        symbol = symbol.strip()
        if not symbol:
            continue
        bests = best_call_options.pick_best_call_option_quote(symbol)
        print(symbol)
        pprint.pprint(bests)
        outfile.write(symbol)
        outfile.write('\n')
        outfile.write(pprint.pformat(bests))
        outfile.write('\n')
