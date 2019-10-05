import argparse
import option_chains.option_chains


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--symbol", type=str, default='GOOG', help="symbol to update the chain for")
    args = parser.parse_args()

    option_chains.option_chains.update_option_chain(args.symbol)

