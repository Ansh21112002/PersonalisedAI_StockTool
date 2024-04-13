import yfinance as yf
import json
from flask import Flask, request, jsonify
from API import data
from Shortterm import*
from Longterm import *
from Midterm import*
from CONSTANTS import *
from flask_cors import CORS
import pandas as pd



def shortTerm():
    tickers = ["ADANIENT", "ADANIPORTS", "APOLLOHOSP"]  # Example tickers, replace with your list of 50 stocks
    ticker_points = {}

    for t in tickers:
        stock_data = data(t)
        points = bb(stock_data) + WMA(stock_data) + adx(stock_data)
        ticker_points[t] = points

    best_ticker = max(ticker_points, key=ticker_points.get)
    return best_ticker

def backtest_strategy(ticker):
    stock_data = data(ticker)
    closing_prices = stock_data['Close']
    backtest_results = []

    for i in range(0, len(closing_prices)-14, 14):
        max_close = max(closing_prices[i:i+14])
        min_close = min(closing_prices[i:i+14])
        current_close = closing_prices[i+13]

        percentage_profit = ((max_close - current_close) / current_close) * 100
        percentage_loss = ((current_close - min_close) / current_close) * 100

        backtest_results.append({'Percentage_Profit': percentage_profit, 'Percentage_Loss': percentage_loss})

    return backtest_results

if __name__ == '__main__':
    selected_ticker = shortTerm()
    backtest_results = backtest_strategy(selected_ticker)
    print(backtest_results)
