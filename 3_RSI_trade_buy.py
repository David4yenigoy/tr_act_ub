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
    if money > 50500 and total < 450000 : 
        res = upbit.buy_market_order(coin, 50000)     
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

# 이용할 코인 리스트 
# coinlist = ["KRW-BTC", "KRW-XRP", "KRW-ETC", "KRW-ETH", "KRW-POWR", "KRW-CRO", "KRW-VET", "KRW-AQT", "KRW-AXS", "KRW-EOS", "KRW-BORA", "KRW-PLA", "KRW-WAXP", "KRW-MANA", "KRW-SAND", "KRW-QKC", "KRW-HIVE", "KRW-HUNT", "KRW-DOGE", "KRW-CHZ", "KRW-ADA", "KRW-MOC", "KRW-DOT"] # Coin ticker 추가 
coinlist = pyupbit.get_tickers(fiat="KRW")

# initiate
lower28 = []
higher70 = []
higher2 = []

for i in range(len(coinlist)):
    lower28.append(False)
    higher70.append(False)    
    higher2.append(True)

while(True):
    for i in range(len(coinlist)):
        try: 
            data = pyupbit.get_ohlcv(ticker=coinlist[i], interval="minute30")
            now_rsi = rsi(data, 14).iloc[-1]           
            df = pyupbit.get_ohlcv(ticker=coinlist[i], interval="minute30", count = 5)
            recent_price = df.iloc[-2]
            now_price = df.iloc[-1]
            recent_volume = recent_price['volume']
            now_volume = now_price['volume']
            av_buy = float(upbit.get_avg_buy_price(coinlist[i]))
            cur_price = pyupbit.get_current_price(coinlist[i])
            # print(coinlist[i], "현재시간: ", datetime.datetime.now(), "< RSI > :", now_rsi)            
        
            if now_rsi <= 28 :
                lower28[i] = True
            elif now_rsi >= 30 and lower28[i] == True and higher70[i] == False :
                buy(coinlist[i])
                higher70[i] = True
                
            elif now_rsi >= 65 and now_rsi <= 70 and higher2[i] == False and now_volume >= recent_volume :
                buy(coinlist[i])
                higher2[i] = True
            elif now_rsi <= 55 and higher2[i] == True :
                higher2[i] = False
                            
            elif now_rsi >= 50 :
                lower28[i] = False
                higher70[i] = False
            elif av_buy*0.9 >= cur_price and now_rsi <= 28 :
                buy(coinlist[i])
                
            time.sleep(0.1)
            
        except Exception as e:
            print(e)
            time.sleep(0.2)
