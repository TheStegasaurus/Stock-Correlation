# Stock Correlation
Pulls historical stock market data from yahoo finance, generates a correlation matrix between the daily change in price for selected stocks, and generates a d3 visualization showing links between correlated stocks.

## How to run
1. Download and install pycharm
2. Import code into new flask project & install dependencies (Python 3.6)
3. Set up configuration to run app.py as a flask app and set working directory to root if it is not already
4. Open app.html in pycharm and click the browser button at the top right to open a browser tab (to avoid cross origin errors) 
ip configuration: line 91
5. Run app.py
6.  Pick selected stocks and hit generate, if configured properly you should see the data in the python console -> correlation matrix and d3 data are in AUTO.csv and AUTO.json respectively, dynamically generated 

## Required libraries
flask  
flask_cors  
json  
multiprocessing
pandas  
numpy  
re  
datetime  
py_yahoo_prices.price_fetcher

## Notes
1. Currently using a workaround for yahoo finance API restrictions, will most likely be deprecated soon.

2. If graph tab is switched before circle graph is done converging D3 will throw an error. Reloading the page fixes this.


![alt text](screencap.PNG)
