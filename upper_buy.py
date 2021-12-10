import pyupbit 
import pandas 
import datetime 
import time

access = ''
secret = ''

upbit = pyupbit.Upbit(access, secret)

def rsi(ohlc: pandas.DataFrame, period: int = 14):
    delta = ohlc["close"].diff()
    ups, downs = delta.copy(), delta.copy()
    ups[ups < 0] = 0 
    downs[downs > 0] = 0
    
    AU = ups.ewm(com = period-1, min_periods = period).mean() 
    AD = downs.abs().ewm(com = period-1, min_periods = period).mean() 
    RS = AU/AD

    return pandas.Series(100 - (100/(1 + RS)), name = "RSI")


# 시장가 매수 함수 
def buy(coin): 
    money = upbit.get_balance("KRW")
    amount = upbit.get_balance(coin) 
    cur_price = pyupbit.get_current_price(coin) 
    total = amount * cur_price 
    print(coin, datetime.datetime.now(),"Buy_G")
    if money > 100500 and total < 850000 : 
        res = upbit.buy_market_order(coin, 100000)     
    return

# 이용할 코인 리스트 
coinlist = pyupbit.get_tickers(fiat="KRW")

# initiate
higher2 = []

for i in range(len(coinlist)):    
    higher2.append(True)

while(True):
    for i in range(len(coinlist)):
        try: 
            data = pyupbit.get_ohlcv(ticker=coinlist[i], interval="minute30")
            now_rsi = rsi(data, 14).iloc[-1]           
        
            elif now_rsi >= 65 and now_rsi <= 70 and higher2[i] == False :
                buy(coinlist[i])
                higher2[i] = True
            elif now_rsi <= 55 and higher2[i] == True :
                higher2[i] = False
                
            time.sleep(0.1)
            
        except Exception as e:
            print(e)
            time.sleep(0.2)
