
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
    
    
location = 'D:/test/test/'
filename = 'test_code_simple.csv'


#data는 csv로 가져온다 - 종목코드, 진입날짜, 행사가격이 line으로 쌓여있는 csv
raw_data = pd.read_csv(location+filename, dtype=object)


#pykrx에서 데이터 조회


for i in range(len(raw_data)):
    #print(i)
    icode = raw_data.loc[i, 'code']
    start_date = raw_data.loc[i, 'issuedate']
    end_date = get_date(start_date, 30)
    
    init, high, close = get_numbers_from(start_date, end_date, icode)

    raw_data.loc[i, 'initial'] = init
    raw_data.loc[i, 'highest'] = high
    raw_data.loc[i, 'closing'] = close
    

#분석
raw_data['profit_highest'] = (raw_data['highest'] - raw_data['initial']) / raw_data['initial'] - 0.01
raw_data['loss_at_close'] = (raw_data['closing'] - raw_data['initial']) / raw_data['initial'] - 0.01

