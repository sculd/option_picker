import argparse
import quotes.quote
import pprint

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--symbol", type=str, default='GOOG', help="symbol to update the chain for")
    parser.add_argument("-a", "--allupdate", action="store_true", help="update all symbols in the list")
    args = parser.parse_args()

    if args.allupdate:
        for symbol in open('snp100.sample.txt', 'r'):
            symbol = symbol.strip()
            if not symbol:
                print('symbol: %s is not valid thus skipping' % (symbol))
                continue
            quotes.quote.update_quote(symbol)
    else:
        pprint.pprint(quotes.quote.update_quote(args.symbol))

