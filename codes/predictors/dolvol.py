# dolvol : Natural logarithm of trading volume times price per share from month t-2
#
import numpy as np
def parameter():
    para = {}
    para['predictor'] = 'dolvol'
    para['relate_finance_index'] = ['mtrdvalue']
    return para
def equation(df):
    df = df.copy()
    df['dolvol'] = np.log(df['mtrdvalue']).shift(2)
    return df
#
