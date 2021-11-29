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


# 시장가 매수 함수 
def buy(coin): 
    amount = upbit.get_balance(coin) 
    cur_price = pyupbit.get_current_price(coin) 
    total = amount * cur_price 
    money = upbit.get_balance("KRW") 
    print(coin, datetime.datetime.now(), "Buy", now_rsi)
    if money > 301000 and total < 300000 : 
        res = upbit.buy_market_order(coin, 300000) 
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


coinlist = pyupbit.get_tickers(fiat="KRW")        
dic_01 ={}

now = datetime.datetime.now()
start_time = get_start_time('KRW-BTC')
end_time = start_time + datetime.timedelta(days=1)

if start_time < now :
    for i in range(len(coinlist)):
        df = pyupbit.get_ohlcv(coinlist[i], interval="day", count=2)
        volatile = (df.iloc[0]['high'] - df.iloc[0]['low']) / df.iloc[0]['open'] * 100

        if volatile >= 10 :
            dic_01[coinlist[i]] = volatile                
            time.sleep(0.3)

    a = sorted(dic_01.items(), key=lambda dic_01: dic_01[1], reverse=True)
    targetlist = [t[0] for t in a][:10]
    print(now,
          targetlist)

    
while(True):
    try :
        now = datetime.datetime.now()
        start_time = get_start_time('KRW-BTC')
        end_time = start_time + datetime.timedelta(days=1)

        if start_time < now < end_time - datetime.timedelta(seconds=180): 
            print(now)
            # 매수조건 검색
            hold_sign = []
            hold_sign2 = []
            hold_sign3 = []

            for i in range(len(targetlist)) :
                hold_sign.append(False)
                hold_sign2.append(False)
                hold_sign3.append(False)

                data = pyupbit.get_ohlcv(ticker=targetlist[i], interval="minute3")
                now_rsi = rsi(data, 14).iloc[-1]
                cur_price = pyupbit.get_current_price(targetlist[i])   
                print(targetlist[i], datetime.datetime.now(), "checking rsi", now_rsi)

                if now_rsi <= 28 and hold_sign[i] == False and hold_sign3[i] == False :
                    buy(targetlist[i])                        
                    hold_sign[i] = True
                    hold_sign3[i] = True
                elif now_rsi <= 20 and hold_sign[i] == True and hold_sign3[i] == True :
                    buy(targetlist[i])
                    hold_sign[i] = False
                    hold_sign2[i] = True
                elif now_rsi <= 15 and hold_sign2[i] == True :
                    buy(targetlist[i])
                    hold_sign2[i] = False
                elif now_rsi >= 60 :
                    hold_sign[i] = False
                    hold_sign2[i] = False
                    hold_sign3[i] = False
                time.sleep(0.5)

    except Exception as e:
        print(e)
        time.sleep(0.2)