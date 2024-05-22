
import pandas as pd
import csv
import yfinance as yf

#data는 csv로 가져온다 - 종목코드, 진입날짜, 행사가격이 line으로 쌓여있는 csv


location = 'C:/Users/yuhs19/Downloads/'
filename = 'samu20240125.csv'

msft = yf.Ticker("MSFT")
msft.info
hist = msft.history(period="1mo")
start = "2023-01-01"
end = start + 3
df = yf.download("MSFT", "2023-01-02", "2023-02-02")


#dataframe으로 가져오기
data = pd.read_csv(location+filename)
#data변환 및 정리
#일단 파일을 그대로 따운받고 NaN이 있는 행은 다 날릴것, 그리고 필요없는 열도 다 날릴것
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