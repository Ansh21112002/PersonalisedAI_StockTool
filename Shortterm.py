import ta
# from API import data

# stock_data = data("ONGC.NS")

def bb(df):
    indicator_bb = ta.volatility.BollingerBands(
        df['Close'], window=10, window_dev=2)
    width = indicator_bb.bollinger_wband()
    current_width = width[len(width)-1]
    prv_width = width[len(width)-2]
    pr_chng = ((current_width-prv_width)/prv_width)*100
    if pr_chng <= 0:
        return 0
    elif pr_chng <= 25:
        return 1
    elif pr_chng <= 50:
        return 2
    elif pr_chng <= 75:
        return 3
    else:
        return 4
    

def adx(df):
    df['adx'] = ta.trend.ADXIndicator(
        df['High'], df['Low'], df['Close'], window=14).adx()
    # df['adx'] = adx
    df['+DI'] = ta.trend.ADXIndicator(
        df['High'], df['Low'], df['Close'], window=14).adx_pos()
    df['-DI'] = ta.trend.ADXIndicator(
        df['High'], df['Low'], df['Close'], window=14).adx_neg()
    if df['adx'][len(df)-1] >= 20 and df['+DI'][len(df)-1] > df['-DI'][len(df)-1]:
        return 1
    return 0



def WMA(df):
  wma_13 = ta.trend.WMAIndicator(close=df['Close'],window=13,fillna=True).wma()
  wma_55 = ta.trend.WMAIndicator(close=df['Close'],window=55,fillna=True).wma()
  if(wma_13.iloc[-1]>wma_55.iloc[-1]):
    return 1
  else:
    return 0
  

def WMA_data(df):
    wma_13 = ta.trend.WMAIndicator(close=df['Close'], window=13, fillna=True).wma()
    wma_55 = ta.trend.WMAIndicator(close=df['Close'], window=55, fillna=True).wma()

    # Extracting values
    wma_13_values = wma_13.values
    wma_55_values = wma_55.values

    wma_dict = {
        "WMA_13": list(wma_13_values),
        "WMA_55": list(wma_55_values)
    }

    return wma_dict



def adx_data(df):
    adx = ta.trend.ADXIndicator(
        df['High'], df['Low'], df['Close'], window=14).adx()
    pos_DI = ta.trend.ADXIndicator(
        df['High'], df['Low'], df['Close'], window=14).adx_pos()
    neg_DI = ta.trend.ADXIndicator(
        df['High'], df['Low'], df['Close'], window=14).adx_neg()
    
    adx_dict = {
        "ADX": list(adx),
        "Pos_DI": list(pos_DI),
        "Neg_DI": list(neg_DI)
    }

    return adx_dict

def bb_data(df):
    indicator_bb = ta.volatility.BollingerBands(
        df['Close'], window=10, window_dev=2)
    
    uband=indicator_bb.bollinger_hband()
    lband=indicator_bb.bollinger_lband() 
    mband=indicator_bb.bollinger_mavg() 

    bb_dict = {
        "Upper_Band": list(uband),
        "Lower_Band": list(lband),
        "Middle_Band": list(mband)
    }

    return bb_dict





def timestamp(df):
    wma = ta.trend.WMAIndicator(close=df['Close'], window=13, fillna=True).wma()
    wma_reset = wma.reset_index()
    wma_reset['Date'] = wma_reset['Date'].astype(str)
    timestamps = wma_reset['Date'].tolist()

    return timestamps


# print(WMA_data(stock_data))
