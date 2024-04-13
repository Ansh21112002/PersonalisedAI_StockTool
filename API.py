import yfinance as yf
from datetime import *

def data(ticker):
  msft = yf.Ticker(ticker)
  return msft.history(period="1y")

# print(data('BAJAJFINSV.NS'))

def databack(ticker,end_date=datetime.now() ,start_date=datetime.now() - timedelta(days=365)):
  msft = yf.Ticker(ticker)
  return msft.history(start=start_date.strftime('%Y-%m-%d'), end=end_date.strftime('%Y-%m-%d'))



# print(databack('AXISBANK.NS'))


