# lgr : Quarterly percent change in total liabilities
# 'A002000000': Total Liabilities
def parameter():
    para = {}
    para['predictor'] = 'lgr'
    para['relate_finance_index'] = ['A002000000']
    return para
def equation(df):
    df = df.copy()
    df['lgr'] = df['A002000000'].pct_change(periods=3)
    return df