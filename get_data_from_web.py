
import pandas as pd
import csv
#먼저 pykrx 그다음 yfinance 마지막은 googlefinance..?
from pykrx import stock
import yfinance as yf
#날짜 계산을 위한 numpy, 및 지연을 위한 time
import numpy as np
import time 


#시작일로부터 period만큼 후의 날짜 생성
def get_date(start, period):
    date1 = np.array(start, dtype="datetime64[D]")
    date2 = date1 + period
    end = str(date2)

    return end


#진입가, 기간내 최고가, 클로징종가 
def get_numbers_from(start, end, code):
    df = stock.get_market_ohlcv(start, end, code)
    #df = stock.get_market_ohlcv(start_date, end_date, 377480)
    time.sleep(1)
    initial = df['시가'].iloc[0]
    highest = max(df['고가'])
    closing = df['종가'].iloc[-1]
    
    return initial, highest, closing


def back_test(raw_data, harvest_profit, period):
    #대략 백테스트라고...
    summarine_profit = 0
    for i in range(len(raw_data)):
        if raw_data.loc[i, 'upper_room'] > 1:
            if raw_data.loc[i, 'profit_highest'] > harvest_profit:
                summarine_profit = summarine_profit + harvest_profit
            else:
                summarine_profit = summarine_profit + raw_data.loc[i, 'loss_at_close']
    
    print("이익률 " + str(harvest_profit) + ", " + str(period) + "일 적용된 수익률 : " + str(round(summarine_profit, 5) * 100))
    
    return summarine_profit


def data_from_pykrx(raw_data, period, tax):
    for i in range(len(raw_data)):
        icode = raw_data.loc[i, 'code']
        print("get from pykrx for period " + str(period) +"일 기간 --> " + str(i) + "/" + str(len(raw_data)) + "종목")
        
        start_date = raw_data.loc[i, 'issuedate']
        end_date = get_date(start_date, period)
        
        init, high, close = get_numbers_from(start_date, end_date, icode)

        raw_data.loc[i, 'initial'] = init
        raw_data.loc[i, 'highest'] = high
        raw_data.loc[i, 'closing'] = close
        
    raw_data['upper_room'] = raw_data['strike_price'] / raw_data['initial']
    raw_data['profit_highest'] = (raw_data['highest'] - raw_data['initial']) / raw_data['initial'] - tax
    raw_data['loss_at_close'] = (raw_data['closing'] - raw_data['initial']) / raw_data['initial'] - tax
    
    return raw_data
    
    
location = 'D:/test/test/'
filename = 'test_code_simple.csv'
#harvest_profit = 0.05
#period = 60
final = pd.DataFrame()
#이게 참....period에 맞춰서 한번 뿌리면 harvest_profit에 대한 분석은 쉽다....
#그러면 period에 의해 가져오는 함수 하나, df를 받아서 분석하는 함수 하나....
tax = 0.005

#data는 csv로 가져온다 - 종목코드, 진입날짜, 행사가격이 line으로 쌓여있는 csv
raw_data = pd.read_csv(location+filename, dtype=object)
raw_data = raw_data.astype({'strike_price':'int32'})



for period in range(1, 3):
    data_from_pykrx(raw_data, period, tax)
    
    for harvest_profit in range(1, 10):
        harvest_profit_ratio = harvest_profit / 100
        
    
        final.loc[period, harvest_profit] = back_test(raw_data, harvest_profit_ratio, period)