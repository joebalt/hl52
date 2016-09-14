import sys
import urllib2


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
            f.write(k + ':' + v + '\n')


def main(argv):
    print('Begin run...')

    print('Loading symbols from {}'.format(argv[1]))
    symbols = load_symbols(argv[1])

    print('Creating outfile {}'.format(argv[1]))
    # create_outfile_headers(symbols, argv[2])

    d = {}
    for s in symbols:
        print('fetching {}...'.format(s))
        d[s] = urllib2.urlopen('http://finance.yahoo.com/d/quotes.csv?s=' + s + '&f=ajkw').read().rstrip()
    print(d)

    create_outfile(d, argv[2])

    print('End run.')


if __name__ == "__main__":
    main(sys.argv)
