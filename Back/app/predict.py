import requests
import pandas as pd
import numpy as np

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
