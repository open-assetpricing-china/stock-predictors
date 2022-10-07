#
def parameter():
    para = {}
    para['predictor'] = 'bm'
    para['relate_finance_index'] = ['A001000000', 'size'] # size : 总市值
    return para
def equation(df):
    df = df.copy()
    df['bm'] = df['A001000000'] / df['size'] # df['A001000000'] -> Total Asset
    return df