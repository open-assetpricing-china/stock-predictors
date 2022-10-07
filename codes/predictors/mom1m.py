# 1-month cumulative return.
def parameter():
    para = {}
    para['predictor'] = 'mom1m'
    para['relate_finance_index'] = ['clsprc']
    return para
def equation(df):
    df = df.copy()
    df['mom1m'] = df['clsprc'].pct_change()
    return df