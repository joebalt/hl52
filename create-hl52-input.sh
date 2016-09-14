#!/usr/bin/env bash

# steps to take getWatchListDetail.csv, dl'ed from fidelity.com
#    to hl52.input4 - suitable for input to hl52.py

cat getWatchlistDetail.csv | cut -d ',' -f 2 >hl52.input

cat hl52.input | head -42 >hl52.input2

cat hl52.input2 | tail -38 >hl52.input3

sed -i "s/\"//g" hl52.input3

cat hl52.input3 | sort >hl52.input4

echo "hl52.input4 created!"

cat -n hl52.input4

exit 0

