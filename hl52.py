#!/usr/bin/env python


import argparse
import sys
import urllib2


###################
# GLOBALS
yfUrl = 'http://download.finance.yahoo.com/d/quotes.csv?s='
# from http://www.financialwisdomforum.org/gummy-stuff/Yahoo-data.htm
#     (a)sk, (b)id, j (52-week low), k (52-week high)
yfSwitches = '&f=abjk'
###################


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
        d[s] = (urllib2.urlopen(yfUrl + s + yfSwitches).read().rstrip()).split(',')

    # v is a list of ticker information:
    #    v[0]  - ask
    #    v[1]  - bid
    #    v[2]  - 52-week low
    #    v[3]  - 52-week high
    for k, v in sorted(d.iteritems()):
        if v[0] == 'N/A' and v[1] == 'N/A':
            print("XXXXXXXXXX  Cannot process {}, bid and ask prices are N/A".format(k))
            continue
        # use ask (v[0]) as bid (v[1]) if bid is 'N/A'
        if v[1] == 'N/A':
            v[1] = v[0]

        print_52_week_hl_marker(float(v[1]), float(v[2]), float(v[3]), k, 50)

    print('End run.')
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
