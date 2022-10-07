#
def parameter():
    para = {}
    para['predictor'] = 'cashdebt'
    para['relate_finance_index'] = ['B002000000', 'A002000000'] # 'B002000000' : Net Profit
    return para
def equation(df):
    df = df.copy()
    df['cashdebt'] = df['B002000000'] / df['A002000000'] # df['A002000000'] -> Total Liabilities
    return df