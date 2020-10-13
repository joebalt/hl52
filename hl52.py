#!/usr/bin/env python3


import argparse
import sys
from yahoo_finance import Share


def init_argparse():
    parser = argparse.ArgumentParser(description="hl52")
    parser.add_argument("--symfile", dest="symFile",
                        help="Path to the symbols file to analyze.")
    return parser.parse_args()


def load_symbols(filename):
    with open(filename, 'rb') as f:
        symbol_list = [line.rstrip() for line in f]
    return symbol_list


def calc_marker_loc(bid, low, high, markerWidth=10):
    markerLoc = 0
    # find out how far above the low price the current bid price is
    if bid >= low:
        bidAboveLow = bid - low
    else:
        return 0
    hlRange = high - low
    markerLoc = int(round(bidAboveLow * markerWidth / hlRange, 0))
    # ensure we don't return anything invalid...just in case.
    if markerLoc > markerWidth - 1:
        markerLoc = markerWidth - 1
    return markerLoc


def print_52_week_hl_marker(bid, low, high, symbol, length=10):
    markerTemplate = list('=' * length)
    markerLoc = calc_marker_loc(bid, low, high, length)
    markerTemplate[markerLoc] = 'X'
    # If bid has crossed below 52-week low, I want the
    # percentage printed at the end of the line here
    # The way I did this feels very 'brute force'...
    if (bid / low) < 1.0:
        print('{:5}@{:6.2f} : {:6.2f}[{}]{:6.2f}  {:6.2f}%'
              .format(symbol,
                      bid,
                      low,
                      ''.join(markerTemplate),
                      high,
                      (bid / low) * 100.0))
    else:
        print('{:5}@{:6.2f}   : {:6.2f}[{}]{:6.2f}'
              .format(symbol,
                      bid,
                      low,
                      ''.join(markerTemplate),
                      high))


def main(argv):
    print('Begin run...')

    args = init_argparse()
    print('Loading symbols from {}'.format(args.symFile))
    symbols = load_symbols(args.symFile)
    d = {}
    for s in symbols:
        print('fetching {}...'.format(s))
        share = Share(s)
        bid = float(share.get_price())
        year_low = float(share.get_year_low())
        year_high = float(share.get_year_high())

        d[s] = [bid, year_low, year_high]

    # v is a list of ticker information:
    #    v[0]  - bid
    #    v[1]  - 52-week low
    #    v[2]  - 52-week high
    for k, v in sorted(d.iteritems()):
        print_52_week_hl_marker(float(v[0]), float(v[1]), float(v[2]), k, 50)

    print('End run.')
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
