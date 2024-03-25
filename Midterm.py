import ta
from API import data

def RSI(df):
   RSI= ta.momentum.RSIIndicator(close=df['Close'],window=14,fillna=True).rsi()
   if RSI.iloc[-1]<30:
      return 2
   elif RSI.iloc[-1]<50:
      return 1
   return 0

def RSI_data(df):
   return ta.momentum.RSIIndicator(close=df['Close'],window=14,fillna=True).rsi()
  
def OBV(df):
  obv = ta.volume.OnBalanceVolumeIndicator(close=df['Close'],volume=df['Volume'],fillna=False).on_balance_volume()
  
  obv_current = obv.iloc[-1]  
  obv_past = obv.iloc[-14]  

  percentage_change = ((obv_current - obv_past) / obv_past) * 100

  if percentage_change<0:
     return 0
  elif percentage_change<15:
     return 1
  elif percentage_change<50:
     return 2
  return 3


