import json
from flask import Flask, request, jsonify
from API import data
from Shortterm import*
from Longterm import *
from Midterm import*
from CONSTANTS import *
from NewsAPI import *
from flask_cors import CORS
import pandas as pd

app = Flask(__name__)
CORS(app)


@app.route("/",methods = ['GET'])
def index():
    return "This whould be working fine!"


@app.route('/shortterm', methods=['GET'])
def shortTerm():
    ticker_points = {}
    
    for t in ticker:
        stock_data = data(t + ".NS")
        points = bb(stock_data) + WMA(stock_data) + adx(stock_data)
        ticker_points[t] = points
    return jsonify(ticker_points)

@app.route('/midterm', methods=['GET'])
def midTerm():
    ticker_points = {}
    
    for t in ticker:
        stock_data = data(t + ".NS")
        points = RSI(stock_data) + adx(stock_data) + OBV(stock_data)
        ticker_points[t] = points
    return jsonify(ticker_points)

@app.route('/longterm', methods=['GET'])
def longterm():
    stock_data = pd.read_excel('Fundamentals.xlsx', index_col='Symbol')
    stock_data['weights'] = 0
    EBIDTA(stock_data)
    alpha_beta(stock_data)
    PE(stock_data)
    Current(stock_data)
    NPM(stock_data)
    ROE(stock_data)
    Market_Cap(stock_data)

    
    weights_dict = stock_data['weights'].to_dict()

    
    return jsonify(weights_dict)


@app.route('/data/<ticker_name>', methods=['GET'])
def stock_data(ticker_name):
    formatted_data = []

    dataframe = data(ticker_name)

    formatted_data = []

    for index, row in dataframe.iterrows():
        index_datetime = pd.to_datetime(index)
        
        unix_epoch = int(index_datetime.timestamp() * 1000)
        
        data_point = {
            'x': unix_epoch,
            'y': [row['Open'], row['High'], row['Low'], row['Close']]
        }
        formatted_data.append(data_point)

    json_data = json.dumps(formatted_data)

    return json_data


@app.route('/newsAndIndicators/<ticker_name>', methods=['GET'])
def nAI(ticker_name):
    stock_data = data(ticker_name + ".NS")
    ####RSI####
    
    rsi_dataframe = RSI_data(stock_data)
    json_response_RSI = rsi_dataframe.to_json(orient='records')

    ###WMA####
    wma=WMA_data(stock_data)
    json_response_WMA = json.dumps(wma)

    ###NEWS####
    news=getNews(ticker_name)
    json_response_NEWS = json.dumps(news)

    ####timestamps####
    ts=timestamp(stock_data)
    json_response_timestamp=json.dumps(ts)

    ####adx####
    adxd=adx_data(stock_data)
    json_response_adx=json.dumps(adxd)

    ####bb####
    bbd=bb_data(stock_data)
    json_response_bb=json.dumps(bbd)



    combined_response = {
        "TimeStamp":json_response_timestamp,
        "RSI": json_response_RSI,
        "NEWS": json_response_NEWS,
        "WMA":json_response_WMA,
        "ADX":json_response_adx,
        "bb":json_response_bb
    }

    return jsonify(combined_response)



if __name__ == '__main__':
    app.run(debug=True)
