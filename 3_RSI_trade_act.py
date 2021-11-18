import pyupbit 
import pandas 
import datetime 
import time

access = "access key"   # access key
secret = "secret key"   # secret key

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


# 이용할 코인 리스트 
coinlist = ["KRW-BTC", "KRW-XRP", "KRW-ETC", "KRW-ETH", "KRW-POWR", "KRW-CRO", "KRW-VET", "KRW-AQT", "KRW-AXS", "KRW-EOS", "KRW-BORA", "KRW-PLA", "KRW-WAXP", "KRW-MANA", "KRW-SAND", "KRW-XEC", "KRW-HIVE", "KRW-HUNT", "KRW-DOGE", "KRW-CHZ", "KRW-ADA", "KRW-CRO", "KRW-DOT"] # Coin ticker 추가 
lower28 = []
higher70 = []

# 시장가 매수 함수 
def buy(coin): 
    money = upbit.get_balance("KRW") 
    if money > 101000 : 
        res = upbit.buy_market_order(coin, 100000) 
#     elif money < 100000: 
#         res = upbit.buy_market_order(coin, money*0.9) 
#     elif money < 250000 : 
#         res = upbit.buy_market_order(coin, money*0.6) 
#     else : 
#         res = upbit.buy_market_order(coin, money*0.4) 
    return

# 시장가 매도 함수 
def sell(coin): 
    amount = upbit.get_balance(coin) 
    cur_price = pyupbit.get_current_price(coin) 
    total = amount * cur_price 
    if total < 1000000 : 
        res = upbit.sell_market_order(coin, amount) 
#     elif total > 1000000: 
#         res = upbit.sell_market_order(coin, amount*0.5) 
    else : 
        res = upbit.sell_market_order(coin, amount*0,7) 
    return

# initiate
for i in range(len(coinlist)):
    lower28.append(False)
    higher70.append(False)

while(True):
    for i in range(len(coinlist)):
        data = pyupbit.get_ohlcv(ticker=coinlist[i], interval="minute3")
        now_rsi = rsi(data, 14).iloc[-1]
        print(coinlist[i], "현재시간: ", datetime.datetime.now(), "< RSI > :", now_rsi)
        print()
        # balances = upbit.get_balances()
        # print("현재시간: ", datetime.datetime.now(), balances)
        if now_rsi <= 28 :
            lower28[i] = True
        elif now_rsi >= 33 and lower28[i] == True:
            buy(coinlist[i])
            lower28[i] = False
        elif now_rsi >= 60 and higher70[i] == False:
            sell(coinlist[i])
            higher70[i] = True
        else now_rsi <= 50 :
            higher70[i] = False
    time.sleep(5)
