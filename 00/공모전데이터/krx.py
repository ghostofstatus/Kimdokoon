import time
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import FinanceDataReader as fdr
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from pykrx import stock

def pykrx(data, value,n,str,end):
    global df
    if data == 1:
        df = stock.get_shorting_status_by_date(str, end, n)
        df = pd.pivot_table(df, index="날짜", values=value)
    elif data == 2:
        df = stock.get_shorting_volume_by_ticker(str)
        df = pd.pivot_table(df, index="티커", values=value)
    elif data == 3:
        df = stock.get_shorting_volume_by_date(str, end, n)
        df = pd.pivot_table(df, index="날짜", values=value)
    elif data == 4:
        df = stock.get_shorting_investor_volume_by_date(str, end, n)
        df = pd.pivot_table(df, index="날짜", values=value)
    elif data == 5:
        df = stock.get_shorting_investor_value_by_date(str, end, n)
        df = pd.pivot_table(df, index="날짜", values=value)
    elif data == 6:
        df = stock.get_shorting_balance_by_date(str, end, n)
        df = pd.pivot_table(df, index="날짜", values=value)
    return df.plot(figsize=(16,9))


def rank(data, day):
    global df
    if data == '공매도비중':
        df = stock.get_shorting_volume_top50(day)
    elif data == '공매도잔고':
        df = stock.get_shorting_balance_top50(day)
    return df

def rank1(data, day):
    global df
    if data == '공매도비중':
        df = stock.get_shorting_volume_top50(day)
        df['위험도'] = 0
        for i in range(len(df)) :
            if df['공매도거래대금증가율'][i] >= 6.0 :
                df['위험도'][i] += 3
            elif df['공매도거래대금증가율'][i] >= 4.0 :
                df['위험도'][i] += 2
            elif df['공매도거래대금증가율'][i] >= 2.0 : 
                df['위험도'][i] += 1
        for i in range(len(df)) :
            if df['주가수익률'][i] <= -10.0 :
                df['위험도'][i] += 4
            elif df['주가수익률'][i] <= -5.0 :
                df['위험도'][i] += 2
            elif df['주가수익률'][i] <= -3.0: 
                df['위험도'][i] += 1
        df['위험도'][[0,1,2,3,4]] += 3
        df['위험도'][[5,6,7,8,9]] += 2
        df['위험도'][[10,11,12,13,14]] += 1
        a = int(input('위험도: '))
        list = []

        for i in range(len(df)) :
            if df['위험도'][i] == a: 
                list.append(i)

    return df.iloc[list]