#!/usr/bin/env bash

# steps to take getWatchlistDetail.csv, dl'ed from fidelity.com
#    to hl52.input4 - suitable for input to hl52.py

infile="getWatchlistDetail.csv"
input1="hl52.input1"
input2="hl52.input2"
input3="hl52.input3"
input4="hl52.input4"

echo "Cleaning up previous run artifacts..."
rm -f $input1 $input2 $input3 $input4

headerLines=4
summaryLines=14

# get total number of lines w/o headers included
infileLineCount=$(cat $infile | wc -l)
linesMinusHeaders=$(( $infileLineCount - $headerLines ))

echo "Total lines in $infile: $infileLineCount"
echo "Lines minus headers: $linesMinusHeaders"

echo "Getting the 2nd field from the file..."
cat $infile | cut -d ',' -f 2 >$input1

echo "Trimming out header lines..."
cat $input1 | tail -$linesMinusHeaders >$input2

# get total number of lines w/o the ending summary lines
totalLines=$(cat $input2 | wc -l)
linesMinusSummary=$(( $totalLines - $summaryLines ))
echo "Lines minus summary: $linesMinusSummary"
echo "Trimming out summary lines..."
cat $input2 | head -$linesMinusSummary >$input3

echo "Removing double quotes..."
sed -i "s/\"//g" $input3

echo "Sorting results..."
cat $input3 | sort >$input4

echo "$input4 created!"

cat -n $input4

exit 0
