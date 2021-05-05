import time
import pyupbit
import datetime
import requests

access = "6PwBHITPpgeLxgj8wUIM6gHzDiixWltrISVyPS7v"        
secret = "UmU3piFu0xJ7xUB3MkVt5BbdVt6DvG0dJ7TZVfVA"
myToken = "xoxb-1991913874982-2007083561303-lwp2UkkgGV2E8t9kCCo1Yky9"


def post_message(token, channel, text):
    response = requests.post("https://slack.com/api/chat.postMessage",
        headers={"Authorization": "Bearer "+token},
        data={"channel": channel,"text": text}
    )

def get_target_price(ticker, k):
    df = pyupbit.get_ohlcv(ticker, interval="minute10", count=5)
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price

def get_start_time(ticker):
    df = pyupbit.get_ohlcv(ticker, interval="minute240", count=1)
    start_time = df.index[0]
    return start_time

def get_ma10(ticker):
    df = pyupbit.get_ohlcv(ticker, interval="minute10", count=30)
    ma10 = df['close'].rolling(window=2).mean()
    return ma10

def get_ma15(ticker):
    df = pyupbit.get_ohlcv(ticker, interval="minute10", count=30)
    ma15 = df['close'].rolling(window=4).mean()
    return ma15

def get_balance(ticker):
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0




def get_current_price(ticker):
    return pyupbit.get_orderbook(tickers=ticker)[0]["orderbook_units"][0]["ask_price"]

# 로그인
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")
# 시작 메세지 슬랙 전송
post_message(myToken,"#stock", "autotrade start")

while True:
    try:
        ma10 = get_ma10("KRW-DOGE")
        ma15 = get_ma15("KRW-DOGE")
        MACD = ma10 - ma15
        MACDP = (ma10-ma15)/ma10*100
        dMACD1=MACD[-1]-MACD[-2]
        dMACD2=MACD[-2]-MACD[-3]
        current_price = get_current_price("KRW-DOGE")

        if dMACD1>0 and dMACD2<0:
            krw = get_balance("KRW")
            if krw > 5000:
                buy_result = upbit.buy_market_order("KRW-DOGE", krw*0.5)
                post_message(myToken,"#stock", "DOGE buy : " +str(buy_result))
                time.sleep(60)
          
                 
        if dMACD1<0 and dMACD2>0:
            btc = get_balance("DOGE")
            if btc > 11:
                sell_result = upbit.sell_market_order("KRW-DOGE", btc*0.5)
                post_message(myToken,"#stock", "DOGE sell : " +str(sell_result))
                time.sleep(60)



    except Exception as e:
        print(e)
        post_message(myToken,"#stock", e)
        time.sleep(1)