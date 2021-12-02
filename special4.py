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
    print(coin, datetime.datetime.now(), "Buy")
    if money > 501000 : 
        res = upbit.buy_market_order(coin, 500000) 
    return

# 시장가 매도 함수 
def sell(coin): 
    amount = upbit.get_balance(coin) 
    cur_price = pyupbit.get_current_price(coin) 
    total = amount * cur_price 
    print(coin, datetime.datetime.now(),"Sold")
    if total > 5000 : 
        res = upbit.sell_market_order(coin, amount) 
    return

# 이용할 코인 리스트 
coinlist = ['KRW-BTC', 'KRW-ETH', 'KRW-HIVE', 'KRW-CRO']
lower28 = []
higher70 = []

# initiate
for i in range(len(coinlist)):
    lower28.append(False)
    higher70.append(False)

while(True):
    for i in range(len(coinlist)):
        try :
            data = pyupbit.get_ohlcv(ticker=coinlist[i], interval="minute3")
            now_rsi = rsi(data, 14).iloc[-1]
            av_buy = float(upbit.get_avg_buy_price(coinlist[i]))
            profit_price = round(av_buy*1.02, 4)   
            cur_price = pyupbit.get_current_price(coinlist[i])   
            amount = upbit.get_balance(coinlist[i])
            total = amount * cur_price
            print(coinlist[i], datetime.datetime.now(), "< RSI30 checking > :", now_rsi)

            if now_rsi <= 28 :
                lower28[i] = True
            elif now_rsi >= 30 and lower28[i] == True and higher70[i] == False :
                buy(coinlist[i])                        
                higher70[i] = True
            elif now_rsi >= 50  :
                lower28[i] = False
                higher70[i] = False
            elif now_rsi _= 65 and cur_price > profit_price and total > 0 :
                sell(coinlist[i])                
            time.sleep(0.2)
            
        except Exception as e:
            print(e)
            time.sleep(0.2)
