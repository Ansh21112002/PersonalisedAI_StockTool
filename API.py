import yfinance as yf

def data(ticker):
  msft = yf.Ticker(ticker)
  return msft.history(period="1y")
