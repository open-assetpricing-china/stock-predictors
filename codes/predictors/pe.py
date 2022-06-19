#
def parameter():
    para = {}
    para['predictor'] = 'pe'
    para['relate_finance_index'] = ['clsprc', 'B003000000']
    return para
def equation(df):
    df = df.copy()
    df['pe'] = df['clsprc'] / df['B003000000'] # df['B003000000'] -> 'eps'
    return df