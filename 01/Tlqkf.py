import pandas as pd
pd.options.display.float_format = '{:.5f}'.format

def Tlqkf(data):
    data['상장주식수대비거래량'] = (data['거래량']/data['상장주식수'])*100
    idx = data[data['시가']==0].index
    data = data.drop(idx)
    data = data.sort_values('상장주식수대비거래량',ascending=True)
    return data