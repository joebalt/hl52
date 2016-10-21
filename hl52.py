#!/usr/bin/env python


import sys
import urllib2


###################
# GLOBALS
yfUrl = 'http://download.finance.yahoo.com/d/quotes.csv?s='
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
    print('{:5}@{:6.2f}   : {:6.2f}[{}]{:6.2f}'.format(symbol, bid, low, ''.join(markerTemplate), high))


def main(argv):
    print('Begin run...')

    print('Loading symbols from {}'.format(argv[1]))
    symbols = load_symbols(argv[1])
    d = {}
    for s in symbols:
        print('fetching {}...'.format(s))
        d[s] = (urllib2.urlopen(yfUrl + s + yfSwitches).read().rstrip()).split(',')
    print(d)

    print('Creating outfile {}'.format(argv[2]))
    create_outfile(d, argv[2])

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
