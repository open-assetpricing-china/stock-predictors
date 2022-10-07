# nincr: Number of consecutive quarters (up to eight quarters) with an
# increase in earnings.
# Net Profit : 'B002000000'
def parameter():
    para = {}
    para['predictor'] = 'nincr'
    para['relate_finance_index'] = ['B002000000']
    return para
#
def equation(df):
    df = df.copy()
    df['earn_diff'] = df['B002000000'] - df['B002000000'].shift(3)
    df['earn_dummy'] = df['earn_diff'].apply(lambda x: 1 if x>=0 else 0)
    df['nincr'] = df['earn_dummy'].rolling(24).sum()
    df.drop(columns=['earn_diff', 'earn_dummy'], inplace=True)
    return df