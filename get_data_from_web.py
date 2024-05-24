
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


#기간내 최고가와 클로징종가 
def get_numbers_from(start, end, code):
    df = stock.get_market_ohlcv(start, end, code)
    time.sleep(1)
    highest = max(df['고가'])
    closing = df['종가'].iloc[-1]
    
    return highest, closing
    
    
location = 'D:/test/test/'
filename = 'test_code_simple.csv'


#data는 csv로 가져온다 - 종목코드, 진입날짜, 행사가격이 line으로 쌓여있는 csv
raw_data = pd.read_csv(location+filename, dtype=object)


#pykrx에서 데이터 조회
start_date = "2024-01-02"
end_date = get_date(start_date, 30)


for i in range(len(raw_data)):
    #print(i)
    icode = raw_data.loc[i, 'code']
    
    high, close = get_numbers_from(start_date, end_date, icode)

    raw_data.loc[i, 'highest'] = high
    raw_data.loc[i, 'closing'] = close
    
    #print(high, close) 


#data.info()
#data.columns
#1#번
#필요한 데이터만 남기기(회사명, 종목코드, 진입날짜, 진입가, 행사가, 어퍼, 최고가, 최고비율)
data = data.drop(columns = ["결의일", "결의일종가", "현재가", "진입가시총", "탈출가능?", "기간내최저가", "최저비율"])
#NaN 삭제(행 삭제)
data = data.dropna()


#데이터 cleaning
data['진입날짜'] = pd.to_datetime(data['진입날짜'])
data['진입가'] = data['진입가'].astype('int64')
data['행사가'] = data['행사가'].astype('int64')
data['기간내최고가'] = data['기간내최고가'].astype('int64')

#데이터 만들기(퍼센트 변환이 귀찮아서 그냥 새로 만듬(이게더 나음))
data['어퍼룸'] = (data['행사가'] -  data['진입가']) / data['진입가']
data['최고비율'] = (data['기간내최고가'] -  data['진입가']) / data['진입가']




#count로 세기 NaN은 세지 않는다고 함(size는 NaN도 포함해서 센다고 함)
#data.count()
data['회사명'].count()

data[data['최고비율']>=0.1].count()