#
def parameter():
    para = {}
    para['predictor'] = 'market_cap'
    para['relate_finance_index'] = ['size']
    return para
def equation(df):
    df = df.copy()
    df['market_cap'] = df['size']
    return df

