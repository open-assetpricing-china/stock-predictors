#
def parameter():
    para = {}
    para['predictor'] = 'cash'
    para['relate_finance_index'] = ['A001000000', 'A001101000'] # 'A001101000' : cash and cash equivalents
    return para
def equation(df):
    df = df.copy()
    df['cash'] = df['A001101000'] / df['A001000000'] # df['A001000000'] -> Total Asset
    return df