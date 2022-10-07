# Cumulative returns from months t-36 to t-13
def parameter():
    para = {}
    para['predictor'] = 'mom36m'
    para['relate_finance_index'] = ['clsprc']
    return para
def equation(df):
    df = df.copy()
    df['mom36m'] = (df['clsprc'].shift(13) - df['clsprc'].shift(36)
                    ) / df['clsprc'].shift(36)
    return df