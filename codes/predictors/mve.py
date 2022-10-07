# Natural log of market capitalization at end of month t-1
#
import numpy as np
def parameter():
    para = {}
    para['predictor'] = 'mve'
    para['relate_finance_index'] = ['size']
    return para
def equation(df):
    df = df.copy()
    df['mve'] = np.log(df['size']).shift(1)
    return df