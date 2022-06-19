#
def parameter():
    para = {}
    para['predictor'] = 'ep'
    para['relate_finance_index'] = ['clsprc', 'B003000000']
    return para
def equation(df):
    df = df.copy()
    df['ep'] = df['B003000000'] / df['clsprc'] # df['B00300000'] -> eps
    return df