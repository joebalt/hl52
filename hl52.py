#!/usr/bin/env python


import sys
import urllib2
import math


###################
# GLOBALS
yfUrl = 'http://finance.yahoo.com/d/quotes.csv?s='
# from http://www.financialwisdomforum.org/gummy-stuff/Yahoo-data.htm
#     (a)sk, (b)id, j (52-week low), k (52-week high)
yfSwitches = '&f=abjk'
###################


def load_symbols(filename):
    with open(filename, 'rb') as f:
        symbol_list = [line.rstrip() for line in f]
    return symbol_list


def create_outfile_headers(symbols_list, outfile):
    with open(outfile, 'wb') as f:
        for s in symbols_list[:-1]:
            f.write(s + ',')
        f.write(symbols_list[-1])


def create_outfile(d, outfile):
    with open(outfile, 'wb') as f:
        for k, v in d.iteritems():
            f.write(k + ':' + ','.join(v) + '\n')


def calc_marker_loc(bid, high, low):
    """
        Return a whole number [0-9] representing the position
        in a 10-char string that is used to mark the scale of
        the current bid within the 52-week HL range
    """
    markerLoc = 0
    # find out how far above the low price the current bid price is
    if bid >= low:
        bidAboveLow = bid - low
    else:
        return 0

    # Find out how much each '=' char is for increments
    hlRange = high - low
    # how many dollars is represented by one '=' char in marker_template?
    bidMarkerIncrements = math.trunc(math.ceil(math.trunc(math.ceil(hlRange)) / 10.0))

    # how far above 52w low is the bid in increments?
    # first, get bidAboveLow in a rounded up whole number
    bidAboveLow = math.trunc(math.ceil(bidAboveLow))
    markerLoc = math.trunc(math.ceil(bidAboveLow / bidMarkerIncrements))

    # ensure we don't return anything invalid...just in case.
    if markerLoc > 9:
        markerLoc = 9

    return markerLoc


def print_52_week_hl_marker(bid, high, low, symbol):
    markerTemplate = list('==========')
    markerLoc = calc_marker_loc(bid, high, low)
    markerTemplate[markerLoc] = 'X'
    print('{}@{}: {}[{}]{}'.format(symbol, bid, low, ''.join(markerTemplate), high))


def main(argv):
    print('Begin run...')

    print('Loading symbols from {}'.format(argv[1]))
    symbols = load_symbols(argv[1])

    # create_outfile_headers(symbols, argv[2])

    d = {}
    for s in symbols:
        print('fetching {}...'.format(s))
        d[s] = (urllib2.urlopen(yfUrl + s + yfSwitches).read().rstrip()).split(',')
    print(d)

    print('Creating outfile {}'.format(argv[2]))
    create_outfile(d, argv[2])

    
    print_52_week_hl_marker(154.04, 164.95, 116.90, 'IBM')

    print('End run.')


if __name__ == "__main__":
    main(sys.argv)
