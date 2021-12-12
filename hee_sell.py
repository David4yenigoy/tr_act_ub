import pyupbit 
import pandas 
import datetime 
import time
from pytz import timezone


access = ''
secret = ''

upbit = pyupbit.Upbit(access, secret)

# 2. 매도함수

def sell(coin): 
    amount = upbit.get_balance(coin) 
    cur_price = pyupbit.get_current_price(coin) 
    total = amount * cur_price 
    print(coin, datetime.datetime.now(timezone('Asia/Seoul')),"Sold", now_rsi)
    if total > 5000 : 
        res = upbit.sell_market_order(coin, amount) 
    return

def rsi(ohlc: pandas.DataFrame, period: int = 14):
    delta = ohlc["close"].diff()
    ups, downs = delta.copy(), delta.copy()
    ups[ups < 0] = 0 
    downs[downs > 0] = 0
    
    AU = ups.ewm(com = period-1, min_periods = period).mean() 
    AD = downs.abs().ewm(com = period-1, min_periods = period).mean()
    RS = AU/AD

    return pandas.Series(100 - (100/(1 + RS)), name = "RSI")

def get_start_time(ticker):
    """시작 시간 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
    start_time = df.index[0]
    return start_time

    
while(True):
    try :
        now = datetime.datetime.now()
        # 매도조건 판단
        balances = upbit.get_balances()
        coins = []
        for i in range(len(balances)) :
            a = balances[i]['currency']
            coins.append('KRW-'+ a )                   
        coins.remove('KRW-KRW')
        coins.remove('KRW-VTHO')
        coins.remove('KRW-XYM')
        coins.remove('KRW-APENFT')
        
        check1 = []
        check2 = []
        check3 = []

        for c in range(len(coins)) :
            check1.append(False)
            check2.append(False)
            check3.append(False)
            
            av_buy = float(upbit.get_avg_buy_price(coins[c]))
            profit_price = round(av_buy*1.015, 4)
            cur_price = pyupbit.get_current_price(coins[c])

            if cur_price > round(av_buy*1.02, 4) and check1[c] == False :
                check1[c] = True
            elif cur_price > round(av_buy*1.03, 4) and check2[c] == False :
                check2[c] = True
            elif cur_price > round(av_buy*1.05, 4) and check3[c] == False :
                check3[c] = True
            elif cur_price > round(av_buy*1.07, 4) :
                sell(coins[c])
            elif cur_price <= round(av_buy*1.05, 4) and check3[c] == True :
                sell(coins[c])
            elif cur_price <= round(av_buy*1.03, 4) and check2[c] == True :
                sell(coins[c])
            elif cur_price <= round(av_buy*1.02, 4) and check1[c] == True :
                sell(coins[c])
            elif cur_price >= profit_price and check1[c] == False and av_buy > 0 :
                sell(coins[c])            
            time.sleep(0.1)

    except Exception as e:
        print(e)
        time.sleep(0.2)
