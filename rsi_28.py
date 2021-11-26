import pyupbit 
import pandas 
import datetime 
import time

f = open("./phmemo.txt")
lines = f.readlines()
access = lines[1].strip()   # access key
secret = lines[3].strip()   # secret key
f.close()

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
    if money > 21000 : 
        res = upbit.buy_market_order(coin, 20000) 
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
coinlist = pyupbit.get_tickers(fiat="KRW")
lower28 = []
hold_sign = []

# initiate
for i in range(len(coinlist)):
    lower28.append(False)
    hold_sign.append(False)

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
            # print(coinlist[i], "현재시간: ", datetime.datetime.now(), "< RSI > :", now_rsi)

            if now_rsi <= 28 and hold_sign == False and total <= 95000 :
                buy(coinlist[i])                        
                hold_sign[i] = True
                if now_rsi <= 20 and hold_sign == True and total <= 95000 :
                    buy(coinlist[i])                        
                    hold_sign[i] = True
            elif cur_price > profit_price and total > 0 :
                sell(coinlist[i])
                hold_sign[i] = False
            time.sleep(0.2)
            
        except Exception as e:
            print(e)
            time.sleep(0.2)
