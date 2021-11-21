import pyupbit 
import pandas 
import datetime 
import time


access = "access key"   
secret = "secret key"   

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
coinlist = ["KRW-BTC", "KRW-XRP", "KRW-ETC", "KRW-ETH", "KRW-POWR", "KRW-CRO", "KRW-VET", "KRW-AQT", "KRW-AXS", "KRW-EOS", "KRW-BORA", "KRW-PLA", "KRW-WAXP", "KRW-MANA", "KRW-SAND", "KRW-QKC", "KRW-HIVE", "KRW-HUNT", "KRW-DOGE", "KRW-CHZ", "KRW-ADA", "KRW-MOC", "KRW-DOT"] # Coin ticker 추가 
r30_lower28 = []
r30_higher70 = []
lower28 = []
higher70 = []
r30_hold = []

# 시장가 매수 함수 
def buy(coin): 
    money = upbit.get_balance("KRW")

    if money > 50500 : 
        res = upbit.buy_market_order(coin, 50000) 
        print(coin, datetime.datetime.now(), "buy")
    return

    
# 시장가 매도 함수 
def sell(coin): 
    amount = upbit.get_balance(coin) 
    cur_price = pyupbit.get_current_price(coin) 
    total = amount * cur_price 
    
    if total > 5000 : 
        res = upbit.sell_market_order(coin, amount) 
        print(coin, datetime.datetime.now(), "sold")
    return


# initiate
for i in range(len(coinlist)):
    lower28.append(False)
    higher70.append(False)
    r30_lower28.append(False)
    r30_higher70.append(False)
    r30_hold.append(False)
    
while(True):
    for i in range(len(coinlist)):
        try:
            data_1 = pyupbit.get_ohlcv(ticker=coinlist[i], interval="minute30")
            now_rsi_30 = rsi(data_1, 14).iloc[-1]
            data_2 = pyupbit.get_ohlcv(ticker=coinlist[i], interval="minute3")
            now_rsi_3 = rsi(data_2, 14).iloc[-1]
            amount = upbit.get_balance(coinlist[i])
            av_buy = float(upbit.get_avg_buy_price(coinlist[i]))
            profit_price = round(av_buy*1.02, 4)   
            cur_price = pyupbit.get_current_price(coinlist[i]) 
            total = amount * cur_price
            print(coinlist[i], datetime.datetime.now(), "< RSI 3 > :", now_rsi_3)
            
            if now_rsi_30 <= 30 :
                r30_lower28[i] = True
            elif now_rsi_30 >= 33 and total < 110000 and r30_lower28[i] == True :
                buy(coinlist[i])
                r30_lower28[i] = False
                r30_hold = True
                print(coin, datetime.datetime.now(), "buy")
            elif now_rsi_30 >= 60 and cur_price >= profit_price and r30_higher70[i] == False :
                sell(coinlist[i])
                higher70[i] = True
                r30_hold = False
                print(coin, datetime.datetime.now(), "sold")
            elif now_rsi_30 <= 50 :
                higher70[i] = False
            
            elif now_rsi_3 <= 30 :
                lower28[i] = True
            elif now_rsi_3 >= 33 and total < 110000 and lower28[i] == True and r30_hold == False :
                buy(coinlist[i])
                lower28[i] = False
                print(coin, datetime.datetime.now(), "buy")
            elif now_rsi_3 >= 60 and cur_price >= profit_price and higher70[i] == False and r30_hold == False :
                sell(coinlist[i])
                higher70[i] = True
                print(coin, datetime.datetime.now(), "sold")
            elif now_rsi_3 <= 50 :
                higher70[i] = False
            time.sleep(0.2)
            
        except Exception as e:
            print(e)
            time.sleep(0.1)
