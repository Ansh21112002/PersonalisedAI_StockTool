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
from flask_pymongo import PyMongo
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bcrypt import hashpw, gensalt, checkpw
import random
app = Flask(__name__)
CORS(app)

uri = 'mongodb+srv://team_user_name:team_user_name@clustermain.bcisjhm.mongodb.net/?retryWrites=true&w=majority&appName=ClusterMain'
app.config['MONGO_URI'] = uri
# mongo = PyMongo(app)
# print(f"MongoDB Connection: {mongo.db.client.server_info()}")
client = MongoClient(uri, server_api=ServerApi('1'))

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

users = client['majorproject']['users']

@app.route('/api/auth/signin', methods=['POST'])
def signup():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    capital = data.get('capital')
    email = data.get('email')

    if not username or not password or not capital:
        return jsonify({'error': 'Username, password and capital are required'}), 400

    existing_user = users.find_one({'username': username})
    if existing_user:
        return jsonify({'error': 'Username is already taken, try something more unique!'}), 400

    hashed_password = hashpw(password.encode('utf-8'), gensalt())
    user_id = users.insert_one({
        'username': username,
        'password': hashed_password,
        'capital': capital,
        'starting_capital' : capital,
        'portfolio_value':capital,
        "portfolio":[],
        "email":email,
             
    }).inserted_id

    return jsonify({'user_id': str(user_id)}), 201

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    user = users.find_one({'username': username})
    if not user or not checkpw(password.encode('utf-8'), user['password']):
        return jsonify({'error': 'Invalid credentials'}), 401
    return jsonify({'message': 'Login successful', 'token':str(user.get('_id'))}), 200

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


#BUY AND SELL CONTROLLERS
def update_portfolio_buy(user, symbol, quantity, ltp):
    existing_stock = next((stock for stock in user['portfolio'] if stock['symbol'] == symbol), None)
    if existing_stock:
        existing_quantity = existing_stock['quantity']
        existing_avg_price = existing_stock['avgPrice']
        new_quantity = existing_quantity + quantity
        new_avg_price = ((existing_quantity * existing_avg_price) + (quantity * ltp)) / new_quantity
        existing_stock.update({'quantity': new_quantity, 'avgPrice': new_avg_price})
    else:
        user['portfolio'].append({
            'symbol': symbol,
            'quantity': quantity,
            'avgPrice': ltp
        })

def update_portfolio_sell(user, symbol, quantity, ltp):
    existing_stock = next((stock for stock in user['portfolio'] if stock['symbol'] == symbol), None)
    if existing_stock:
        existing_quantity = existing_stock['quantity']
        if existing_quantity > quantity:
            existing_stock['quantity'] -= quantity
        elif existing_quantity == quantity:
            user['portfolio'].remove(existing_stock)
        else:
            return False  # Insufficient quantity to sell
        return True
    return False  # Stock not found in portfolio

@app.route('/api/stock/buy', methods=['POST'])
def buy_stock():
    data = request.json
    username = data.get('username')
    symbol = data.get('symbol')
    quantity = data.get('quantity')

    if not username or not symbol or quantity is None:
        return jsonify({'error': 'Username, symbol, and quantity are required'}), 400

    user = users.find_one({'username': username})
    if not user:
        return jsonify({'error': 'User not found'}), 404

    # Fetching the latest ticker price (LTP) using a mock API

    # ltp = requests.get(f'https://mock-api.com/ticker/{symbol}').json().get('ltp')
    ltp = random.randint(100, 200)

    if not ltp:
        return jsonify({'error': 'Failed to fetch latest ticker price'}), 500

    total_cost = ltp * quantity
    if total_cost > user['capital']:
        return jsonify({'error': 'Insufficient capital to buy'}), 400

    # Update user's capital and add or update the stock in the portfolio
    new_capital = user['capital'] - total_cost
    update_portfolio_buy(user, symbol, quantity, ltp)

    users.update_one(
        {'username': username},
        {'$set': {'capital': new_capital, 'portfolio': user['portfolio']}}
    )

    return jsonify({'message': 'Stock bought successfully'}), 200

@app.route('/api/stock/sell', methods=['POST'])
def sell_stock():
    data = request.json
    username = data.get('username')
    symbol = data.get('symbol')
    quantity = data.get('quantity')

    if not username or not symbol or quantity is None:
        return jsonify({'error': 'Username, symbol, and quantity are required'}), 400

    user = users.find_one({'username': username})
    if not user:
        return jsonify({'error': 'User not found'}), 404

    # Fetching the latest ticker price (LTP) using a mock API
    # ltp = requests.get(f'https://mock-api.com/ticker/{symbol}').json().get('ltp')
    ltp = random.randint(100, 200)

    if not ltp:
        return jsonify({'error': 'Failed to fetch latest ticker price'}), 500

    if update_portfolio_sell(user, symbol, quantity, ltp):
        total_sale = ltp * quantity
        new_capital = user['capital'] + total_sale

        users.update_one(
            {'username': username},
            {'$set': {'capital': new_capital, 'portfolio': user['portfolio']}}
        )

        return jsonify({'message': 'Stock sold successfully'}), 200
    else:
        return jsonify({'error': 'Insufficient stock to sell'}), 400


if __name__ == '__main__':
    app.run(debug=True)
