from fastapi import FastAPI
#import predict as p
import pickle

import requests
import pandas as pd
import numpy as np

from os.path import join, dirname

pkl_path = join(dirname(__file__), 'crypto_model.pkl')

#from tensorflow.keras import models
#from tensorflow.keras import layers
#from sklearn.model_selection import train_test_split

def get_crypto_data(crypto_name):

    #sources API coingecko
    url = f"https://api.coingecko.com/api/v3/coins/{crypto_name}/market_chart?vs_currency=usd&days=max&interval=daily"
    response = requests.get(url)
    data = response.json()['prices']

    #creates DataFrame with columns date and price
    df = pd.DataFrame(data, columns=['date', 'price'])
    df['date'] = pd.to_datetime(df['date'], unit='ms')
    df.set_index('date', inplace=True)
    df.index = df.index.date

    df = df.groupby(df.index).max()
    return df

def get_x_y(df):
    price_data = df['price'].values

    #How many previous prices the model will use to predict the target
    past_days = 15

    X = []
    y = []
    for i in range(len(price_data) - past_days):
        X.append(price_data[i:i+past_days])
        y.append(price_data[i+past_days])

    X = np.array(X)
    y = np.array(y)
    X = pd.DataFrame(X)
    y = pd.DataFrame(y)

    return X, y

def price_prediction(df, X, past_days, model):
    # Get the last few prices, dependent on past_days
    latest_prices = df['price'].values[-past_days:]
    X = np.append(X, latest_prices)[-past_days:]

    # Reshape X to match the input shape of the LSTM model
    X = X.reshape((1, past_days, 1))

    #predict next 5 prices
    next_prices = []
    for i in range(5):
        next_price = model.predict(X, verbose = 0)[0][0]
        next_prices.append(next_price)
        X = np.append(X, next_price)[-past_days:]
        X = X.reshape((1, past_days, 1))

    return next_prices

app = FastAPI() # we create a fastapi instance

# Define a root `/` endpoint with a '@' decorator
@app.get('/')
def index():
    # whenever I "get" the "/" root, I have connection: True as a result
    return {'connection': True}

# Creating a new endpoint called predict with params
@app.get('/product') # "get" endpoint again
def product(input_1, input_2):
    # returns the product of two inputs
    product = int(input_1) * int(input_2) # changing str to int
    return {'result': product} # passing a value without parameters for the time being

# Creating a new predict endpoint with the prices predictions
@app.get('/predict')
def predict(coin='bitcoin'):
    # returns the prices in the next X days
    df = get_crypto_data(coin)
    print('data retrieved')
    X, y = get_x_y(df)
    print("x and y defined")
    past_days = 15
    model = pickle.load(open(pkl_path, 'rb'))
    print("model pulled")
    next_prices = price_prediction(df, X, past_days, model)
    print("prices determined")
    next_prices_float = [float(round(i)) for i in next_prices]
    print(type(next_prices_float[0]))
    return {'result': next_prices_float}

if __name__ == '__main__':
    print(pkl_path)
    print(predict())
