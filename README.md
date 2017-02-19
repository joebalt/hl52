# Pre-reqs
Uses: https://pypi.python.org/pypi/yahoo-finance/1.1.4

pip install yahoo-finance

Run ./create-hl52-input.sh to create requisite input file for usage.

You can modify getWatchListDetail.csv to include additional symbols for your own use. Just copy an existing line and change the symbol only in the new line - the other data is not used.

# Synopsis
Attempt to analyze stocks based on their current state with respect to their 52-week high and low values.

Look for stocks that are near their 52-week low, and are substantially below their 52-week high.

Questions:

- What does 'substantially' mean here?
- What can be used to back test this algorithm? That is, how would you test past history of the current price? Is the stock REALLY down or is it plummeting, for example.

