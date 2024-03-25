import pandas as pd


def filterByCapital(capital,df):
    
    for tickerSymbol in df.index:
        try:            
            close = df[df.index == tickerSymbol]['close']
            if float(capital) < close.iloc[0]:
                df.drop(tickerSymbol, inplace=True)

        except Exception as e:
            print(e)
    return df