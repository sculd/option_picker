import best_put_options
import pprint

with open('top_low_symbols.txt') as infile, open('top_low_symbol_put_options.txt', 'w') as outfile:
    for symbol in infile:
        symbol = symbol.strip()
        if not symbol:
            continue
        bests = best_put_options.pick_best_put_option_quote(symbol)
        print(symbol)
        pprint.pprint(bests)
        outfile.write(symbol)
        outfile.write('\n')
        outfile.write(pprint.pformat(bests))
        outfile.write('\n')
