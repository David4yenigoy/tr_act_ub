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


# 1. 잔고종목조회
# balances = upbit.get_balances()
# b = []
# for i in range(len(balances)) :
#     a = balances[i]['currency']
#     b.append(a)

# 2. 매도함수

def sell(coin): 
    amount = upbit.get_balance(coin) 
    cur_price = pyupbit.get_current_price(coin) 
    total = amount * cur_price 
    print(coin, datetime.datetime.now(),"Sold", now_rsi)
    if total > 5000 : 
        res = upbit.sell_market_order(coin, amount) 
    return


# 시장가 매수 함수 
def buy(coin): 
    amount = upbit.get_balance(coin) 
    cur_price = pyupbit.get_current_price(coin) 
    total = amount * cur_price 
    money = upbit.get_balance("KRW") 
    print(coin, datetime.datetime.now(), "Buy", now_rsi)
    if money > 51000 and total < 145000 : 
        res = upbit.buy_market_order(coin, 50000) 
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


# coinlist = pyupbit.get_tickers(fiat="KRW")
coinlist = ["KRW-BTC", "KRW-ETH", "KRW-SAND", "KRW-STORJ", "KRW-HIVE", "KRW-XRP", "KRW-BAT", "KRW-GLM", "KRW-MANA", "KRW-BORA", "KRW-PLA", "KRW-HUNT", "KRW-HUM", "KRW-ANKR", "KRW-POWR"] # Coin ticker 추가 
hold_sign = []
hold_sign2 = []

for i in range(len(coinlist)):
    hold_sign.append(False)
    hold_sign2.append(False)

# print(coinlist)    
    
while(True):
    try :
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
        # print(coins)
        for c in range(len(coins)) :
            data = pyupbit.get_ohlcv(ticker=coins[c], interval="minute3")
            now_rsi = rsi(data, 14).iloc[-1]
            av_buy = float(upbit.get_avg_buy_price(coins[c]))
            profit_price = round(av_buy*1.02, 4)   
            cur_price = pyupbit.get_current_price(coins[c]) 
            print(coins[c], datetime.datetime.now(), 'now_rsi', now_rsi)

            if cur_price > profit_price and av_buy > 0 :
                sell(coins[c])               
                time.sleep(0.2)

            # 매수조건 검색
        for i in range(len(coinlist)) :
            data = pyupbit.get_ohlcv(ticker=coinlist[i], interval="minute3")
            now_rsi = rsi(data, 14).iloc[-1]
            cur_price = pyupbit.get_current_price(coinlist[i])   
            print(coinlist[i], "checking rsi", now_rsi)
            if now_rsi <= 35 and hold_sign == False :
                buy(coinlist[i])                        
                hold_sign[i] = True
                if now_rsi <= 28 and hold_sign == True :
                    buy(coinlist[i])
                    hold_sign2[i] = True
                    if now_rsi <= 20 and hold_sign2 == True :
                        buy(coinlist[i])
            elif now_rsi >= 50 :
                hold_sign[i] = False
                hold_sign2[i] = False
                
        time.sleep(0.2)

    except Exception as e:
        print(e)
        time.sleep(0.2)