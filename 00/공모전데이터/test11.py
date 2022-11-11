import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import FinanceDataReader as fdr
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split

plt.rcParams['font.family'] = 'NanumGothic'


def LSTM(data):
    df = fdr.DataReader(data)
    scaler = MinMaxScaler()
    # 스케일을 적용할 column을 정의합니다.
    scale_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
    # 스케일 후 columns
    scaled = scaler.fit_transform(df[scale_cols])
    df = pd.DataFrame(scaled, columns=scale_cols)
    x_train, x_test, y_train, y_test = train_test_split(df.drop('Close', 1), df['Close'], test_size=0.2, random_state=0, shuffle=False)
    return x_train