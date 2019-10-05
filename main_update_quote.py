import argparse
import quotes.quote
import pprint

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--symbol", type=str, default='GOOG', help="symbol to update the chain for")
    args = parser.parse_args()

    pprint.pprint(quotes.quote.update_quote(args.symbol))

