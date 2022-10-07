# chmom : Cumulative returns from months t - 6 to t - 1 minus months t - 12 to t - 7.
def parameter():
    para = {}
    para['predictor'] = 'chmom'
    para['relate_finance_index'] = ['clsprc']
    return para
def equation(df):
    df = df.copy()
    df['chmom'] = (df['clsprc'].shift(1) - df['clsprc'].shift(6)) / df[
        'clsprc'].shift(6) - (df['clsprc'].shift(7) - df['clsprc'].shift(12)) / df['clsprc'].shift(12)
    return df