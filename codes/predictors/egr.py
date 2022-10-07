# egr: Quarterly percent change in book value of equity.
# df['A001000000'] -> Total Asset
def parameter():
    para = {}
    para['predictor'] = 'egr'
    para['relate_finance_index'] = ['A001000000']
    return para
def equation(df):
    df = df.copy()
    df['egr'] = df['A001000000'].pct_change(periods=3)
    return df
#
