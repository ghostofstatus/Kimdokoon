from pykrx import stock
from pykrx import bond
import matplotlib.pyplot as plt


def chart(code,start_date,end_date):
    data_df = stock.get_market_ohlcv(start_date, end_date, code, "m")
    data_df.drop(['시가','저가','고가'],axis=1,inplace=True)
    
    xs=data_df.index.to_list()					#플롯할 데이터 모두 list로 저장
    ys_close=data_df['종가'].to_list()
    ys_volume=data_df['거래량'].to_list()

    plt.figure(figsize=(10, 8))					#전체 그래프 크기 설정

    plt.subplot(2,1,1)						#2행 1열에서 1번째 그래프 지정
    plt.plot(xs, ys_close, 'o-', ms=3, lw=1, label='close')		#xy데이터 플롯-line		#xy데이터 플롯	
    plt.xlabel('Date')						#x축 이름 
    plt.ylabel('Price * 10^7 (KRW)')				#y축 이름
    plt.legend()							#범례 표시

    plt.subplot(2,1,2)						#2행 1열에서 2번재 그래프 지정
    plt.plot(xs, ys_volume, color='grey', label='volume')		#xy데이터 플롯-bar
    plt.xlabel('Date')						#x축 이름
    plt.ylabel('Volume')						#y축 이름
    plt.legend()							#범례 표시
