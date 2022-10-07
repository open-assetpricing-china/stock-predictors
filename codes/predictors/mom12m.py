# mom12m: 11-month cumulative returns ending one month before month end.
def parameter():
    para = {}
    para['predictor'] = 'mom12m'
    para['relate_finance_index'] = ['clsprc']
    return para
def equation(df):
    df = df.copy()
    df['mom12m'] = df['clsprc'].pct_change(periods=11).shift(1)
    return df