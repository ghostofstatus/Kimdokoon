def gongmae(data):
    import pandas as pd
    df = data.drop(["수량_상장주식수", "수량_비중", "금액_공매도잔고금액", "금액_시가총액", "금액_비중"], axis=1, inplace=True)
    df = pd.pivot_table(data, index=["일자"], values=["수량_공매도잔고수량"])
    return df.plot(figsize=(16,9))

## KOSPI 공매도 잔량 구하는 함수
def gongmae2(data):
    import pandas as pd
    df = data.drop(["수량_상장주식수", "금액_공매도잔고금액", "금액_시가총액","비중"], axis=1, inplace=True)
    df = pd.pivot_table(data, index=["일자"], values=["수량_공매도잔고수량"])
    return df.plot(figsize=(16,9))

## 개별종목 공매도 잔량 구하는 함수

def jongga(data):
    import pandas as pd
    df = data.drop(["대비", "등락률", "시가","고가","저가","거래량","거래대금","상장시가총액"],axis=1, inplace=True)
    df = pd.pivot_table(data, index=["일자"], values=["종가"])
    return df.plot(figsize=(16,9))

## KOSPI 종가 구하는 함수

def jongga2(data):
    import pandas as pd
    df = data.drop(["대비", "등락률", "시가","고가","저가","거래량","거래대금","시가총액"],axis=1, inplace=True)
    df = pd.pivot_table(data, index=["일자"], values=["종가"])
    return df.plot(figsize=(16,9))

## 개별종목 종가 구하는 법

def percent(data):
    import pandas as pd
    # df = data.drop(["금액_거래대금","금액_공매도거래대금_전체","수량_거래량","수량_공매도거래량_전체","수량_비중",'수량_공매도거래량_업틱룰적용','수량_공매도거래량_업틱룰예외','금액_공매도거래대금_업틱룰적용','금액_공매도거래대금_업틱룰예외'],axis=1, inplace=True)
    df = pd.pivot_table(data, index='일자', values='금액_비중')
    return df.plot(figsize=(16,9))


def trade(data):
    import pandas as pd
    # df_1 = data.drop(["금액_거래대금","금액_공매도거래대금_전체","수량_거래량","금액_비중","수량_비중",'수량_공매도거래량_업틱룰적용','수량_공매도거래량_업틱룰예외','금액_공매도거래대금_업틱룰적용','금액_공매도거래대금_업틱룰예외'],axis=1, inplace=True)
    df_1 = pd.pivot_table(data, index='일자', values='수량_공매도거래량_전체')
    return df_1.plot(figsize=(16,9))


def price(data):
    import pandas as pd
    # df_2 = data.drop(["금액_거래대금","수량_공매도거래량_전체","수량_거래량","금액_비중","수량_비중",'수량_공매도거래량_업틱룰적용','수량_공매도거래량_업틱룰예외','금액_공매도거래대금_업틱룰적용','금액_공매도거래대금_업틱룰예외'],axis=1, inplace=True)
    df_2 = pd.pivot_table(data, index='일자', values='금액_공매도거래대금_전체')
    return df_2.plot(figsize=(16,9))


