from lib2to3.pgen2.pgen import DFAState
import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import FinanceDataReader as fdr
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from pykrx import stock

def dan(code,day,onedayago):
    trade = stock.get_market_ohlcv(day)                 ## 해당 날짜의 KOSPI 시가, 저가, 고가, 종가, 변동률을 데이터프레임으로 불러옴(시가, 종가, 등락률 사용)
    rank = stock.get_shorting_volume_top50(day)         ## 공매도 거래량 상위 50종목 데이터프레임 불러옴 (공매도거래대금, 직전40일거래대금평균, 공매도거래대금증가율, 공매도비중, 직전40일공매도평균비중 사용)
    name = stock.get_market_price_change(day,day)       ## 모든 종목의 가격변동 데이터프레임인데 종목명 가져올려고 씀 다른이유없음(종목명 사용)
    name.drop(['시가','종가','거래량','거래대금','등락률'], axis=1,inplace=True)    ## 종목명을 제외한 모든 컬럼들 제거
    many = pd.read_csv('./csv/5years2.csv')     ## 최근 5년동안 공매도 과열종목에 올라간 기업들과 그 횟수(과열횟수 사용)
    many.drop(['Unnamed: 0'],axis=1,inplace=True)       ## 쓸데없는 컬럼 제거
    jan = stock.get_shorting_status_by_date(onedayago, day, code)       ## 잔고수량 확인하기 위한 데이터프레임(잔고수량 사용)
    jan.drop(['거래량','거래대금','잔고금액'],axis=1,inplace=True)  ## 쓸데없는 컬럼 제거
    jan['티커'] = code      ## merge를 사용해 다른 데이터 프레임과 합치기 위해 같은 컬럼 생성
    jan['잔고수량증가율'] = ((jan['잔고수량'].shift(1)-jan['잔고수량'])/jan['잔고수량'])*100        ## 잔고수량 증가율 확인을 위한 데이터 프레임 생성
    jan.dropna(axis=0 , inplace=True)       ## 결측치가 있는 행 제거
    jan.set_index(['티커'], inplace=True)       ## jan 데이터프레임의 인덱스를 티커 컬럼의 값으로 교체
    rank_trade = pd.merge(rank,trade,on="티커", how='inner')    ## rank와 trade 를 티커 값을 기준으로 merge로 합쳐서 rank_trade로 제작
    rank_name = pd.merge(rank_trade,name,on='티커',how='inner')     ## merge가 한번에 두개의 데이터프레임만 합칠 수 있어서 합친 데이터프레임과 name 데이터프레임을 다시 합침
    rank_name.drop(['총거래대금','고가','저가','거래량','거래대금','변동폭','주가수익률'],axis=1, inplace=True)     ## 합친 데이터프레임에서 쓸모없는 컬럼과 중복컬럼을 제거
    df = pd.merge(rank_name,jan,on='티커',how='inner')      ## 잔고수량증가율을 추가하기 위해 다시 merge를 사용해 합침
    df = df[['종목명','시가','종가','등락률','공매도거래대금','직전40일거래대금평균','공매도거래대금증가율','공매도비중','직전40일공매도평균비중','공매도비중증가율','잔고수량','잔고수량증가율','순위']]       ## 합쳐져서 나온 데이터프레임의 컬럼 순서 변경
    rank_name_many = pd.merge(df,many,on='종목명',how='left')       ## df와 5년동안 과열횟수 데이터프레임을 마지막으로 합침
    rank_name_many.set_index(['종목명'],inplace=True)       ## 나온 데이터 프레임의 인덱스를 종목명 값으로 교체(인덱스 종목코드(티커) -> 종목명)
    rank_name_many['과열횟수'] = rank_name_many['과열횟수'].fillna(0)       ## 과열횟수의 결측치를 0으로 교체
    rank_name_many['위험도수치'] = 0        ## 계산할 위험도수치 컬럼을 만들고 기본값으로 0을 배정
    for i in range(len(rank_name_many)) :       ## 위험도수치를 계산하기 위한 for문
            if rank_name_many['공매도거래대금증가율'][i] >= 3.0 :       ## 공매도거래대금증가율에 따른 위험도 수치를 배정하기 위한 for문 안의 조건문들(공매도거래대금증가율이 3%이상이면 5점부여)
                rank_name_many['위험도수치'][i] += 5
            elif rank_name_many['공매도거래대금증가율'][i] >= 2.5 :
                rank_name_many['위험도수치'][i] += 4
            elif rank_name_many['공매도거래대금증가율'][i] >= 2.0 : 
                rank_name_many['위험도수치'][i] += 3
            elif rank_name_many['공매도거래대금증가율'][i] >= 1.5 : 
                rank_name_many['위험도수치'][i] += 2
            elif rank_name_many['공매도거래대금증가율'][i] >= 1.0 : 
                rank_name_many['위험도수치'][i] += 1
    for i in range(len(rank_name_many)) :       ## 위험도수치를 계산하기 위한 for문
            if rank_name_many['공매도비중증가율'][i] >= 3.0 :           ## 공매도비중증가율에 따른 위험도 수치를 배정하기 위한 for문 안의 조건문들(공매도비중증가율이 3% 이상이면 5점 부여)
                rank_name_many['위험도수치'][i] += 5
            elif rank_name_many['공매도비중증가율'][i] >= 2.5 :
                rank_name_many['위험도수치'][i] += 4
            elif rank_name_many['공매도비중증가율'][i] >= 2.0 : 
                rank_name_many['위험도수치'][i] += 3
            elif rank_name_many['공매도비중증가율'][i] >= 1.5 : 
                rank_name_many['위험도수치'][i] += 2
            elif rank_name_many['공매도비중증가율'][i] >= 1.0 : 
                rank_name_many['위험도수치'][i] += 1
    for i in range(len(rank_name_many)) :
            if rank_name_many['등락률'][i] <= -10.0 :   ## 위험도수치를 계산하기 위한 for문
                rank_name_many['위험도수치'][i] += 5    ##  공매도비중증가율에 따른 위험도 수치를 배정하기 위한 for문 안의 조건문들(등락률이 -10% 이하면 5범 부여)
            elif rank_name_many['등락률'][i] <= -8.0 :
                rank_name_many['위험도수치'][i] += 4
            elif rank_name_many['등락률'][i] <= -6.0 : 
                rank_name_many['위험도수치'][i] += 3
            elif rank_name_many['등락률'][i] <= -4.0 : 
                rank_name_many['위험도수치'][i] += 2
            elif rank_name_many['등락률'][i] <= -2.0 : 
                rank_name_many['위험도수치'][i] += 1
    for i in range(len(rank_name_many)) :           ## 위험도수치를 계산하기 위한 for문
            if rank_name_many['과열횟수'][i] >= 5.0 :       #  공매도비중증가율에 따른 위험도 수치를 배정하기 위한 for문 안의 조건문들(최근 5년동안의 과열횟수가 5회 이상이면 5점부여)
                rank_name_many['위험도수치'][i] += 5
            elif rank_name_many['과열횟수'][i] >= 4.0 :
                rank_name_many['위험도수치'][i] += 4
            elif rank_name_many['과열횟수'][i] >= 3.0 : 
                rank_name_many['위험도수치'][i] += 3
            elif rank_name_many['과열횟수'][i] >= 2.0 : 
                rank_name_many['위험도수치'][i] += 2
            elif rank_name_many['과열횟수'][i] >= 1.0 : 
                rank_name_many['위험도수치'][i] += 1
    for i in range(len(rank_name_many)) :            ## 위험도수치를 계산하기 위한 for문
            if rank_name_many['잔고수량증가율'][i] >= 25.0 :         #  공매도비중증가율에 따른 위험도 수치를 배정하기 위한 for문 안의 조건문들(잔고수량증가율이 25%이상이면 5점부여)
                rank_name_many['위험도수치'][i] += 5
            elif rank_name_many['잔고수량증가율'][i] >= 20.0 :
                rank_name_many['위험도수치'][i] += 4
            elif rank_name_many['잔고수량증가율'][i] >= 15.0 : 
                rank_name_many['위험도수치'][i] += 3
            elif rank_name_many['잔고수량증가율'][i] >= 10.0 : 
                rank_name_many['위험도수치'][i] += 2
            elif rank_name_many['잔고수량증가율'][i] >= 5.0 : 
                rank_name_many['위험도수치'][i] += 1
    rank_name_many['위험도'] = ''       ## 데이터 프레임에 위험도 컬럼 생성
    if rank_name_many['위험도수치'].values>= 20.0 :     ## 위험도 수치가 20이상이면 위험도 level5 점수가 5점 줄어들때마다 레벨을 한단계씩 낮춤
        rank_name_many['위험도'] ='Level5'
    elif rank_name_many['위험도수치'].values >= 15.0 :
        rank_name_many['위험도'] = 'Level4'
    elif rank_name_many['위험도수치'].values >= 10.0 : 
        rank_name_many['위험도'] = 'Level3'
    elif rank_name_many['위험도수치'].values >= 5.0 : 
        rank_name_many['위험도'] = 'Level2'
    elif rank_name_many['위험도수치'].values >= 0.0 : 
        rank_name_many['위험도'] = 'Level1'
    else:
        rank_name_many['위험도'] =np.NaN  
    
    return rank_name_many           ## 여태까지 한 작업의 데이터프레임을 나오게함

