# 6-month cumulative return.
def parameter():
    para = {}
    para['predictor'] = 'mom6m'
    para['relate_finance_index'] = ['clsprc']
    return para
def equation(df):
    df = df.copy()
    df['mom6m'] = df['clsprc'].pct_change(periods=5).shift(1)
    return df