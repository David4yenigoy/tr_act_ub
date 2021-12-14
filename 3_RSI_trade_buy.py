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
    print(coin, datetime.datetime.now(),"Buy_G", now_rsi)
    if money > 600000 and total < 900000 :
        res = upbit.buy_market_order(coin, 300000)
    elif money > 100500 and total < 900000:
        res = upbit.buy_market_order(coin, 100000)
    return

def buy2(coin):
    money = upbit.get_balance("KRW")
    print(coin, datetime.datetime.now(),"Buy_BTC")
    if money > 10100 :
        res = upbit.buy_market_order(coin, 10000)
    return

def buy3(coin) :
    money = upbit.get_balance("KRW")
    print(coin, datetime.datetime.now(), "Buy_BTC_rsi")
    if money > 30300 :
        res = upbit.buy_market_order(coin, 30000)
    return

# 시장가 매도 함수 
def sell(coin): 
    amount = upbit.get_balance(coin) 
    cur_price = pyupbit.get_current_price(coin) 
    total = amount * cur_price 
    print(coin, datetime.datetime.now(),"Sold_G")
    if total > 5000 : 
        res = upbit.sell_market_order(coin, amount) 
    return

# 거래량 체크
def check_volume(coin):        
    df = pyupbit.get_ohlcv(coin, interval="minute30", count = 5)
    recent_price = df.iloc[-2]
    now_price = df.iloc[-1]
    recent_volume = recent_price['volume']
    now_volume = now_price['volume']
    if now_volume >= recent_volume :
        check_volume = True
    return

def get_ma10(coin):
    df = pyupbit.get_ohlcv(coin, interval="day", count=15)
    ma10 = df['close'].rolling(10).mean().iloc[-1]
    return ma10


# 이용할 코인 리스트 
# coinlist = ["KRW-BTC", "KRW-XRP", "KRW-ETC", "KRW-ETH", "KRW-POWR", "KRW-CRO", "KRW-VET", "KRW-AQT", "KRW-AXS", "KRW-EOS", "KRW-BORA", "KRW-PLA", "KRW-WAXP", "KRW-MANA", "KRW-SAND", "KRW-QKC", "KRW-HIVE", "KRW-HUNT", "KRW-DOGE", "KRW-CHZ", "KRW-ADA", "KRW-MOC", "KRW-DOT"] # Coin ticker 추가 
coinlist = pyupbit.get_tickers(fiat="KRW")

# initiate

lower28 = []
higher70 = []
higher1 = []
higher2 = []
btc_buy = []
btc_buy_down = []
btc_rsi = []
btc_rsi2 = []
btc_rsi_high = []
btc_down = []
btc_down2 = []
btc_down3 = []

for i in range(len(coinlist)):
    lower28.append(False)
    higher70.append(False)
    higher1.append(True)
    higher2.append(True)
    btc_buy.append(False)
    btc_buy_down.append(False)
    btc_rsi.append(False)
    btc_rsi2.append(False)
    btc_rsi_high.append(False)
    btc_down.append(False)
    btc_down2.append(False)
    btc_down3.append(False)

while(True):
    try :
        df = pyupbit.get_ohlcv('KRW-BTC', interval="day", count=15)
        ma10 = df['close'].rolling(10).mean().iloc[-1]
        df2 = pyupbit.get_ohlcv(ticker='KRW-BTC', interval="minute30", count = 5)
        recent_price = df2.iloc[-2]['close']
        recent_price2 = df2.iloc[-3]['close']
        recent_price3 = df2.iloc[-4]['close']
        start_time = df2.index[-1]
        now = datetime.datetime.now() #+ datetime.timedelta(hours=9)
        data_btc = pyupbit.get_ohlcv(ticker='KRW-BTC', interval="minute30")
        now_rsi_btc = rsi(data_btc, 14).iloc[-1]

        if ma10 < pyupbit.get_current_price("KRW-BTC") :
            for i in range(len(coinlist)):
                data = pyupbit.get_ohlcv(ticker=coinlist[i], interval="minute30")
                now_rsi = rsi(data, 14).iloc[-1]
                if now_rsi >= 65 and now_rsi <= 70 and higher2[i] == False :
                    buy(coinlist[i])
                    higher2[i] = True
                elif now_rsi >= 75 and higher1[i] == False :
                    buy(coinlist[i])
                    higher1[i] = True
                elif now_rsi <= 65 and higher1[i] == True :
                    higher1[i] = False
                elif now_rsi <= 55 and higher2[i] == True :
                    higher2[i] = False
                elif now_rsi <= 28 :
                    lower28[i] = True
                elif now_rsi >= 30 and lower28[i] == True and higher70[i] == False :
                    buy(coinlist[i])
                    higher70[i] = True
                elif now_rsi >= 65 and now_rsi <= 70 and higher2[i] == False :
                    buy(coinlist[i])
                    higher2[i] = True
                elif now_rsi <= 55 and higher2[i] == True :
                    higher2[i] = False
                elif now_rsi >= 50 :
                    lower28[i] = False
                    higher70[i] = False
                time.sleep(0.1)
            time.sleep(15)
             
        elif ma10 > pyupbit.get_current_price('KRW-BTC') :
            cur_p_btc = pyupbit.get_current_price('KRW-BTC')

            if btc_buy == False and start_time + datetime.timedelta(seconds=1650) < now < start_time + datetime.timedelta(seconds=1750) and recent_price > cur_p_btc :
                buy2('KRW-BTC')
                btc_buy = True
            elif recent_price3 > recent_price2 > recent_price > cur_p_btc and btc_buy_down == False :
                buy2('KRW-BTC')
                buy2('KRW-BTC')
                btc_buy_down = True

            elif start_time + datetime.timedelta(seconds=1750) < now :
                btc_buy = False
            elif recent_price * 0.99 > cur_p_btc and btc_buy == False :
                buy2('KRW-BTC')
                btc_buy = True
            elif recent_price * 0.985 > cur_p_btc and btc_down == False :
                buy2('KRW-BTC')
                btc_down = True
            elif recent_price * 0.98 > cur_p_btc and btc_down2 == False :
                buy2('KRW-BTC')
                btc_down2 = True
            elif recent_price * 0.97 > cur_p_btc and btc_down3 == False :
                buy3('KRW-BTC')
                btc_down3 = True
            elif recent_price < cur_p_btc :
                btc_down = False
                btc_down2 = False
                btc_down3 = False
            elif recent_price > recent_price2 :
                btc_buy_down = False

            elif btc_rsi == False and now_rsi_btc <= 30 and start_time < now < start_time + datetime.timedelta(seconds=1750):
                buy3('KRW-BTC')
                btc_rsi = True

            elif btc_rsi2 == True and now_rsi_btc > 28 and btc_rsi_high == False :
                buy3('KRW-BTC')
                btc_rsi_high = True

            elif now_rsi_btc > 50 or start_time + datetime.timedelta(seconds=1750) < now :
                btc_rsi = False
                btc_rsi2 = False
                btc_rsi_high = False
                #print('start : ', start_time)
                #print('checking : ', now)
            time.sleep(15)

        else :
            #print('sleep', now)
            time.sleep(15)

    except Exception as e:
    print(e)
    time.sleep(0.2)


