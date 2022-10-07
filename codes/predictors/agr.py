#
def parameter():
    para = {}
    para['predictor'] = 'agr'
    para['relate_finance_index'] = ['A001000000'] # Total asset
    return para
def equation(df):
    df = df.copy()
    df['agr'] = (df['A001000000'] - df['A001000000'].shift(12)) / df['A001000000'].shift(12) # df['A001000000'] -> total assets
    return df